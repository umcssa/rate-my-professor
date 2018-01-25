"""Insta485 user view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/u/<username>/', methods=['GET', 'POST'])
def user(username):
    """Display /u/<username>/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    if flask.request.method == 'POST':
        if 'create_post' in flask.request.form \
                and 'file' in flask.request.files:
            filename = insta485.model.save_file()
            insta485.model.create_post(
                flask.session[
                    insta485.app.config['SESSION_COOKIE_NAME']],
                filename)
        elif 'follow' in flask.request.form:
            insta485.model.follow_user(
                flask.session[
                    insta485.app.config['SESSION_COOKIE_NAME']],
                flask.request.form['username'])
        elif 'unfollow' in flask.request.form:
            insta485.model.unfollow_user(
                flask.session[
                    insta485.app.config['SESSION_COOKIE_NAME']],
                flask.request.form[
                    'username'])
    context = insta485.model.get_user_info_verbose(
        username,
        flask.session[insta485.app.config['SESSION_COOKIE_NAME']])
    context['logname'] = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    return flask.render_template("user.html", **context)
