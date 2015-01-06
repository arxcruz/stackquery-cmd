Stackquery
==========

Stackquery is a python script which gather information from [Stackalytics](stackalytics.com) website through their REST API.

The code to get the user information comes from [Martina Kollarova launchpadstats](https://github.com/mkollaro/launchpadstats) script.

Basically, it does the same, except that I'm using prettytable to render the table containing all the information, and some css to make it more cute.

This is a great script for keep track of what your team are doing in [OpenStack](www.openstack.org)

The script isn't perfect, and I'm using to improve my python skills, so expect a lot of errors and bad code practices.
 
Examples of usage
=================

Using a config file
-------------------

You can use a config file with the following content:

TODO: add config file content

Using config file (you need to have a list of users option in the DEFAULT
section):

stackquery --config config.ini

Others command line examples
----------------------------

##### Using config file and list of users: #####

stackquery --config config.ini --engineer=arxcruz

##### Without config file: #####

    stackquery --engineer=arxcruz

##### Using config file and a team:#####

    stackquery --config config.ini --team=qe

##### Generating output in html: #####
    stackquery --config config.ini --team=qe --html

##### Showing metrics only: #####
    stackquery --config config.ini --team=qe --metric

##### Showing metrics and results per release #####
    stackquery --config config.ini --team=qe --all