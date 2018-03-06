"""RMP model (database) API."""
import os
import re
import hashlib
import uuid
import shutil
import tempfile
import sqlite3
import flask
import arrow
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import rmp
from rmp.api.invalid_usage import InvalidUsage


def dict_factory(cursor, row):
    """
    Convert database row objects to a dictionary.

    This is useful for building dictionaries which
    are then used to render a template. Note that
    this would be inefficient for large queries.
    """
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            rmp.app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@rmp.app.teardown_appcontext
def close_db(error):
    # pylint: disable=unused-argument
    """Close the database at the end of a request."""
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()


# Rate My Professor

def get_all_departments():
    cur = get_db().execute(
        "SELECT name FROM department ORDER BY name ASC")
    results = cur.fetchall()
    departments = []
    for result in results:
        departments.append(result['name'])
    cur.close()
    return departments


def get_courses(department):
    cur = get_db().execute(
        "SELECT department.name, course.number, course.title FROM course INNER JOIN department WHERE upper(department.name)=upper(?) AND course.department_id=department.department_id ORDER BY department.name ASC, course.number ASC",
        (department,))
    results = cur.fetchall()
    courses = []
    for result in results:
        courses.append(
            '{} {}: {}'.format(result['name'], result['number'],
                               result['title']))
    cur.close()
    return courses


def get_professors(department):
    cur = get_db().execute(
        "SELECT professor.name FROM professor INNER JOIN department WHERE upper(department.name)=upper(?) AND professor.department_id=department.department_id ORDER BY professor.name ASC",
        (department,))
    results = cur.fetchall()
    professors = []
    for result in results:
        professors.append(result['name'])
    cur.close()
    return professors


def validate_form(rate):
    return bool(re.match(r'^\d{4} (spring|summer|fall|winter)$',
                         rate.get('semester').lower()))


def save_rate(rate):
    try:
        cur = get_db().cursor()
        semester = re.findall(r'^(\d{4}) (spring|summer|fall|winter)$',
                              rate.get('semester').lower())[0]

        result = cur.execute(
            "SELECT semester_id FROM semester WHERE year=? AND season=?",
            (semester[0], semester[1])).fetchone()
        if result:
            semester_id = result['semester_id']
        else:
            cur.execute(
                "INSERT INTO semester (year, season) VALUES (?,?)",
                (semester[0], semester[1]))
            semester_id = cur.execute("SELECT last_insert_rowid() FROM semester").fetchone()['last_insert_rowid()']

        types = rate.getlist('type[]')
        suggestion = rate.get('suggestion')
        cur.execute(
            "INSERT INTO rate (rate_id, course_title, professor_name, semester_id, credits, isHU, isSS, isNS, isID, isRE, isOther, grade, difficulty, quality, workload, recommend, suggestion) VALUES "
            "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                rate.get('rate_id'),
                rate.get('course'), rate.get('professor'), semester_id,
                rate.get('credits'), 'HU' in types, 'SS' in types,
                'NS' in types, 'ID' in types, 'RE' in types,
                'Other' in types,
                rate.get('grade'), rate.get('difficulty'),
                rate.get('quality'), rate.get('workload'),
                rate.get('recommend'),
                None if suggestion == None or str(
                    suggestion).strip() == '' else suggestion)
        )
        rate_id = cur.execute("SELECT last_insert_rowid() FROM rate").fetchone()['last_insert_rowid()']
        cur.close()
        return send_verification_email(rate_id, rate.get('uniqname'))
    except sqlite3.Error:
        return False


def get_viewable_departments():
    cur = get_db().execute(
        "SELECT DISTINCT department.name FROM rate INNER JOIN course ON rate.course_id=course.course_id INNER JOIN department ON course.department_id=department.department_id WHERE rate.viewable=1 ORDER BY name ASC")
    results = cur.fetchall()
    departments = []
    for result in results:
        departments.append(result['name'])
    cur.close()
    return departments


