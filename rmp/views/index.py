"""RMP index view."""
import flask
import rmp
import rmp.model
import random


@rmp.app.route(rmp.app.config['APPLICATION_ROOT'], methods=['GET', 'POST'])
def index():
    """Display / route."""
    return flask.render_template('index.html')


@rmp.app.route(rmp.app.config[
                        'APPLICATION_ROOT'] + 'hello')  # take note of this decorator syntax, it's a common pattern
def hello():
    # It is good practice to only call a function in your route end-point,
    # rather than have actual implementation code here.
    # This allows for easier unit and integration testing of your functions.
    return get_hello()


def get_hello():
    greeting_list = ['Ciao', 'Hei', 'Salut', 'Hola', 'Hallo', 'Hej']
    return random.choice(greeting_list)
