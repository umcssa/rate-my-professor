"""Insta485 edit view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """Display /accounts/edit/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    logname_edit = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    if flask.request.method == 'POST':
        user = {}
        if 'file' in flask.request.files:
            user['filename'] = insta485.model.save_file()
        user['username'] = logname_edit
        user['fullname'] = flask.request.form['fullname']
        user['email'] = flask.request.form['email']
        insta485.model.update_user(user)
    context = insta485.model.get_user_info_edit(logname_edit)
    context['logname'] = logname_edit
    return flask.render_template("edit.html", **context)
