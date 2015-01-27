from flask import Blueprint
from flask import jsonify
from models import Release

import simplejson as json

rest_api = Blueprint('rest_api', __name__)


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


@rest_api.route('/api/releases/')
def get_releases():
    releases = Release.query.all()
    return json.dumps(list(releases), default=date_handler)