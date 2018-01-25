"""Insta485 logout view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/accounts/logout/')
def logout():
    """Display /accounts/logout/ route."""
    if insta485.app.config['SESSION_COOKIE_NAME'] in flask.session:
        flask.session.pop(insta485.app.config['SESSION_COOKIE_NAME'])
    return flask.redirect(flask.url_for('login'))
