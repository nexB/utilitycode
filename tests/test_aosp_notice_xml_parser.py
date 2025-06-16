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
from utilitycode import aosp_notice_xml_parser


class TestAOSPNoticeXMLParser(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_parse_aosp_notice(self):
        test_file = self.get_test_loc('aosp_notice/notice.xml')
        id_reference, id_license = aosp_notice_xml_parser.parse_aosp_notice(
            test_file)
        expected_id = '45d4ee055bdf34776905c04117951798'
        expected_lic = '<file-content contentId="45d4ee055bdf34776905c04117951798"><![CDATA[\n/*-\n * Copyright (c) blah blah\n *\n * This is under a public domain.\n */\n]]></file-content>\n'
        expected_file = '/vendor/bin/blah'

        assert id_license == [{expected_id: expected_lic}]
        assert id_reference == [
            {'contentID': expected_id, 'reference_path': expected_file}]