def get_viewable_courses(department):
    cur = get_db().execute(
        "SELECT DISTINCT department.name, course.number, course.title FROM rate INNER JOIN course ON rate.course_id=course.course_id INNER JOIN department WHERE upper(department.name)=upper(?) AND course.department_id=department.department_id ORDER BY department.name ASC, course.number ASC",
        (department,))
    results = cur.fetchall()
    courses = []
    for result in results:
        courses.append(
            '{} {}: {}'.format(result['name'], result['number'],
                               result['title']))
    cur.close()
    return courses


def get_viewable_professors(department):
    cur = get_db().execute(
        "SELECT DISTINCT professor.name FROM rate INNER JOIN professor ON rate.professor_id=professor.professor_id INNER JOIN department WHERE upper(department.name)=upper(?) AND professor.department_id=department.department_id ORDER BY professor.name ASC",
        (department,))
    results = cur.fetchall()
    professors = []
    for result in results:
        professors.append(result['name'])
    cur.close()
    return professors


def get_keywords(string):
    """Get keywords from string, with % as prefix and suffix."""
    keywords = re.sub('[^a-zA-Z0-9]', ' ', string).split()
    if len(keywords) == 0:
        keywords = ['']
    for i, keyword in enumerate(keywords):
        keywords[i] = '%' + keyword + '%'
    return keywords


def search_rate(rate):
    offset = int(rate.get('offset'))
    department = (rate.get('department') if rate.get('department') else '') + '%'

    course = rate.get('course') if rate.get('course') else ''
    course_keywords = get_keywords(course)

    professor = rate.get('professor') if rate.get('professor') else ''
    professor_keywords = get_keywords(professor)

    credits = rate.getlist('credits[]')
    if (len(credits) == 5):
        credits.append('0')
    elif (len(credits) == 0):
        credits.append('-1')

    types = rate.getlist('type[]')
    excluded_types = []
    for type in ['HU', 'SS', 'NS', 'ID', 'RE', 'Other']:
        if type not in types:
            excluded_types.append(type)

    grades = rate.getlist('grade[]')
    if (len(grades) == 0):
        grades.append('')

    difficulty = rate.getlist('difficulty[]')
    quality = rate.getlist('quality[]')
    workload = rate.getlist('workload[]')
    recommend = rate.getlist('recommend[]')

    sql = "SELECT rate.*, semester.year, semester.season FROM rate INNER JOIN semester ON rate.semester_id = semester.semester_id WHERE rate.course_title LIKE ?" + " AND rate.course_title LIKE ?" * len(
        course_keywords) + " AND rate.professor_name LIKE ?" * len(
        professor_keywords) + " AND (rate.credits=?" + " OR rate.credits=?" * (len(
        credits) - 1) + ")" + (" AND rate.isHU=0" if 'HU' in excluded_types else "") + (
              " AND rate.isSS=0" if 'SS' in excluded_types else "") + (
              " AND rate.isNS=0" if 'NS' in excluded_types else "") + (
              " AND rate.isID=0" if 'ID' in excluded_types else "") + (
              " AND rate.isRE=0" if 'RE' in excluded_types else "") + (
              " AND rate.isOther=0" if 'Other' in excluded_types else "") + " AND (rate.grade=?" + " OR rate.grade=?" * (
                  len(grades) - 1) + ")" + "".join(
        [" AND rate.{}>=? AND rate.{}<=?".format(i, i) for i in
         ['difficulty', 'quality', 'workload', 'recommend']]) + " ORDER BY rate.rate_id DESC"

    data = get_db().execute(sql, tuple([
                                           department] + course_keywords + professor_keywords + credits + grades + difficulty + quality + workload + recommend)).fetchall()

    data = [item for item in data if rate_in_range(item, rate.getlist('semester[]'))]
    return {'results': data[offset:offset + 10], 'total': len(data), 'offset': offset}


def rate_in_range(rate, range):
    months = convert_semester_to_months(rate['year'], rate['season'])
    return range[0] <= months[0] and range[1] >= months[1]


def convert_semester_to_months(year, season):
    seasons = ['spring', 'summer', 'fall', 'winter']
    begins = ['05', '06', '09', '01']
    ends = ['06', '08', '12', '04']
    return [str(year) + '-' + begins[seasons.index(season)], str(year) + '-' + ends[seasons.index(season)]]


