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

from utilitycode import analyze_debian_status

from commoncode.testcase import FileBasedTesting
import os


class TestAnalyzeDebianStatus(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_parse_status(self):
        input = self.get_test_loc('debian_status/status')
        output = analyze_debian_status.parse_status(input)
        expected = [{'package': '0trace', 'status': 'install ok installed', 'priority': 'optional', 'section': 'net',
                     'installed-size': '43', 'maintainer': 'Kali Developers <devel@kali.org>', 'architecture': 'amd64',
                     'version': '0.01-3kali1', 'depends': 'libc6 (>= 2.7), tcpdump',
                     'description': 'A traceroute tool that can run within an existing TCP connection.\n 0trace is traceroute tool that can be run within an existing, open TCP connection,\n therefore bypassing some types of stateful packet filters with ease.', 'homepage': 'http://lcamtuf.coredump.cx'},
                    {'package': '4kvideodownloader', 'status': 'install ok installed', 'priority': 'optional', 'section': 'web', 'installed-size': '67324',
                     'maintainer': '4KDownload <support@4kdownload.com>', 'architecture': 'amd64', 'version': '4.4-10', 'depends': 'libc6, libstdc++6',
                     'description': 'Download online video\n 4K Video Downloader allows to download video and audio\n content from YouTube and other services in the high \n quality as fast as possible and to save this video on \n your computer.'}]
        assert expected == output
