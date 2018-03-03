"""RMP index view."""
import flask
import rmp
import rmp.model
import random

@rmp.app.route(rmp.app.config['APPLICATION_ROOT'], defaults={'path': ''})
@rmp.app.route(rmp.app.config['APPLICATION_ROOT'] + '<path:path>')
def index(path):
    """Display / route."""
    return flask.render_template('index.html')

@rmp.app.route(rmp.app.config['APPLICATION_ROOT'] + 'static/<path:filename>')
def client_static(filename):
    """Display /static/<path:filename> route."""
    return flask.send_from_directory(
        rmp.app.config['STATIC_FOLDER'], filename)
