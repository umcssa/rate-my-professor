"""Insta485 followers view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/u/<username>/followers/',
                    methods=['GET', 'POST'])
def followers(username):
    """Display /u/<username>/followers/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    logname_follower = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    if flask.request.method == 'POST':
        if 'follow' in flask.request.form:
            insta485.model.follow_user(logname_follower,
                                       flask.request.form['username'])
        elif 'unfollow' in flask.request.form:
            insta485.model.unfollow_user(logname_follower,
                                         flask.request.form[
                                             'username'])
    context = {}
    context['logname'] = logname_follower
    context['followers'] = insta485.model.get_followers(username,
                                                        logname_follower)
    return flask.render_template("followers.html", **context)
