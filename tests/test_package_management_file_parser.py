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

import csv
import json
import os

from commoncode.testcase import FileBasedTesting
from utilitycode import package_management_file_parser


def read_csv(filename):
    with open(filename, encoding='utf-8') as f:
        file_data = csv.reader(f)
        headers = next(file_data)
        return [dict(zip(headers, i)) for i in file_data]


class TestPMFParser(FileBasedTesting):

    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_get_package_management_files(self):
        test_data_dir = self.get_test_loc('package_management_files/')
        pmf_list = package_management_file_parser.get_management_files(
            test_data_dir)
        assert len(pmf_list) == 13

    def test_get_ylock_name_version(self):
        test_data_file = self.get_test_loc(
            'package_management_files/yarn.lock')
        expected = [['@babel/code-frame', '7.0.0'],
                    ['@babel/highlight', '7.0.0'],
                    ['postgres-array', '2.0.0'],
                    ['private-sample', '0.0.0-use.local']]
        output = package_management_file_parser.get_ylock_name_version(
            test_data_file)
        print(output)
        assert output == expected

    def test_gosum_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/go.sum')
        package_list, error = package_management_file_parser.gosum_process(
            test_data_file)
        assert len(error) == 0
        expected_file = self.get_test_loc(
            'package_management_files/expected_go_sum-parsed.csv')
        expected = read_csv(expected_file)
        for index, package in enumerate(package_list):
            expected_dict = expected[index]
            for key in package.keys():
                if not key == 'Resource':
                    if package[key]:
                        assert package[key] == expected_dict[key]

    def test_pubspec_lock_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/pubspec.lock')
        extract_pubspec_data_list = package_management_file_parser.pubspec_lock_process(
            test_data_file)
        expected = [{'Resource': '', 'package__type': 'dart', 'package__name': 'archive', 'package__version': 'v 2.0.10',
                     'package__description': 'Provides encoders and decoders for various archive and compression formats such as zip, tar, bzip2, gzip, and zlib.',
                     'package__homepage_url': 'https://github.com/brendan-duncan/archive', 'package__download_url': 'https://pub.dev/api/archives/archive-2.0.10.tar.gz',
                     'package__owner': 'Brendan Duncan <brendanduncan@gmail.com>', 'package__sha256': '61d02a97dcf6fe3b8057da48670bec4bde35d4fbe7b3379c28820cfd342e2f08',
                     'package__release_date': '2019-06-12T06:40:19.858017Z', 'package__declared_license': 'MIT'},
                    {'Resource': '', 'package__type': 'dart', 'package__name': 'args', 'package__version': 'v 1.5.2',
                     'package__description': 'Library for defining parsers for parsing raw command-line arguments into a set of options and values using GNU and POSIX style options.',
                     'package__homepage_url': 'https://github.com/dart-lang/args', 'package__download_url': 'https://pub.dev/api/archives/args-1.5.2.tar.gz',
                     'package__owner': 'Dart Team <misc@dartlang.org>', 'package__sha256': '0667732e815f02b7dc9006eee523948adb88b6ab691b90f97893b0d53f7674f0',
                     'package__release_date': '2019-05-31T17:21:34.216938Z', 'package__declared_license': 'BSD-3-Clause'}]
        for index, package in enumerate(extract_pubspec_data_list):
            for key in package.keys():
                if not key == 'Resource':
                    assert package[key] == expected[index][key]

    def test_pipfile_lock_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/Pipfile.lock')
        extract_pipfile_data_list = package_management_file_parser.pipfile_lock_process(
            test_data_file)
        expected = [{'Resource': '', 'package__type': 'pypi', 'package__name': 'certifi', 'package__version': 'v 2022.12.7',
                     'package__homepage_url': 'https://github.com/certifi/python-certifi', 'package__download_url': '',
                     'package__owner': 'Kenneth Reitz', 'package__declared_license': 'MPL-2.0'},
                    {'Resource': '', 'package__type': 'pypi', 'package__name': 'chardet', 'package__version': 'v 3.0.4',
                     'package__homepage_url': 'https://github.com/chardet/chardet', 'package__download_url': '',
                     'package__owner': 'Daniel Blanchard', 'package__declared_license': 'LGPL'}
                    ]
        for index, package in enumerate(extract_pipfile_data_list):
            for key in package.keys():
                if not key == 'Resource':
                    assert package[key] == expected[index][key]

    def test_requirements_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/requirements.txt')
        extract_requirements_data_list = package_management_file_parser.requirements_process(
            test_data_file)
        expected = [{'Resource': '', 'package__type': 'pypi', 'package__name': 'contourpy', 'package__version': 'v 1.0.6',
                     'package__homepage_url': 'https://github.com/contourpy/contourpy', 'package__download_url': '',
                     'package__owner': 'Ian Thomas', 'package__declared_license': 'BSD-3-Clause'},
                    {'Resource': '', 'package__type': 'pypi', 'package__name': 'cycler', 'package__version': 'v 0.11.0',
                     'package__homepage_url': 'https://github.com/matplotlib/cycler', 'package__download_url': '',
                     'package__owner': 'Thomas A Caswell', 'package__declared_license': 'BSD'}
                    ]
        for index, package in enumerate(extract_requirements_data_list):
            for key in package.keys():
                if not key == 'Resource':
                    assert package[key] == expected[index][key]

    def test_podfile_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/Podfile.lock')
        extract_podfile_data_list = package_management_file_parser.podfile_process(
            test_data_file)
        expected = [{'Resource': '', 'package__type': 'cocoapods', 'package__name': 'LemonUninstaller', 'package__version': 'v 0.1.0'},
                    {'Resource': '', 'package__type': 'cocoapods', 'package__name': 'Masonry',
                     'package__version': 'v 1.1.0', 'package__primary_language': 'Objective C',
                     'package__declared_license': 'MIT', 'package__copyright': 'Jonas Budelmann, Robert Payne',
                     'package__homepage_url': 'https://github.com/cloudkite/Masonry'}]
        for index, package in enumerate(extract_podfile_data_list):
            for key in package.keys():
                if not key == 'Resource':
                    assert package[key] == expected[index][key]

    def test_opk_contol_file_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/6in4.control')
        opk_contol_file_list = package_management_file_parser.opk_contol_file_process(
            test_data_file)
        expected = [{'Resource': '', 'package__type': 'OpenWRT', 'package__name': '6in4',
                     'package__version': 'v 28', 'package__source_location': 'package/network/ipv6/6in4',
                     'package__declared_license': 'GPL-2.0', 'package__copyright': 'Jo-Philipp Wich <jo@mein.io>',
                     'package__size': '1706', 'package__description': 'Provides support for 6in4 tunnels in /etc/config/network. Refer to http://wiki.openwrt.org/doc/uci/network for configuration details.'}]
        for index, package in enumerate(opk_contol_file_list):
            for key in package.keys():
                if not key == 'Resource':
                    assert package[key] == expected[index][key]

    def test_extract_go_sum_data(self):
        test_data_file = self.get_test_loc(
            'package_management_files/go.sum')
        gosum_package_list, errors = package_management_file_parser.extract_go_sum_data(
            test_data_file)
        expected = [{'Resource': '', 'package__homepage_url': 'github.com/chromedp/chromedp', 'package__version': 'v 0.9.1', 'package__owner': 'chromedp', 'package__name': 'chromedp'},
                    {'Resource': '', 'package__homepage_url': 'golang.org/x/xerrors', 'package__version':
                        'v 0.0.0-20191204190536-9bdfabe68543', 'package__name': 'xerrors', 'package__owner': ''},
                    {'Resource': 'C:\\go.sum', 'package__homepage_url': 'google.golang.org/appengine', 'package__version': 'v 1.6.7', 'package__name': 'appengine', 'package__owner': ''}]
        for index, package in enumerate(gosum_package_list):
            for key in package.keys():
                if not key == 'Resource':
                    assert package[key] == expected[index][key]

    def test_glock_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/Gemfile.lock')
        package_list = package_management_file_parser.glock_process(
            test_data_file)
        expected_file = self.get_test_loc(
            'package_management_files/expected_gem_lock-parsed.csv')
        expected = read_csv(expected_file)
        index = 0
        for package in package_list:
            expected_dict = expected[index]
            for key in package.keys():
                if not key == 'Resource':
                    if package[key]:
                        assert package[key] == expected_dict[key]
            index = index + 1

    def test_plock_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/package-lock.json')
        package_list = package_management_file_parser.plock_process(
            test_data_file)
        expected_file = self.get_test_loc(
            'package_management_files/expected_package_lock-parsed.csv')
        expected = read_csv(expected_file)
        index = 0
        for package in package_list:
            expected_dict = expected[index]
            for key in package.keys():
                if not key == 'path':
                    if package[key]:
                        assert package[key] == expected_dict[key]
            index = index + 1

    def test_plock_process_no_dev(self):
        test_data_file = self.get_test_loc(
            'package_management_files/package-lock.json')
        no_dev = True
        package_list = package_management_file_parser.plock_process(
            test_data_file, no_dev)
        expected_file = self.get_test_loc(
            'package_management_files/expected_package_lock-parsed-no_dev.csv')
        expected = read_csv(expected_file)
        index = 0
        for package in package_list:
            expected_dict = expected[index]
            for key in package.keys():
                if not key == 'path':
                    if package[key]:
                        assert package[key] == expected_dict[key]
            index = index + 1

    def test_ylock_process(self):
        test_data_file = self.get_test_loc(
            'package_management_files/yarn.lock')
        package_list = package_management_file_parser.ylock_process(
            test_data_file)
        expected_file = self.get_test_loc(
            'package_management_files/expected_yarn_lock-parsed.csv')
        expected = read_csv(expected_file)
        index = 0
        for package in package_list:
            expected_dict = expected[index]
            for key in package.keys():
                if not key == 'path':
                    if package[key]:
                        assert package[key] == expected_dict[key]
            index = index + 1

    def test_update_package_with_data(self):
        test_package = package_management_file_parser.LockPackage(
            'debug', '3.1.0')
        test_data_file = self.get_test_loc(
            'package_management_files/debug-3.1.0.json')
        with open(test_data_file) as f:
            test_data = json.load(f)

        package_management_file_parser.update_package_with_data(
            test_package, test_data)

        assert test_package.tk_package.name == 'debug'
        assert test_package.tk_package.version == '3.1.0'
        assert test_package.tk_package.declared_license_expression == 'mit'

    def test_package_LockPackage_api_url(self):
        test_name = 'node'
        test_version = '0.0.0'

        result = package_management_file_parser.LockPackage(
            test_name, test_version).api_url_plock()

        assert result == 'https://registry.npmjs.org/node/0.0.0'

    def test_create_packages(self):
        test_deps = {
            "browser-stdout": {
                "version": "1.3.1",
                "resolved": "https://registry.npmjs.org/browser-stdout/-/browser-stdout-1.3.1.tgz",
                "integrity": "sha512-qhAVI1+Av2X7qelOfAIYwXONood6XlZE/fXaBSmW/T5SzLAmCgzi+eiWE7fUvbHaeNBQH13UftjpXxsfLkMpgw==",
                "dev": True
            },
            "commander": {
                "version": "2.15.1",
                "resolved": "https://registry.npmjs.org/commander/-/commander-2.15.1.tgz",
                "integrity": "sha512-VlfT9F3V0v+jr4yxPc5gg9s62/fIVWsd2Bk2iD435um1NlGMYdVCq+MjcXnhYq2icNOizHr1kK+5TI6H0Hy0ag==",
            },
        }

        result = list(
            package_management_file_parser.create_plock_packages(test_deps))

        assert result[0].name == 'browser-stdout'
        assert result[0].version == '1.3.1'
        assert result[0].dev == True

        assert result[1].name == 'commander'
        assert result[1].version == '2.15.1'
        assert result[1].dev == False
