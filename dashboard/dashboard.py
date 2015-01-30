from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash

import stackquery.common as common
from database import db_session
from models import Team
from models import User
from forms import UserForm

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


@dashboard.route('/users/', methods=['GET', 'POST'])
def dashboard_users():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user = User()
        user.name = user_name
        db_session.add(user)
        db_session.commit()

    users = User.query.all()
    return render_template('list_users.html', users=users)

@dashboard.route('/users/create/', methods=['GET', 'POST'])
def dashboard_create_user():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.user_id = form.user_id.data
        user.name = form.name.data
        user.email = form.email.data
        db_session.add(user)
        db_session.commit()
        flash('User created successfully')
    return render_template('create_user.html', form=form)