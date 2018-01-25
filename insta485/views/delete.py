"""Insta485 delete view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def delete():
    """Display /accounts/delete/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    logname = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    if flask.request.method == 'POST' and \
            flask.request.form['delete'] == 'confirm delete account':
        insta485.model.delete_user(logname)
        flask.session.pop(insta485.app.config['SESSION_COOKIE_NAME'])
        return flask.redirect(flask.url_for('create'))
    context = {}
    context['logname'] = logname
    return flask.render_template("delete.html", **context)
