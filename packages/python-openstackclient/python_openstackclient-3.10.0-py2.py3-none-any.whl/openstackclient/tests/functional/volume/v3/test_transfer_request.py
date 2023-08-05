#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from openstackclient.tests.functional.volume.v2 import test_transfer_request \
    as v2
import os


class TransferRequestTests(v2.TransferRequestTests):
    """Functional tests for transfer request. """

    @classmethod
    def setUpClass(cls):
        super(TransferRequestTests, cls).setUpClass()
        os.environ['OS_VOLUME_API_VERSION'] = '3'
