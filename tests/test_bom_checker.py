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


class TestBomChecker(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    """
    FIXME: This is not a correct approach. The test need to be rewritten.

    def test_check_potential_redirected_url(self):
        input = 'https://www.ibmbigdatahub.com/infographic/four-vs-big-data'
        redirected_output = 'https://www.ibm.com/blog/'

        assert bom_checker.check_potential_redirected_url(input) == redirected_output
    """
