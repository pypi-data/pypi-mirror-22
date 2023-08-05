"""
Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import unittest

from hqlib.metric_source import Git


class GitUnderTest(Git):  # pylint: disable=too-few-public-methods
    """ Override the Git class to prevent it from running shell commands. """

    def _run_shell_command(self, *args, **kwargs):  # pylint: disable=unused-argument
        return ''


class GitTests(unittest.TestCase):
    """ Unit tests for the Git class. """
    def setUp(self):
        self.__git = GitUnderTest(url='http://git/')

    def test_is_equal(self):
        """ Test that the branch is taken into account for equality. """
        self.assertNotEqual(GitUnderTest(url=self.__git.url(), branch='branch'), self.__git)

    def test_hash(self):
        """ Test that the branch is taken into account for the hash. """
        self.assertNotEqual(hash(GitUnderTest(url=self.__git.url(), branch='branch')), hash(self.__git))

    def test_last_changed_date(self):
        """ Test that there is no last changed date for a missing repo. """
        self.assertEqual(datetime.datetime.min, self.__git.last_changed_date('path'))

    def test_branches(self):
        """ Test that there are no branches by default. """
        self.assertFalse(self.__git.branches('path'))

    def test_unmerged_branches(self):
        """ Test that there are no unmerged branches by default. """
        self.assertEqual({}, self.__git.unmerged_branches('http://git/'))

    def test_normalize_path(self):
        """ Test path that needs no changes. """
        self.assertEqual('http://git/master/', self.__git.normalize_path('http://git/master/'))

    def test_normalize_path_does_not_add_trailing_slash(self):
        """ Test that the normalized path doesn't have a trailing slash. """
        self.assertEqual('http://git/master', self.__git.normalize_path('http://git/master'))

    def test_branch_folder_for_branch(self):
        """ Test that a branch folder can be created from a trunk folder and a branch name. """
        self.assertEqual('http://git/master/branch',
                         self.__git.branch_folder_for_branch('http://git/master', 'branch'))
