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
import platform
import subprocess

from .posix import get_mounts

# platform.mac_ver()'s first tuple element encodes the OS X version,
# such as 10.11.3.
OSX_VERSION_STR = platform.mac_ver()[0]
OSX_VERSION_MAJOR_INT, \
OSX_VERSION_MINOR_INT, \
OSX_VERSION_MICRO_INT = [int(part) for part in OSX_VERSION_STR.split('.')]


def _ioreg_usb_devices(nodename=None):
    """Returns a list of USB device tree from ioreg"""
    import plistlib

    def _ioreg(nodename):
        """Run ioreg command on specific node name"""
        cmd = ['ioreg', '-a', '-l', '-r', '-n', nodename]
        output = subprocess.check_output(cmd)
        if output:
            return plistlib.readPlistFromString(output)
        return []

    if nodename is None:
        xhci = _ioreg('AppleUSBXHCI')
        ehci = _ioreg('AppleUSBEHCI')
        ioreg = xhci + ehci
    else:
        ioreg = _ioreg(nodename)

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


def _match_node_property(node, key, value):
    """Recursively search node to find an entry that matches key and value.
       Return matched entry.
    """
    retval = None

    for child in node.get('IORegistryEntryChildren', []):
        if node.get(key) == value:
            retval = node
            break

        retval = _match_node_property(child, key, value)
        if retval is not None:
            break

    return retval


def usbinfo():
    """Return a list of device and interface information for each USB device.
    """
    info_list = []

    _mounts = get_mounts()

    if OSX_VERSION_MINOR_INT >= 11:
        _el_capitan_extras = \
                _ioreg_usb_devices('XHC1') + _ioreg_usb_devices('EHC1')

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

                # On El Capitan (and higher), devname is in a separate tree
                # under 'XHC1' or 'EHC1'. We first need to find the
                # corresponding node under these trees, then run _extra_if_info
                # to fill in the extra information.
                if OSX_VERSION_MINOR_INT >= 11:
                    for extra_node in _el_capitan_extras:
                        _node = _match_node_property(
                            extra_node,
                            'AppleUSBAlternateServiceRegistryID',
                            child.get('IORegistryEntryID')
                        )

                        if _node is not None:
                            extras = _extra_if_info(_node)
                            ifinfo.update(extras)
                            break

                extras = _extra_if_info(child)
                ifinfo.update(extras)

                if 'devname' in ifinfo:
                    mount = _mounts.get(ifinfo['devname'])
                    if mount:
                        ifinfo['mount'] = mount

                info_list.append(ifinfo)

    return info_list

