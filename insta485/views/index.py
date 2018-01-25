"""Insta485 index view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/', methods=['GET', 'POST'])
def index():
    """Display / route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    logname_index = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    if flask.request.method == 'POST':
        if 'like' in flask.request.form:
            postid = flask.request.form['postid']
            insta485.model.like_post(logname_index, postid)
        elif 'unlike' in flask.request.form:
            postid = flask.request.form['postid']
            insta485.model.unlike_post(logname_index, postid)
        elif 'comment' in flask.request.form:
            postid = flask.request.form['postid']
            text = flask.request.form['text']
            insta485.model.add_comment(logname_index, postid, text)
    context = {}
    logname = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    context['logname'] = logname
    context['posts'] = insta485.model.get_posts(logname)
    return flask.render_template("index.html", **context)
