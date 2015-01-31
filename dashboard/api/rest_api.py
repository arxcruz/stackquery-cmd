from flask import Blueprint
from flask import request
from flask import jsonify

from database import db_session
from models import Release
from models import Team
from models import User

import simplejson as json

rest_api = Blueprint('rest_api', __name__)


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


@rest_api.route('/api/releases/')
def get_releases():
    releases = Release.query.all()
    return json.dumps(list(releases), default=date_handler)


@rest_api.route('/api/teams/')
def get_teams():
    teams = Team.query.all()
    return json.dumps(list(teams), default=date_handler)


@rest_api.route('/api/users/')
def get_users():
    users = User.query.all()
    return json.dumps(list(users), default=date_handler)

@rest_api.route('/api/users/<int:user_id>/delete/', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        request = jsonify({'status': 'Not Found'})
        request.status = 404
        return request

    db_session.delete(user)
    db_session.commit()
    return jsonify({'status': 'OK'})


