from flask import Blueprint
from flask import render_template
from flask import request

import stackquery.common as common
from models import Team

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/', methods=['GET', 'POST'])
def dashboard_index():
    if request.method == 'POST':
        release = request.form.get('release')
        project_type = request.form.get('project_type')
        users = common.get_status_from_users(['arxcruz', 'david-kranz'],
                                             'Red Hat',
                                             project_type, release)
        return render_template('index.html', users=users)
    else:
        return render_template('index.html')


@dashboard.route('/teams/')
def dashboard_teams():
    teams = Team.query.all()
    return render_template('list_teams.html', teams=teams)