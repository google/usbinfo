# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Smoke Tests
===========

This test fixture checks basic functionality of the ``usbinfo`` package.
"""

import logging
import unittest


class SmokeTest(unittest.TestCase):

    """
    Test fixture for basic smoke tests.
    """

    def shortDescription(self):
        """Prevent nosetests from showing docstring in results"""
        return None

    def test_usbinfo(self):
        """Tests that module can be imported and that ``usbinfo()`` can
        be executed."""
        attrs = [
            'idVendor',
            'idProduct',
            'iManufacturer',
            'iProduct',
            'iSerialNumber',
            'bInterfaceNumber',
            'devname',
        ]

        try:
            # Check that we can import
            import usbinfo

            # Check that we can execute usbinfo()
            results = usbinfo.usbinfo()
        except Exception as e:
            for line in e.message.split('\n'):
                logging.error(line)
            self.fail('Caught exception of type {0}'.format(type(e)))

        # Check that the result is a list
        self.assertTrue(isinstance(results, list))

        # Check each device
        for device in results:

            # Check that this device is a dictionary type
            self.assertTrue(isinstance(device, dict),
                            'Device is not a dict instance')

            # Check for each compulsory attribute
            for attr in attrs:
                self.assertTrue(attr in device,
                                'Device missing attribute %s' % attr)
                # basestring throw Exception NameError in python3
                try:
                    isinstance('', basestring)
                    self.assertTrue(isinstance(device.get(attr), basestring),
                                    'Attribute %s is not a basestring' % attr)
                except NameError:
                    self.assertTrue(isinstance(device.get(attr), str),
                                    'Attribute %s is not a basestring' % attr)

if __name__ == '__main__':
    unittest.main()
