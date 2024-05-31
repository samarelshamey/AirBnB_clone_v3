#!/usr/bin/python3
"""Cities"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """retrieves all City"""
    city_list = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_dict())
    return jsonify(city_list)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """create city route"""
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_dict())
    resp.status_code = 201
    return resp


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """gets a specific City object by ID"""
    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """updates specific City object"""
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """deletes City by id"""

    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
