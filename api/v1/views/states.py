#!/usr/bin/python3
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views

state_objects = storage.all(State)


@app_views.route('/states', strict_slashes=False)
def get_states():
    """ Retrieves states from storage
    """
    retrieved_states = []
    for state in state_objects.values():
        retrieved_states.append(state.to_dict())
    return jsonify(retrieved_states), 200


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves one state from sotrage based on the id
    """
    state_id = str(state_id)
    try:
        return jsonify(storage.get(State, state_id).to_dict()), 200
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """ Deletes the state from storage by its given id
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Adds a new state to storage
    """
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort('400', 'Missing name')
    new_state = State(**body)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Modifies the attributes of a state if they are not dates or id
    """
    state = storage.get(State, state_id)
    if state:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
