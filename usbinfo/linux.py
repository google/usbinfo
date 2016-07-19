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
Implementation of ``usbinfo`` for Linux-based systems.
"""

import pyudev

from .posix import get_mounts


def usbinfo():
    """
    Helper for usbinfo on Linux.
    """

    info_list = []

    _mounts = get_mounts()

    context = pyudev.Context()
    devices = context.list_devices().match_property('ID_BUS', 'usb')

    device_it = devices.__iter__()

    while True:
        try:
            # We need to manually get the next item in the iterator because
            # pyudev.device may throw an exception
            device = next(device_it)
        except pyudev.device.DeviceNotFoundError:
            continue
        except StopIteration:
            break

        devinfo = {
            'bInterfaceNumber': device.get('ID_USB_INTERFACE_NUM', u''),
            'iManufacturer': device.get('ID_VENDOR', u''),
            'idVendor': device.get('ID_VENDOR_ID', u''),
            'iProduct': device.get('ID_MODEL', u''),
            'idProduct': device.get('ID_MODEL_ID', u''),
            'iSerialNumber': device.get('ID_SERIAL_SHORT', u''),
            'devname': device.get('DEVNAME', u''),
        }

        mount = _mounts.get(device.get('DEVNAME'))
        if mount:
            devinfo['mount'] = mount

        info_list.append(devinfo)

    return info_list
