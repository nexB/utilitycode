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
from utilitycode import collect_binary_strings


class TestCollectBinaryStrings(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_collect_binary_strings(self):
        test_file = self.get_test_loc('binary/libaprutil-1.so.0.0.0')
        result = collect_binary_strings.strings(test_file)
        subset_of_strings_command = [
            '_DYNAMIC',
            '_GLOBAL_OFFSET_TABLE_',
            '__gmon_start__',
            '_fini',
            '_SDA_BASE_',
            '_SDA2_BASE_',
            '__cxa_finalize',
            '_Jv_RegisterClasses',
            'apr_brigade_cleanup',
            'apr_brigade_destroy',
            'apr_pool_cleanup_kill',
            'apr_pool_cleanup_null',
            'apr_brigade_create'
        ]

        assert set(subset_of_strings_command).issubset(set(result))
