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

from utilitycode import debian_package_installed_list

from commoncode.testcase import FileBasedTesting
import os


class TestDebianPackageInstalledList(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_get_package_list(self):
        input = self.get_test_loc('debian_pacakge_md5sums')
        output = debian_package_installed_list.get_package_list(input)
        expected = [os.path.join(input, 'test.md5sums')]
        assert expected == output

    def test_parse_process(self):
        input = self.get_test_loc('debian_pacakge_md5sums')
        test_input = [os.path.join(input, 'test.md5sums')]
        assert os.path.exists(test_input[0])
        output = debian_package_installed_list.parse_process(test_input)
        expected = [{'Resource': 'test.md5sums', 'md5': 'vsgrc68a544asdasdasde836bfd3096f', 'installed_path': 'bin/test1'},
                    {'Resource': 'test.md5sums', 'md5': 'kljglskgjkdekmldfd32c5df13asadac',
                        'installed_path': 'bin/test2'},
                    {'Resource': 'test.md5sums', 'md5': 'aas409a573ceeab897kdfslffwoiejfm', 'installed_path': 'bin/test3'}]
        assert expected == output
