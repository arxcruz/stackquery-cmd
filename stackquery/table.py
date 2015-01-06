from collections import OrderedDict
from prettytable import PrettyTable


TABLE_NORMAL = 'Normal'
TABLE_METRIC = 'Metric'

table_normal_columns = OrderedDict([('user', 'User'),
                                    ('commit_count', 'Total commits'),
                                    ('loc', 'Total LOC'),
                                    ('change_request_count',
                                     'Change Requests'),
                                    ('patch_set_count', 'Patch Sets'),
                                    ('marks', 'Marks'),
                                    ('drafted_blueprint_count',
                                     'Draft Blueprints'),
                                    ('completed_blueprint_count',
                                     'Completed Blueprints'),
                                    ('filed_bug_count', 'Filed Bugs'),
                                    ('resolved_bug_count', 'Resolved Bugs'),
                                    ('email_count', 'Emails')])


def _create_table(table_type=TABLE_NORMAL, release_list=None):

    if table_type == TABLE_NORMAL:
        table = PrettyTable()
        for column in table_normal_columns.keys():
            table.add_column(table_normal_columns[column], [])

        # Align the column 'Marks' to left to be more readable
        table.align['Marks'] = 'l'
        return table

    elif table_type == TABLE_METRIC:

        table = PrettyTable()
        table.add_column('Metric / Release', [])

        for release in release_list:
            table.add_column(release.title(), [])

        return table

    return None


def create_and_fill_table(release, html):
    table = _create_table()
    table.align['Marks'] = 'l'
    fill_table(table, TABLE_NORMAL, release, html)

    return table


def create_and_fill_metric_table(team):
    table = _create_table(TABLE_METRIC, [
                          team.releases[release].release_name.title()
                          for release in team.releases])
    fill_table(table, TABLE_METRIC, team.releases)
    table.align['Metric / Release'] = 'l'
    return table


def fill_table(table, table_type, release, html=False):

    if table_type == TABLE_NORMAL:
        for user in release.obj_users:
            user_in_list = user.to_list()
            if html:
                user_in_list[0] = '<a href=http://stackalytics.com/' \
                                  '?user_id=%s&release=%s>%s</a>' % \
                                  (user.user, release.release_name, user.user)
            table.add_row(user_in_list)
    if table_type == TABLE_METRIC:
        rows = ['drafted_blueprint_count', 'completed_blueprint_count',
                'filed_bug_count', 'resolved_bug_count']

        good_names = [table_normal_columns[x] for x in rows]
        good_names.append('Sum')
        rows.append('Sum')
        for row in rows:
            new_row = [row]
            for r in release:
                if row == 'Sum':
                    new_row.append(release[r].get_total_all_metrics(rows[:-1]))
                else:
                    new_row.append(release[r].get_total_metrics(row))
            table.add_row(new_row)


def print_table(team, metric, html=False, all=False):
    tables = []

    if metric or all:
        tbl = create_and_fill_metric_table(team)
        message = "Group summary for the releases %s" % ', '.join(
            [team.releases[r].release_name.title() for r in team.releases])
        tables.append({'message': message, 'table': tbl, 'metric': True})

    if not metric or all:
        for release in team.releases:
            tbl = create_and_fill_table(team.releases[release], html)
            message = "Metrics per user in OpenStack %s" % team.releases[
                release].release_name.title()
            tables.append({'message': message, 'table': tbl, 'metric': False})

    if html:
        output = ''
        output += '<!DOCTYPE html>\n<html>\n'
        output += '<head>\n'
        output += css_table()
        output += '<title>Stackquery results</title>\n'
        output += '</head>\n'

        output += '<h1>Information for team %s</h1>\n' % team.team_name
        for table in tables:
            output += '<h2>%s</h2>\n' % table['message']
            output += '<div class="CSSTableGenerator">'
            if table['metric']:
                output += table['table'].get_html_string(format=True)
            else:
                columns = [table_normal_columns[x] for x in team.columns]
                output += table['table'].get_html_string(format=True,
                                                         fields=columns)
            output += '</div>'

        output += '</html>'
        output = output.replace('&lt;', '<')
        output = output.replace('&gt;', '>')
        output = output.replace('<th', '<td')
        output = output.replace('</th>', '</td>')
        print output

    else:

        print "Information for team %s" % team.team_name.title()

        for table in tables:
            print table['message']
            if table['metric']:
                print table['table'].get_string()
            else:
                print table['table'].get_string(fields=[table_normal_columns[x]
                                                        for x in team.columns])


