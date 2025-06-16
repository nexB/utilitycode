# ============================================================================
#  Copyright (c) nexB Inc. http://www.nexb.com/ - All rights reserved.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  SPDX-License-Identifier: Apache-2.0
# ============================================================================

from __future__ import absolute_import, print_function

from utilitycode import debian_copyright_parser

from commoncode.testcase import FileBasedTesting
import os


class TestDebianCopyrightParser(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_get_copyright_files(self):
        input = self.get_test_loc('debian_copyright')
        output = debian_copyright_parser.get_copyright_files(input)
        expected = [os.path.join(input, 'copyright')]
        assert expected == output

    def test_parse_copyright(self):
        input = os.path.join(self.get_test_loc(
            'debian_copyright'), 'copyright')
        data_list, header = debian_copyright_parser.parse_copyright(input)
        expected_header = ['files', 'copyright', 'license', 'comment']
        expected_data_list = [{'files': '*',
                               'copyright': '1998 John Doe <jdoe@example.com>\n           1998 Jane Smith <jsmith@example.net>',
                               'license': 'GPL-2+', 'comment': 'This is a test comment.'}]
        assert expected_header == header
        assert expected_data_list == data_list
