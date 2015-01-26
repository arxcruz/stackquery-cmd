from flask import Blueprint
from flask import render_template
from flask import request

import stackquery.common as common

dashboard = Blueprint('dashboard', __name__, url_prefix='/')


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
