"""Insta485 password view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
def password():
    """Display /accounts/password/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    if flask.request.method == 'POST':
        user = {}
        user['username'] = flask.session[
            insta485.app.config['SESSION_COOKIE_NAME']]
        user['password'] = flask.request.form['password']
        user['new_password1'] = flask.request.form[
            'new_password1']
        user['new_password2'] = flask.request.form[
            'new_password2']
        result = int(insta485.model.change_password(user))
        if result == 403 or result == 401:
            return flask.abort(result)
        if result:
            return flask.redirect(flask.url_for('edit'))
    context = {}
    context['logname'] = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    return flask.render_template("password.html", **context)
