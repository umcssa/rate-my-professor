import flask
import rmp
import json


@rmp.app.route('/api/rate-my-professor/get-departments/', methods=['GET'])
def get_departments():
    return json.dumps(rmp.model.get_all_departments())


@rmp.app.route('/api/rate-my-professor/get-courses/', methods=['GET'])
def get_courses():
    department = flask.request.args.get('department')
    departments = json.dumps(rmp.model.get_all_departments())
    if department in departments:
        return json.dumps(rmp.model.get_courses(department))
    else:
        return '[]'


@rmp.app.route('/api/rate-my-professor/get-professors/', methods=['GET'])
def get_professors():
    department = flask.request.args.get('department')
    departments = json.dumps(rmp.model.get_all_departments())
    if department in departments:
        return json.dumps(rmp.model.get_professors(department))
    else:
        return '[]'


@rmp.app.route('/api/rate-my-professor/rmp-form/', methods=['GET', 'POST'])
def process_rmp_form():
    if not rmp.model.validate_form(flask.request.form):
        return 'invalid'
    if rmp.model.save_rate(flask.request.form):
        return 'success'
    else:
        return 'fail'


@rmp.app.route('/api/rate-my-professor/get-viewable-departments/', methods=['GET'])
def get_viewable_departments():
    return json.dumps(rmp.model.get_viewable_departments())


@rmp.app.route('/api/rate-my-professor/get-viewable-courses/', methods=['GET'])
def get_viewable_courses():
    department = flask.request.args.get('department')
    departments = json.dumps(rmp.model.get_viewable_departments())
    if department in departments:
        return json.dumps(rmp.model.get_viewable_courses(department))
    else:
        return '[]'


@rmp.app.route('/api/rate-my-professor/get-viewable-professors/', methods=['GET'])
def get_viewable_professors():
    department = flask.request.args.get('department')
    departments = json.dumps(rmp.model.get_viewable_departments())
    if department in departments:
        return json.dumps(rmp.model.get_viewable_professors(department))
    else:
        return '[]'


@rmp.app.route('/api/rate-my-professor/rmp-search/', methods=['GET', 'POST'])
def search_rate():
    return json.dumps(rmp.model.search_rate(flask.request.form))


@rmp.app.route('/api/rate-my-professor/verification/', methods=['GET'])
def verify_rate():
    if rmp.model.verify_rate(flask.request.args.get('id'), flask.request.args.get('token')):
        rmp.model.make_rate_viewable(flask.request.args.get('id'))
        return flask.redirect('/rate-my-professor/verification-success/')
    else:
        return flask.redirect('/rate-my-professor/verification-fail/')

# @rmp.app.route('/api/rate-my-professor/auto-update-rates/', methods=['GET'])
# def auto_update_rates():
#     rmp.model.auto_update_rates()
#     return 'updated'
