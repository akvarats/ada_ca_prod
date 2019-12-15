from flask import Flask
from flask_jwt_extended import JWTManager

from ada_platform.docker import get_docker_secret

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask("auth")
app.config['JWT_SECRET_KEY'] = get_docker_secret("jwt_secret_key")
jwt = JWTManager(app)

from views import auth
