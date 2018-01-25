"""Insta485 index view."""
import flask
import insta485
import insta485.model


@insta485.app.route('/test/', methods=['GET', 'POST'])
def test():
    """Display /test/ route."""
    return flask.render_template("test.html")
