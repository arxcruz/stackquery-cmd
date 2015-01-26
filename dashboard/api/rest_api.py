from flask import Blueprint
from flask import jsonify
from models import Release

rest_api = Blueprint('rest_api', __name__)


@rest_api.route('/api/releases/')
def get_releases():
    releases = Release.query.all()
    return jsonify(json_list=[i.serialize for i in releases])