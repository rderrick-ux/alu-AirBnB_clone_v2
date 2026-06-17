#!/usr/bin/python3
"""Starts a Flask web application for states and their cities."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """Display states or a specific state with its cities."""
    if state_id is None:
        states = sorted(storage.all(State).values(), key=lambda s: s.name)
        return render_template('9-states.html', states=states)
    else:
        state = storage.all(State).get('State.' + state_id)
        return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
