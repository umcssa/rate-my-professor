import os
import re
import flask

departments = ['EECS', 'STATS']
sql = ""

department_id = 0
for department in departments:
    department_id += 1
    if os.path.exists(os.path.join('data',department+'_professors.txt')):
        read_file = open(os.path.join('data',department+'_professors.txt'))
        professors = list(set(read_file.readlines()))
        sql += "\nINSERT INTO professors (departmentid, name) VALUES \n"
        for professor in professors:
            sql += "(" + str(department_id) + ", '" + flask.Markup(professor[:-1]).unescape() + "'), \n"
        sql = sql[:-3] + ";\n"
    if os.path.exists(os.path.join('data', department + '_courses.txt')):
        read_file = open(os.path.join('data', department + '_courses.txt'))
        courses = read_file.readlines()
        sql += "\nINSERT INTO courses (departmentid, number, title) VALUES \n"
        for course in courses:
            result = re.findall('^\w+ (\d{3}): (.+)$', course)[0]
            number = result[0]
            title = flask.Markup(result[1]).unescape()
            sql += "(" + str(department_id) + ", " + number + ", '" + title + "'), \n"
        sql = sql[:-3] + ";\n"

output = open('sql/data.sql', 'w')
output.write(sql)
