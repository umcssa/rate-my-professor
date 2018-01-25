"""Insta485 post view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/p/<int:postid>/', methods=['GET', 'POST'])
def post(postid):
    """Display /p/<int:postid>/ route."""
    if insta485.model.check_login() != 'login':
        return insta485.model.check_login()
    logname_post = flask.session[
        insta485.app.config['SESSION_COOKIE_NAME']]
    if flask.request.method == 'POST':
        if 'uncomment' in flask.request.form:
            commentid = flask.request.form['commentid']
            insta485.model.delete_comment(commentid)
        elif 'delete' in flask.request.form:
            postid = flask.request.form['postid']
            insta485.model.delete_post(postid)
            return flask.redirect(
                flask.url_for('user', username=logname_post))
        elif 'like' in flask.request.form:
            postid = flask.request.form['postid']
            insta485.model.like_post(logname_post, postid)
        elif 'comment' in flask.request.form:
            postid = flask.request.form['postid']
            text = flask.request.form['text']
            insta485.model.add_comment(logname_post, postid, text)
        elif 'unlike' in flask.request.form:
            postid = flask.request.form['postid']
            insta485.model.unlike_post(logname_post, postid)
    context = insta485.model.get_post(postid, logname_post)
    context['logname'] = logname_post
    return flask.render_template("post.html", **context)
