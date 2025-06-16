#!/usr/bin/env python
# -*- coding: utf8 -*-

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

from collections import defaultdict

from tempfile import NamedTemporaryFile
import gzip
import os
import pickle

import click
import requests
import unicodecsv

from commoncode.fileutils import create_dir


VERSION = '0.0.1'


# TODO: make a smaller Content file for testing
# TODO: use fetchcode
# TODO: have options to make queries to index
@click.command()
@click.argument('location', type=click.Path(exists=True, readable=True))
@click.argument('destination', type=click.Path(exists=False), required=True)
@click.option('--reindex', is_flag=True, help='Recreate the system package files index before matching.')
@click.option('--contents-file', multiple=True, help='Create index from a specified Contents-<arch>.gz file. '
                                                     'Multiple Contents files can be specified and they will be combined into a single index.')
@click.option('--index-file', help='Specify an index file to use for matching. This option is only used for testing purposes.')
@click.help_option('-h', '--help')
def cli(location, destination, reindex=False, contents_file=[], index_file=''):
    """
    Match file paths to Linux system packages.

    LOCATION is the path to a CSV with one column named `Resource` that contains the paths to be matched.

    DESTINATION is the path where the match results are to be saved as CSV.
    """
    # Create or load index
    index_directory = get_index_directory()
    if index_file:
        index_path = index_file
    else:
        index_path = os.path.join(index_directory, 'index-file')

    if reindex or contents_file or not os.path.exists(index_path):
        packages_by_path = create_index(contents_file)
        save_index(packages_by_path, index_path)
    else:
        packages_by_path = load_index(index_path)

    # Collect paths to match on from `location`
    paths = []
    with open(location, 'rb') as f:
        r = unicodecsv.DictReader(f)
        for row in r:
            path = row.get('Resource')
            if not path:
                raise Exception('Input CSV does not have a Resource column')
            paths.append(path)

    # Perform matching process and write results to `destination`
    results = [match.to_dict() for match in get_matches(paths, packages_by_path)]
    with open(destination, 'wb') as f:
        w = unicodecsv.DictWriter(f, ('Resource', 'matched_suffix', 'matched_package'))
        w.writeheader()
        for match in results:
            w.writerow(match)


def get_index_directory():
    """
    Create a directory that will be used to store the index file and return its path
    """
    user_home = os.path.abspath(os.path.expanduser('~'))
    index_directory = os.path.join(user_home, '.cache', 'system-file-index', VERSION)
    create_dir(index_directory)
    return index_directory


def load_index(index_path):
    with open(index_path, 'rb') as f:
        index = pickle.load(f)
    return index


def save_index(index, index_path):
    with open(index_path, 'wb') as f:
        pickle.dump(index, f)


def download_contents_file_from_url(contents_file_url):
    """
    Return the path of a downloaded file from `contents_file_url`
    """
    contents_file_request = requests.get(contents_file_url)
    contents_file = NamedTemporaryFile('wb', suffix='.gz', delete=False)
    contents_file_location = contents_file.name
    contents_file.write(contents_file_request.content)
    contents_file.close()
    return contents_file_location


