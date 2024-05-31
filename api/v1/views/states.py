#!/usr/bin/python3
"""states"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_state():
    """retrieves all State objects"""
    state_lst = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_lst.append(obj.to_dict())
    return jsonify(state_lst)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """create state"""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """gets a specific State object by ID"""

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """updates specific State object by ID"""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """deletes State by id"""

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
