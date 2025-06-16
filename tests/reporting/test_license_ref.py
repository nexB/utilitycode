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


from commoncode.testcase import FileBasedTesting
from reporting import license_ref


class TestLicenseRef(FileBasedTesting):

    def test_get_license_data(self):
        license_keys = ['apache-2.0', 'bsd-new']
        api_url = ''
        api_key = ''
        result, errors = license_ref.get_license_data(
            license_keys, api_url, api_key)
        expected_result = [['apache-2.0', 'Apache-2.0', 'Permissive', 'https://scancode-licensedb.aboutcode.org/apache-2.0.LICENSE'],
                           ['bsd-new', 'BSD-3-Clause', 'Permissive', 'https://scancode-licensedb.aboutcode.org/bsd-new.LICENSE']]
        assert not errors
        assert result == expected_result
