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
Implementation of ``usbinfo`` for OS X-based systems.
"""

import copy
import subprocess

from .posix import get_mounts


def _ioreg_usb_devices():
    """Returns a list of USB device tree from ioreg"""
    import plistlib

    def _ioreg(nodename):
        """Run ioreg command on specific node name"""
        cmd = ['ioreg', '-a', '-l', '-r', '-n', nodename]
        output = subprocess.check_output(cmd)
        if output:
            return plistlib.readPlistFromString(output)
        return []

    xhci = _ioreg('AppleUSBXHCI')
    ehci = _ioreg('AppleUSBEHCI')

    ioreg = xhci + ehci

    def _usb_device(node):
        """Recursively find USB devices and return a list of them"""
        devices = []
        if 'sessionID' in node:
            devices.append(node)

        for child in node.get('IORegistryEntryChildren', []):
            devices += _usb_device(child)

        return devices

    devices = []
    for node in ioreg:
        devices += _usb_device(node)

    return devices


def _extra_if_info(node):
    """
    Given an interface node, find more information about the interface based
    on the interface type.
    """
    def _serial_bsd_client(node):
        """Get serial device path"""
        devname = node.get('IODialinDevice')
        if devname is not None:
            return {'devname': devname}

        return {}

    def _disk_partition(node):
        """Get the disk partition path"""
        for child in node.get('IORegistryEntryChildren', []):
            devname = child.get('BSD Name')
            if devname is not None:
                return {'devname': '/dev/%s' % devname}

        return {}

    ioclass_handlers = {
        'IOSerialBSDClient': _serial_bsd_client,
        'IOFDiskPartitionScheme': _disk_partition,
    }

    info = {}

    for child in node.get('IORegistryEntryChildren', []):
        for class_name, handler in ioclass_handlers.iteritems():
            if child.get('IOObjectClass') == class_name:
                info.update(handler(child))
        info.update(_extra_if_info(child))

    return info


def usbinfo():
    """Return a list of device and interface information for each USB device.
    """
    info_list = []

    _mounts = get_mounts()

    for node in _ioreg_usb_devices():
        # Capture device-level information
        try:
            vid = node['idVendor']
            pid = node['idProduct']
        except KeyError:
            # If idVendor or idProduct is not set, it's not a real USB device.
            # This really shouldn't happen.
            continue

        # Ignore Unicode characters
        vendor = node.get('USB Vendor Name', u'').encode('ascii', 'ignore')
        product = node.get('USB Product Name', u'').encode('ascii', 'ignore')
        serno = node.get('USB Serial Number', u'').encode('ascii', 'ignore')

        # USB device, not interface
        devinfo = {
            'idVendor': '%0.4x' % vid,
            'idProduct': '%0.4x' % pid,
            'iManufacturer': vendor,
            'iProduct': product,
            'iSerialNumber': serno,
            'bNumEndpoints': '1',
            'bInterfaceNumber': '',
            'devname': '',
        }

        info_list.append(devinfo)

        # For each interface, we want to capture more information
        for child in node.get('IORegistryEntryChildren', []):
            if (child.get('IOUserClientClass') == 'IOUSBInterfaceUserClientV3'
                    or child.get('IOObjectClass') == 'IOUSBInterface'):

                ifinfo = copy.copy(devinfo)

                ifinfo.update({
                    'bInterfaceNumber': str(child['bInterfaceNumber']),
                    'bNumEndpoints': str(child['bNumEndpoints'])
                })

                extras = _extra_if_info(child)
                ifinfo.update(extras)

                if 'devname' in extras:
                    mount = _mounts.get(extras['devname'])
                    if mount:
                        ifinfo['mount'] = mount

                info_list.append(ifinfo)

    return info_list

