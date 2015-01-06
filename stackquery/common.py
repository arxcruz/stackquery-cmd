from prettytable import PrettyTable
import ConfigParser
import os
import stackalytics
import stackquery.table as table
from collections import OrderedDict

DEFAULTS = OrderedDict([
    ('project_type', 'openstack'),
    ('releases', 'all'),
    ('company', 'Red Hat'),
    ('metric', 'commits'),
])


class User(object):

    def __init__(self, user_id, user_info):

        if not user_info:
            user_info = {}

        self.commit_count = int(user_info.get('commit_count', 0))
        self.loc = int(user_info.get('loc', 0))
        self.change_request_count = int(user_info.get('change_request_count',
                                                      0))
        self.patch_set_count = int(user_info.get('patch_set_count', 0))
        self.marks = user_info.get('marks', '')
        self.drafted_blueprint_count = int(user_info.get
                                           ('drafted_blueprint_count', 0))
        self.completed_blueprint_count = int(user_info.get
                                             ('completed_blueprint_count', 0))
        self.filed_bug_count = int(user_info.get('filed_bug_count', 0))
        self.resolved_bug_count = int(user_info.get('resolved_bug_count', 0))
        self.email_count = int(user_info.get('email_count', 0))
        self.user = user_id

    def to_list(self):
        list_attributes = []
        for key in table.table_normal_columns.keys():
            list_attributes.append(getattr(self, key))

        return list_attributes

    @property
    def marks(self):
        return self._marks

    @marks.setter
    def marks(self, value):
        if type(value) == type(dict()):
            self._marks = ''
            for key in value:
                self._marks += "%s: %s\n" % (key, value[key])
            self._marks += '\n'
        elif type(value) == str:
            self._marks = value
        else:
            raise ValueError


class Release(object):

    def __init__(self, release_name, parameters, users=list()):
        self.release_name = release_name
        self.parameters = parameters
        self.stack_users = []
        self.users = None
        self.obj_users = None
        if users:
            self.load_users()

    def load_users(self):
        user_list = []
        if self.users:
            for user in self.users:
                self.parameters['user_id'] = user
                self.parameters['release'] = self.release_name
                _user_info = stackalytics.get_stats(self.parameters)
                if _user_info:
                    usr = User(user, _user_info['contribution'])
                    user_list.append(usr)

        self.obj_users = user_list

    def get_total_metrics(self, metric):

        value = 0
        for user in self.obj_users:
            value += int(getattr(user, metric))

        return value

    def get_total_all_metrics(self, metrics):

        total = 0
        for metric in metrics:
            total += self.get_total_metrics(metric)

        return total


class Team(object):

    def __init__(self, team_name, project_type='openstack',
                 company='Red Hat', metric='commits', module=None):
        self.team_name = team_name
        self._users = [None]
        self.project_type = project_type
        self.company = company
        self.metric = metric
        self._releases = dict()
        self.columns = ['user', 'commit_count', 'loc', 'change_request_count',
                        'patch_set_count', 'marks', 'drafted_blueprint_count',
                        'completed_blueprint_count', 'filed_bug_count',
                        'resolved_bug_count', 'email_count']

        self.module = None

    @property
    def releases(self):
        return self._releases

    @releases.setter
    def releases(self, value):
        if type(value) == type(list()):
            for key in value:
                self._releases[key] = Release(key, self.get_parameters(),
                                              self.users)
        elif type(value) == str:
            for release in value.split(','):
                self._releases[release] = Release(release,
                                                  self.get_parameters(),
                                                  self.users)
        else:
            raise ValueError

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, value):
        if type(value) == type(list()):
            self._users = value
        elif type(value) == str:
            self._users = value.split(',')
        else:
            raise ValueError

        if self._releases:
            for release in self._releases:
                self._releases[release].users = self._users
                self._releases[release].load_users()

    def get_parameters(self):
        parameters = {
            'project_type': self.project_type,
            'company': self.company,
            'metric': self.metric
        }

        if self.module:
            parameters['module'] = self.module

        return parameters

    def __str__(self):
        return self.team_name


def load_teams_from_config(config, args=None):
    teams = []

    # We always will have a default team
    team = Team('DEFAULT')
    teams.append(team)

    if config:
        if config.has_section('DEFAULT'):
            items = dict(config.items('DEFAULT'))
            for key in items.keys():
                if getattr(team, key) or \
                   type(getattr(team, key)) == type(dict()):
                    setattr(team, key, items[key])

        for section in config.sections():
            items = dict(config.items(section))
            team = Team(section)
            for key in items.keys():
                if getattr(team, key) or \
                   type(getattr(team, key)) == type(dict()):
                    setattr(team, key, items[key])

            teams.append(team)

    if args:
        for team in teams:
            if args.project_type:
                team.project_type = args.project_type
            if args.release:
                team.releases = args.release
            if args.company:
                team.company = args.company
            if args.module:
                team.module = args.module
            if args.users:
                team.users = args.users

    return teams


def load_config_file(configfile):

    if not configfile:
        return None

    if not os.path.isfile(configfile):
        raise Exception("No such file '%s'" % configfile)

    config = ConfigParser.ConfigParser(DEFAULTS, dict_type=OrderedDict)
    config.read(configfile)

    return config