from flask import Blueprint
from flask import jsonify
from models import Release
from models import Team

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