def css_table():
    return '''
    <style media="screen" type="text/css">
    .CSSTableGenerator {
        margin:0px;padding:0px;
        width:100%; box-shadow: 10px 10px 5px #888888;
        border:1px solid #000000;

        -moz-border-radius-bottomleft:0px;
        -webkit-border-bottom-left-radius:0px;
        border-bottom-left-radius:0px;

        -moz-border-radius-bottomright:0px;
        -webkit-border-bottom-right-radius:0px;
        border-bottom-right-radius:0px;

        -moz-border-radius-topright:0px;
        -webkit-border-top-right-radius:0px;
        border-top-right-radius:0px;

        -moz-border-radius-topleft:0px;
        -webkit-border-top-left-radius:0px;
        border-top-left-radius:0px;
    }
    .CSSTableGenerator table {
        width:100%;
        height:100%;
        margin:0px;padding:0px;
    }
    .CSSTableGenerator tr:last-child td:last-child {
        -moz-border-radius-bottomright:0px;
        -webkit-border-bottom-right-radius:0px;
        border-bottom-right-radius:0px;
    }
    .CSSTableGenerator table tr:first-child td:first-child {
        -moz-border-radius-topleft:0px;
        -webkit-border-top-left-radius:0px;
        border-top-left-radius:0px;
    }
    .CSSTableGenerator table tr:first-child td:last-child {
        -moz-border-radius-topright:0px;
        -webkit-border-top-right-radius:0px;
        border-top-right-radius:0px;
    }
    .CSSTableGenerator tr:last-child td:first-child {
        -moz-border-radius-bottomleft:0px;
        -webkit-border-bottom-left-radius:0px;
        border-bottom-left-radius:0px;
    }
    .CSSTableGenerator tr:hover td {
        background-color:#ffaaaa;
    }
    .CSSTableGenerator td {
        vertical-align:middle;

        background-color:#ffffff;
        border:1px solid #000000;
        border-width:0px 1px 1px 0px;
        text-align:left;
        padding:7px;
        font-size:15px;
        font-family:arial;
        font-weight:normal;
        color:#000000;
    }
    .CSSTableGenerator tr:last-child td {
        border-width:0px 1px 0px 0px;
    }
    .CSSTableGenerator tr td:last-child {
        border-width:0px 0px 1px 0px;
    }
    .CSSTableGenerator tr:last-child td:last-child {
        border-width:0px 0px 0px 0px;
    }
    .CSSTableGenerator tr:first-child td {
        background:-o-linear-gradient(bottom, #ff5656 5%, #7f0000 100%);
        background:-webkit-gradient(linear, left top, left bottom,
            color-stop(0.05, #ff5656), color-stop(1, #7f0000) );
        background:-moz-linear-gradient(center top, #ff5656 5%, #7f0000 100%);
        filter:progid:DXImageTransform.Microsoft.gradient(
            startColorstr="#ff5656", endColorstr="#7f0000");
        background: -o-linear-gradient(top,#ff5656,7f0000);
        background-color:#ff5656;
        border:0px solid #000000;
        text-align:center;
        border-width:0px 0px 1px 1px;
        font-size:14px;
        font-family:arial;
        font-weight:bold;
        color:#ffffff;
    }
    .CSSTableGenerator tr:first-child:hover td {
        background:-o-linear-gradient(bottom, #ff5656 5%, #7f0000 100%);
        background:-webkit-gradient(linear, left top, left bottom,
                                    color-stop(0.05, #ff5656), c
                                    olor-stop(1, #7f0000));
        background:-moz-linear-gradient(center top, #ff5656 5%, #7f0000 100%);
        filter:progid:DXImageTransform.Microsoft.gradient(
            startColorstr="#ff5656", endColorstr="#7f0000");
        background: -o-linear-gradient(top,#ff5656,7f0000);
        background-color:#ff5656;
    }
    .CSSTableGenerator tr:first-child td:first-child {
        border-width:0px 0px 1px 0px;
    }
    .CSSTableGenerator tr:first-child td:last-child {
        border-width:0px 0px 1px 1px;
    }
    </style>
'''