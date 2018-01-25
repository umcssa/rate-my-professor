"""Insta485 explore view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/explore/', methods=['GET', 'POST'])
def explore():
    """Display /explore/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    if flask.request.method == 'POST':
        insta485.model.follow_user(
            flask.session[insta485.app.config['SESSION_COOKIE_NAME']],
            flask.request.form['username'])
    context = {}
    context['logname'] = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    context['not_following'] = insta485.model.get_not_following(
        flask.session[
            insta485.app.config['SESSION_COOKIE_NAME']])
    return flask.render_template("explore.html", **context)
