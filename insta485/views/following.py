"""Insta485 following view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/u/<username>/following/',
                    methods=['GET', 'POST'])
def following(username):
    """Display /u/<username>/following/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    logname_following = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    if flask.request.method == 'POST':
        if 'unfollow' in flask.request.form:
            insta485.model.unfollow_user(logname_following,
                                         flask.request.form[
                                             'username'])
        elif 'follow' in flask.request.form:
            insta485.model.follow_user(logname_following,
                                       flask.request.form['username'])
    context = {}
    context['logname'] = logname_following
    context['following'] = insta485.model.get_following(username,
                                                        logname_following)
    return flask.render_template("following.html", **context)
