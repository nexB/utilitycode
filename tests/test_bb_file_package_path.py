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

import os


from commoncode.testcase import FileBasedTesting
from utilitycode import bb_file_package_path
from utilitycode.utils import to_posix


class TestAnalyze3PPKTV(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_get_package_file(self):
        expected = ['/buildhistory/logger/logger/files-in-package.txt',
                    '/buildhistory/zlib/zlib/files-in-package.txt']
        location = self.get_test_loc('bitbake')
        result = bb_file_package_path.get_package_file(location)
        assert len(result) == 2
        for path in result:
            assert to_posix(path.partition(location)[2]) in expected

    def test_get_package_path_data(self):
        location = self.get_test_loc('bitbake')
        test_file = [self.get_test_loc(
            'bitbake/buildhistory/logger/logger/files-in-package.txt')]
        expected = [{'Resource': 'buildhistory/logger/logger/files-in-package.txt',
                     'installed_path': ['./lib/liblogger_ldplugin.so', './usr/sbin/logger'],
                     'Package': 'logger'}]
        result = bb_file_package_path.get_package_path_data(
            test_file, location)
