#! /usr/bin/env python
# Copyright (c) 2014 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, print_function
import sys
import setuptools
import pip.req
from setuptools.command.test import test as TestCommand

import stackquery

install_reqs = pip.req.parse_requirements('requirements.txt')

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import must be here, because outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setuptools.setup(
    name='stackquery',
    version=stackquery.__version__,
    author='Arx Cruz',
    author_email='acruz@redhat.com',
    url='https://github.com/arxcruz/stackquery',
    packages=['stackquery'],
    license='Apache License, Version 2.0',
    scripts=['bin/stackquery'],
    description='Get Launchpad statistics and create various CSV or HTML'
                ' tables from them.',
#    long_description=long_description,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2'
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        ],
    install_requires=[str(x.req) for x in install_reqs],
    tests_require=['tox>=1.6'],  # tox will take care of the other reqs
    cmdclass={'test': Tox},
)