def parse_contents(location, has_header=True):
    """
    Return a mapping of {path: [list of packages]} and a mapping of
    {package: [list of paths]} from parsing a Debian Contents file at
    ``location``.
    If ``has_header`` is True, the file is expected to have a header narrative
    and a FILE/LOCATION columns headers before the table starts in earnest.
    See https://wiki.debian.org/DebianRepository/Format#A.22Contents.22_indices
    for format details.
    """
    packages_by_path = defaultdict(list)
    paths_by_package = defaultdict(list)
    with gzip.GzipFile(location) as lines:
        if has_header:
            # keep track if we are now in the table proper
            # e.g. after the FILE  LOCATION header
            # this is the case for Ubuntu
            in_table = False
        else:
            # if we have no header (like in Debian) we start right away.
            in_table = True

        for line in lines:
            line = line.decode('utf-8')
            left, _, right = line.strip().rpartition(' ')
            left = left.strip()
            right = right.strip()
            if not in_table:
                # "The first row of the table SHOULD have the columns "FILE" and "LOCATION""
                # This is the spec and used to be TRue for Debian.
                # But nowadays only Ubuntu does this.
                if left == 'FILE' and right == 'LOCATION':
                    in_table = True
            else:
                path = left
                packages = right
                package_names = packages.split(',')
                for archsec_name in package_names:
                    # "A list of qualified package names, separated by comma. A
                    # qualified package name has the form
                    # [[$AREA/]$SECTION/]$NAME, where $AREA is the archive area,
                    # $SECTION the package section, and $NAME the name of the
                    # package."

                    # NOTE: we ignore the arch and section for now
                    archsec, _, package_name = archsec_name.rpartition('/')
                    arch, _, section = archsec.rpartition('/')
                    packages_by_path[path].append(package_name)
                    paths_by_package[package_name].append(path)

    if not in_table:
        raise Exception('Invalid Content files without FILE/LOCATION header.')
    return packages_by_path, paths_by_package


def create_index(contents_files=[]):
    """
    Return a dictionary of paths and their associated Package names that has
    been created from Debian Contents files

    If `contents_files` is not empty, then we create our index from the Contents
    files from `contents_files`

    TODO: have option to process Contents files with headers
    """
    if contents_files:
        indexes = []
        for contents_file in contents_files:
            index, _ = parse_contents(contents_file, has_header=False)
            indexes.append(index)
    else:
        contrib_contents = download_contents_file_from_url('http://ftp.de.debian.org/debian/dists/Debian10.6/contrib/Contents-amd64.gz')
        main_contents = download_contents_file_from_url('http://ftp.de.debian.org/debian/dists/Debian10.6/main/Contents-amd64.gz')
        non_free_contents = download_contents_file_from_url('http://ftp.de.debian.org/debian/dists/Debian10.6/non-free/Contents-amd64.gz')

        contrib_index, _ = parse_contents(contrib_contents, has_header=False)
        main_index, _ = parse_contents(main_contents, has_header=False)
        non_free_index, _ = parse_contents(non_free_contents, has_header=False)

        # Remove downloaded Contents files after we are done parsing them
        os.remove(contrib_contents)
        os.remove(main_contents)
        os.remove(non_free_contents)
        indexes = [contrib_index, main_index, non_free_index]

    # Combine the three packages_by_paths into one
    combined_index = defaultdict(list)
    for index in indexes:
        for path, packages in index.items():
            combined_index[path].extend(packages)

    return combined_index


class Match(object):
    def __init__(self, path, matched_suffix='', matched_package=''):
        self.path = path
        self.matched_suffix = matched_suffix
        self.matched_package = matched_package

    def to_dict(self):
        return dict(
            Resource=self.path,
            matched_suffix=self.matched_suffix,
            matched_package=self.matched_package
        )


def get_matches(paths, packages_by_path):
    """
    Yield a Match object, containing the matched path, matched suffix, and
    package given a list of paths
    """
    for path in paths:
        path_is_matched = False
        # iterate through suffixes until we find a match
        for suffix in path_suffixes(path):
            for package in packages_by_path[suffix]:
                yield Match(path, suffix, package)
                # We stop matching on a path if we have a match result
                path_is_matched = True
            if path_is_matched:
                break
        else:
            # If we do not find a suffix that has a Package match and did not
            # break out of the loop, return an empty Match object
            yield Match(path)


def path_suffixes(path):
    """
    Yield all the suffixes of `path`, starting from the longest (e.g. more segments).

    Do not return a suffix for a single file.
    """
    segments = path.strip('/').split('/')
    # This will give us all the suffixes of `path`, starting from the longest,
    # ignoring the single file case (which is why we subtract 1 in range())
    suffixes = (segments[i:] for i in range(len(segments) - 1))
    for suffix in suffixes:
        yield '/'.join(suffix)
