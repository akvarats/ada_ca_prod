from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from run import app

from ada_platform.auth import region_identity
from tokens import get_region_identity_for_token


@app.route("/auth", methods=["GET", "POST"])
def auth():
    """ Проверяет токен доступа """

    token = request.args.get("token") if request.method == "GET" else (request.json or {}).get("token")

    if not token:
        return dict(success=False, error="no-token")

    result = dict(success=False, error="invalid-token")

    region_identity = get_region_identity_for_token(token)
    if region_identity:
        result = dict(success=True, data=dict(jwt_token=create_access_token(region_identity)))

    return jsonify(result)

