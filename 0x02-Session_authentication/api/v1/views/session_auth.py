#!/usr/bin/env python3

"""
Session Authentication
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if the User doesn't exist
    """
    email = request.form.get("email")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie("session_id", session_id)
    return response
