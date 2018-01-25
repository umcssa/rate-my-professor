"""Insta485 login view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """Display /accounts/login/ route."""
    if insta485.app.config['SESSION_COOKIE_NAME'] in flask.session:
        return flask.redirect(flask.url_for('index'))
    if flask.request.method == 'POST' and insta485.model.check_password(
            flask.request.form['username'],
            flask.request.form['password']):
        flask.session[insta485.app.config['SESSION_COOKIE_NAME']] = \
            flask.request.form['username']
        return flask.redirect(flask.url_for('index'))
    context = {}
    return flask.render_template("login.html", **context)
