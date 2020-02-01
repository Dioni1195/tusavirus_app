#!/usr/bin/python3
"""This module starts flask application for states """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, render_template
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """ Return status of the APP as OK """
    states_list = []
    for state in storage.all('State').values():
        states_list.append(state.to_dict())
    return render_template('states.html', states=states_list, victims=storage.count())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """ Return status of the APP as OK """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'victims' not in data:
        abort(400, 'Missing victims')
    #Only receives values of type int
    if type(data['victims']) is int:
        new_state = State(**data)
        new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states_id(state_id):
    """ Return status of the APP as OK """
    catch_state = storage.get('State', state_id)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'victims' not in data:
        abort(400, 'Missing victims')
    if catch_state is None:
        #If the object doesnt exists, create it
        """DUDAS A ESTE PUNTO, ES NECESARIO CREAR EL STATE O YA VA A ESTAR CREADO"""
        if type(data['victims']) is int:
            new_state = State(**data)
            new_state.save()
        else:
            new_state = {}
        return jsonify(new_state.to_dict()), 201
        """HASTA ACA"""
    #If the object exists, update it
    setattr(catch_state, 'victims', data['victims'])
    storage.save()
    return jsonify(catch_state.to_dict()), 200