# def auto_update_rates():
#     """For all rates that are not viewable, update course_id and professor_id."""
#     cur = get_db().cursor()
#     rates = cur.execute(
#         "SELECT rate_id, course_id, course_title, professor_id, professor_name FROM rate WHERE viewable=0").fetchall()
#     for rate in rates:
#         if not rate['course_id']:
#             course_keywords = get_keywords(rate['course_title'])
#             courses = cur.execute(
#                 "SELECT d.name, c.course_id, c.number, c.title FROM course c INNER JOIN department d ON c.department_id = d.department_id WHERE 1" + " AND d.name||c.number||c.title LIKE ?" * len(
#                     course_keywords), tuple(course_keywords)).fetchall()
#             if len(courses) == 1:
#                 print(course_keywords)
#                 print(courses)
#                 cur.execute("UPDATE rate SET course_id=?, course_title=NULL WHERE rate_id=?",
#                             (courses[0]['course_id'], rate['rate_id']))
#             elif len(courses) > 1:
#                 print(course_keywords)
#                 print(courses)
#         if not rate['professor_id']:
#             professor_keywords = get_keywords(rate['professor_name'])
#             professors = cur.execute(
#                 "SELECT professor_id, name FROM professor WHERE 1" + " AND name LIKE ?" * len(
#                     professor_keywords), tuple(professor_keywords)).fetchall()
#             if len(professors) == 1 or (len(professors) > 1 and professors[0]['name'] == professors[1]['name']):
#                 print(professor_keywords)
#                 print(professors)
#                 cur.execute("UPDATE rate SET professor_id=?, professor_name=NULL WHERE rate_id=?",
#                             (professors[0]['professor_id'], rate['rate_id']))
#
#     rates = cur.execute(
#         "SELECT rate_id, course_id, course_title, professor_id, professor_name FROM rate WHERE viewable=0").fetchall()
#     for rate in rates:
#         if rate['course_id'] and rate['professor_id']:
#             cur.execute("UPDATE rate SET viewable=1 WHERE rate_id=?", (rate['rate_id'],))
#
#
# def fill_in_rates():
#     cur = get_db().cursor()
#     rates = cur.execute(
#         "SELECT rate_id, course_id, course_title, professor_id, professor_name FROM rate").fetchall()
#     for rate in rates:
#         if not rate['course_title'] and rate['course_id']:
#             course = cur.execute(
#                 "SELECT d.name, c.number, c.title FROM course c INNER JOIN department d ON c.department_id = d.department_id WHERE c.course_id = ?",
#                 (rate['course_id'],)).fetchone()
#             cur.execute("UPDATE rate SET course_title=? WHERE rate_id=?",
#                         (course['name'] + ' ' + str(course['number']) + ': ' + course['title'], rate['rate_id']))
#         if not rate['professor_name'] and rate['professor_id']:
#             professor = cur.execute(
#                 "SELECT name FROM professor WHERE professor_id = ?",
#                 (rate['professor_id'],)).fetchone()
#             cur.execute("UPDATE rate SET professor_name=? WHERE rate_id=?",
#                         (professor['name'], rate['rate_id']))


def send_verification_email(rate_id, uniqname):
    from_address = os.environ['CSSA_APPS_EMAIL_ADDRESS']
    from_password = os.environ['CSSA_APPS_EMAIL_PASSWORD']

    to_address = uniqname + '@umich.edu'
    if not re.match(r'[^@]+@[^@]+\.[^@]+', to_address):
        return False

    try:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(from_address, from_password)

        msg = MIMEMultipart()
        message_template = Template(
            'Dear ${PERSON_NAME}, \n\nPlease use the following security code for the UM-CSSA account: ${ACCOUNT}.\n\nAnd your Security Code is: ${URL}\n\nThanks,\nUM-CSSA account team\n')
        message = message_template.substitute(PERSON_NAME=uniqname, ACCOUNT=to_address,
                                              URL="app.um-cssa.org/verification/" + str(rate_id))

        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = "UM-CSSA account security code"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

        s.quit()
        return True
    except:
        return False
