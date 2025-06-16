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

import attr


@attr.s()
class Resource:
    path = attr.ib(default=None, repr=False)
    name = attr.ib(default=None, repr=False)
    extension = attr.ib(default=None, repr=False)
    mime_type = attr.ib(default=None, repr=False)
    file_type = attr.ib(default=None, repr=False)
    type = attr.ib(default=None, repr=False)
    programming_language = attr.ib(default=None, repr=False)

    analysis_priority = attr.ib(default=None, repr=False)
    file_category = attr.ib(default=None, repr=False)
    file_subcategory = attr.ib(default=None, repr=False)
    category_notes = attr.ib(default=None, repr=False)
    rule_applied = attr.ib(default=None, repr=False)
    # input_dict will hold all columns/values from input file for use in creating output file
    input_dict = attr.ib(default=None, repr=False)

    @classmethod
    def from_dict(cls, result):
        return cls(
            path=result.get('path', ''),
            name=result.get('name', ''),
            extension=result.get('extension', ''),
            mime_type=result.get('mime_type', ''),
            file_type=result.get('file_type', ''),
            type=result.get('type', ''),
            programming_language=result.get('programming_language', ''),
            # get the full XLSX dict
            input_dict=result
        )

    def to_dict(self):
        # Except for 'input_dict', which is not an XLSX column, field names
        # must match XLSX column names defined above as class attributes,
        # otherwise will throw error In 3 cat-related fields, replace None
        # value with empty string to avoid openpyxl errors
        resource_dict = {
            'path': self.path,
            'name': self.name,
            'extension': self.extension,
            'mime_type': self.mime_type,
            'file_type': self.file_type,
            'type': self.type,
            'programming_language': self.programming_language,
            'analysis_priority': self.analysis_priority if self.analysis_priority is not None else '',
            'file_category': self.file_category if self.file_category is not None else '',
            'file_subcategory': self.file_subcategory if self.file_subcategory is not None else ''
        }
        for k, v in self.input_dict.items():
            if k not in resource_dict:
                resource_dict[k] = v
        return resource_dict
