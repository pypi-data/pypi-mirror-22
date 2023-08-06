# Copyright 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import mock
from oslo_service import loopingcall
from oslotest import base as test_base
import requests

from ironic_python_agent import errors
from ironic_python_agent import hardware
from ironic_python_agent import ironic_api_client

API_URL = 'http://agent-api.ironic.example.org/'
DRIVER = 'agent_ipmitool'


class FakeResponse(object):
    def __init__(self, content=None, status_code=200, headers=None):
        content = content or {}
        self.content = json.dumps(content)
        self.status_code = status_code
        self.headers = headers or {}


class TestBaseIronicPythonAgent(test_base.BaseTestCase):
    def setUp(self):
        super(TestBaseIronicPythonAgent, self).setUp()
        self.api_client = ironic_api_client.APIClient(API_URL, DRIVER)
        self.hardware_info = {
            'interfaces': [
                hardware.NetworkInterface(
                    'eth0', '00:0c:29:8c:11:b1', vendor='0x15b3',
                    product='0x1014'),
                hardware.NetworkInterface(
                    'eth1', '00:0c:29:8c:11:b2',
                    lldp=[(1, '04885a92ec5459'),
                          (2, '0545746865726e6574312f3138')],
                    vendor='0x15b3', product='0x1014'),
            ],
            'cpu': hardware.CPU('Awesome Jay CPU x10 9001', '9001', '10',
                                'ARMv9'),
            'disks': [
                hardware.BlockDevice('/dev/sdj', 'small', '9001', False),
                hardware.BlockDevice('/dev/hdj', 'big', '9002', False),
            ],
            'memory': hardware.Memory(total='8675309',
                                      physical_mb='8675'),
        }

    def test_successful_heartbeat(self):
        response = FakeResponse(status_code=202)

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        self.api_client.heartbeat(
            uuid='deadbeef-dabb-ad00-b105-f00d00bab10c',
            advertise_address=('192.0.2.1', '9999')
        )

        heartbeat_path = 'v1/heartbeat/deadbeef-dabb-ad00-b105-f00d00bab10c'
        request_args = self.api_client.session.request.call_args[0]
        self.assertEqual('POST', request_args[0])
        self.assertEqual(API_URL + heartbeat_path, request_args[1])

    def test_successful_heartbeat_old_api(self):
        response = FakeResponse(status_code=202)

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        self.api_client.use_ramdisk_api = False
        self.api_client.heartbeat(
            uuid='deadbeef-dabb-ad00-b105-f00d00bab10c',
            advertise_address=('192.0.2.1', '9999')
        )

        heartbeat_path = ('v1/nodes/deadbeef-dabb-ad00-b105-f00d00bab10c/'
                          'vendor_passthru/heartbeat')
        request_args = self.api_client.session.request.call_args[0]
        self.assertEqual('POST', request_args[0])
        self.assertEqual(API_URL + heartbeat_path, request_args[1])

    def test_heartbeat_requests_exception(self):
        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.side_effect = Exception('api is down!')

        self.assertRaises(errors.HeartbeatError,
                          self.api_client.heartbeat,
                          uuid='deadbeef-dabb-ad00-b105-f00d00bab10c',
                          advertise_address=('192.0.2.1', '9999'))

    def test_heartbeat_invalid_status_code(self):
        response = FakeResponse(status_code=404)
        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        self.assertRaises(errors.HeartbeatError,
                          self.api_client.heartbeat,
                          uuid='deadbeef-dabb-ad00-b105-f00d00bab10c',
                          advertise_address=('192.0.2.1', '9999'))

    def test_heartbeat_409_status_code(self):
        response = FakeResponse(status_code=409)
        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        self.assertRaises(errors.HeartbeatConflictError,
                          self.api_client.heartbeat,
                          uuid='deadbeef-dabb-ad00-b105-f00d00bab10c',
                          advertise_address=('192.0.2.1', '9999'))

    @mock.patch('eventlet.greenthread.sleep')
    @mock.patch('ironic_python_agent.ironic_api_client.APIClient._do_lookup')
    def test_lookup_node(self, lookup_mock, sleep_mock):
        content = {
            'node': {
                'uuid': 'deadbeef-dabb-ad00-b105-f00d00bab10c'
            },
            'config': {
                'heartbeat_timeout': 300
            }
        }
        lookup_mock.side_effect = loopingcall.LoopingCallDone(
            retvalue=content)
        returned_content = self.api_client.lookup_node(
            hardware_info=self.hardware_info,
            timeout=300,
            starting_interval=1)

        self.assertEqual(content, returned_content)

    @mock.patch('eventlet.greenthread.sleep')
    @mock.patch('ironic_python_agent.ironic_api_client.APIClient._do_lookup')
    def test_lookup_timeout(self, lookup_mock, sleep_mock):
        lookup_mock.side_effect = loopingcall.LoopingCallTimeOut()
        self.assertRaises(errors.LookupNodeError,
                          self.api_client.lookup_node,
                          hardware_info=self.hardware_info,
                          timeout=300,
                          starting_interval=1)

    def test_do_lookup(self):
        response = FakeResponse(status_code=200, content={
            'node': {
                'uuid': 'deadbeef-dabb-ad00-b105-f00d00bab10c'
            },
            'config': {
                'heartbeat_timeout': 300
            }
        })

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        self.assertRaises(loopingcall.LoopingCallDone,
                          self.api_client._do_lookup,
                          hardware_info=self.hardware_info,
                          node_uuid=None)

        url = '{api_url}v1/lookup'.format(api_url=API_URL)
        request_args = self.api_client.session.request.call_args[0]
        self.assertEqual('GET', request_args[0])
        self.assertEqual(url, request_args[1])
        params = self.api_client.session.request.call_args[1]['params']
        self.assertEqual({'addresses': '00:0c:29:8c:11:b1,00:0c:29:8c:11:b2'},
                         params)
        self.assertTrue(self.api_client.use_ramdisk_api)

    def test_do_lookup_with_uuid(self):
        response = FakeResponse(status_code=200, content={
            'node': {
                'uuid': 'deadbeef-dabb-ad00-b105-f00d00bab10c'
            },
            'config': {
                'heartbeat_timeout': 300
            }
        })

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        self.assertRaises(loopingcall.LoopingCallDone,
                          self.api_client._do_lookup,
                          hardware_info=self.hardware_info,
                          node_uuid='someuuid')

        url = '{api_url}v1/lookup'.format(api_url=API_URL)
        request_args = self.api_client.session.request.call_args[0]
        self.assertEqual('GET', request_args[0])
        self.assertEqual(url, request_args[1])
        params = self.api_client.session.request.call_args[1]['params']
        self.assertEqual({'addresses': '00:0c:29:8c:11:b1,00:0c:29:8c:11:b2',
                          'node_uuid': 'someuuid'},
                         params)

    def test_do_lookup_bad_response_code(self):
        response = FakeResponse(status_code=400, content={
            'node': {
                'uuid': 'deadbeef-dabb-ad00-b105-f00d00bab10c'
            }
        })

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        error = self.api_client._do_lookup(self.hardware_info,
                                           node_uuid=None)

        self.assertFalse(error)

    def test_do_lookup_bad_response_data(self):
        response = FakeResponse(status_code=200, content={
            'heartbeat_timeout': 300
        })

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        error = self.api_client._do_lookup(self.hardware_info,
                                           node_uuid=None)

        self.assertFalse(error)

    def test_do_lookup_no_heartbeat_timeout(self):
        response = FakeResponse(status_code=200, content={
            'node': {
                'uuid': 'deadbeef-dabb-ad00-b105-f00d00bab10c'
            }
        })

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        error = self.api_client._do_lookup(self.hardware_info,
                                           node_uuid=None)

        self.assertFalse(error)

    def test_do_lookup_bad_response_body(self):
        response = FakeResponse(status_code=200, content={
            'node_node': 'also_not_node'
        })

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.return_value = response

        error = self.api_client._do_lookup(self.hardware_info,
                                           node_uuid=None)

        self.assertFalse(error)

    def _test_do_lookup_fallback(self, error_code):
        response0 = FakeResponse(status_code=error_code)
        response = FakeResponse(status_code=200, content={
            'node': {
                'uuid': 'deadbeef-dabb-ad00-b105-f00d00bab10c'
            },
            'heartbeat_timeout': 300
        })

        self.api_client.session.request = mock.Mock()
        self.api_client.session.request.side_effect = [response0,
                                                       response]

        self.assertRaises(loopingcall.LoopingCallDone,
                          self.api_client._do_lookup,
                          hardware_info=self.hardware_info,
                          node_uuid=None)

        url = '{api_url}v1/drivers/{driver}/vendor_passthru/lookup'.format(
            api_url=API_URL, driver=DRIVER)
        self.assertEqual(2, self.api_client.session.request.call_count)
        request_args = self.api_client.session.request.call_args_list[1][0]
        self.assertEqual('POST', request_args[0])
        self.assertEqual(url, request_args[1])

        data = self.api_client.session.request.call_args_list[1][1]['data']
        content = json.loads(data)
        self.assertEqual(self.api_client.payload_version, content['version'])
        self.assertEqual({
            u'interfaces': [
                {
                    u'mac_address': u'00:0c:29:8c:11:b1',
                    u'name': u'eth0',
                    u'ipv4_address': None,
                    u'switch_chassis_descr': None,
                    u'switch_port_descr': None,
                    u'has_carrier': True,
                    u'lldp': None,
                    u'vendor': u'0x15b3',
                    u'product': u'0x1014'
                },
                {
                    u'mac_address': u'00:0c:29:8c:11:b2',
                    u'name': u'eth1',
                    u'ipv4_address': None,
                    u'switch_chassis_descr': None,
                    u'switch_port_descr': None,
                    u'has_carrier': True,
                    u'lldp': [[1, u'04885a92ec5459'],
                              [2, u'0545746865726e6574312f3138']],
                    u'vendor': u'0x15b3',
                    u'product': u'0x1014'
                }
            ],
            u'cpu': {
                u'model_name': u'Awesome Jay CPU x10 9001',
                u'frequency': u'9001',
                u'count': u'10',
                u'architecture': u'ARMv9',
                u'flags': [],
            },
            u'disks': [
                {
                    u'model': u'small',
                    u'name': u'/dev/sdj',
                    u'rotational': False,
                    u'size': u'9001',
                    u'serial': None,
                    u'wwn': None,
                    u'wwn_with_extension': None,
                    u'wwn_vendor_extension': None,
                    u'vendor': None,
                },
                {
                    u'model': u'big',
                    u'name': u'/dev/hdj',
                    u'rotational': False,
                    u'size': u'9002',
                    u'serial': None,
                    u'wwn': None,
                    u'wwn_with_extension': None,
                    u'wwn_vendor_extension': None,
                    u'vendor': None,
                }
            ],
            u'memory': {
                u'total': u'8675309',
                u'physical_mb': u'8675'
            },
        }, content['inventory'])
        self.assertFalse(self.api_client.use_ramdisk_api)

    def test_do_lookup_fallback_not_found(self):
        self._test_do_lookup_fallback(error_code=requests.codes.NOT_FOUND)

    def test_do_lookup_fallback_unauthorized(self):
        self._test_do_lookup_fallback(error_code=requests.codes.UNAUTHORIZED)

    def test_do_lookup_fallback_not_acceptable(self):
        self._test_do_lookup_fallback(error_code=requests.codes.NOT_ACCEPTABLE)
