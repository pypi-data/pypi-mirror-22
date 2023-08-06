"""Freezer swift.py related tests

Copyright 2015 Hewlett-Packard

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import unittest
from mock import Mock, MagicMock, patch
from .common import *

from freezer_api.api import v1
import json


class TestHomedocResource(FreezerBaseTestCase):

    def setUp(self):
        self.resource = v1.homedoc.Resource()
        self.req = MagicMock()
        self.req.__getitem__.side_effect = get_req_items
        super(TestHomedocResource, self).setUp()

    def test_on_get_return_resources_information(self):
        self.resource.on_get(self.req, self.req)
        result = json.loads(self.req.data.decode('utf-8'))
        print("TEST HOME DOC RESULT: {}".format(result))
        expected_result = v1.homedoc.HOME_DOC
        self.assertEquals(result, expected_result)
