# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_server_set_metadata
----------------------------------

Tests for the `set_server_metadata` command.
"""

import mock

from shade import OpenStackCloud
from shade.exc import OpenStackCloudException
from shade.tests.unit import base


class TestServerSetMetadata(base.TestCase):

    @mock.patch.object(OpenStackCloud, 'nova_client')
    def test_server_set_metadata_with_set_meta_exception(self, mock_nova):
        """
        Test that a generic exception in the novaclient set_meta raises
        an exception in set_server_metadata.
        """
        mock_nova.servers.set_meta.side_effect = Exception("exception")

        self.assertRaises(
            OpenStackCloudException, self.cloud.set_server_metadata,
            {'id': 'server-id'}, {'meta': 'data'})

    @mock.patch.object(OpenStackCloud, 'nova_client')
    def test_server_set_metadata_with_exception_reraise(self, mock_nova):
        """
        Test that an OpenStackCloudException exception gets re-raised
        in set_server_metadata.
        """
        mock_nova.servers.set_meta.side_effect = OpenStackCloudException("")

        self.assertRaises(
            OpenStackCloudException, self.cloud.set_server_metadata,
            'server-id', {'meta': 'data'})
