"""Insta485 create view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def create():
    """Display /accounts/create/ route."""
    if insta485.app.config['SESSION_COOKIE_NAME'] in flask.session:
        return flask.redirect(flask.url_for('edit'))
    if flask.request.method == 'POST':
        user = {}
        user['filename'] = insta485.model.save_file()
        user['fullname'] = flask.request.form['fullname']
        user['username'] = flask.request.form['username']
        user['email'] = flask.request.form['email']
        user['password'] = insta485.model.get_password_db_string(
            flask.request.form['password'])
        insta485.model.create_user(user)
        flask.session[
            insta485.app.config['SESSION_COOKIE_NAME']] = \
            user['username']
        return flask.redirect(flask.url_for('index'))
    context = {}
    return flask.render_template("create.html", **context)
