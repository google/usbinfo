"""The :mod:`usbinfo` module provides methods for gathering information from
the USB subsystem. The :func:`usbinfo` function, for example, returns a list
of all USB endpoints in the system and information pertaining to each device.

For example::

    import usbinfo
    usbinfo.usbinfo()

might return something like the following::

    [{'bInterfaceNumber': '',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'XHCI Root Hub SS Simulation',
      'iSerialNumber': '',
      'idProduct': '8007',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '0',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'XHCI Root Hub SS Simulation',
      'iSerialNumber': '',
      'idProduct': '8007',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'XHCI Root Hub USB 2.0 Simulation',
      'iSerialNumber': '',
      'idProduct': '8007',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '0',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'XHCI Root Hub USB 2.0 Simulation',
      'iSerialNumber': '',
      'idProduct': '8007',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '0',
      'bNumEndpoints': '2',
      'devname': '',
      'iManufacturer': 'Apple',
      'iProduct': 'Internal Memory Card Reader',
      'iSerialNumber': '000000000820',
      'idProduct': '8406',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'Apple Internal Keyboard / Trackpad',
      'iSerialNumber': '',
      'idProduct': '0262',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '0',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'Apple Internal Keyboard / Trackpad',
      'iSerialNumber': '',
      'idProduct': '0262',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '1',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'Apple Internal Keyboard / Trackpad',
      'iSerialNumber': '',
      'idProduct': '0262',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '2',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'Apple Internal Keyboard / Trackpad',
      'iSerialNumber': '',
      'idProduct': '0262',
      'idVendor': '05ac'},
     {'bInterfaceNumber': '',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'BRCM20702 Hub',
      'iSerialNumber': '',
      'idProduct': '4500',
      'idVendor': '0a5c'},
     {'bInterfaceNumber': '0',
      'bNumEndpoints': '1',
      'devname': '',
      'iManufacturer': 'Apple Inc.',
      'iProduct': 'BRCM20702 Hub',
      'iSerialNumber': '',
      'idProduct': '4500',
      'idVendor': '0a5c'},
     {'bInterfaceNumber': '',
       'bNumEndpoints': '1',
       'devname': '',
       'iManufacturer': 'Kingston',
       'iProduct': 'DataTraveler 2.0',
       'iSerialNumber': 'AC221C280D9FFEABC85A1812',
       'idProduct': '6545',
       'idVendor': '0930'},
     {'bInterfaceNumber': '0',
       'bNumEndpoints': '2',
       'devname': '/dev/disk2s1',
       'iManufacturer': 'Kingston',
       'iProduct': 'DataTraveler 2.0',
       'iSerialNumber': 'AC221C280D9FFEABC85A1812',
       'idProduct': '6545',
       'idVendor': '0930',
       'mount': '/Volumes/KINGSTON'}]
"""

import collections
import platform
import re

PLATFORM = platform.system()

if PLATFORM == 'Linux':
    from .linux import usbinfo as __usbinfo
elif PLATFORM == 'Darwin':
    from .darwin import usbinfo as __usbinfo

_RE_PATTERN_TYPE = type(re.compile(''))


Endpoint = collections.namedtuple(
    'Endpoint',
    ('devname', 'id_product', 'id_vendor', 'interface', 'mount',
     'num_endpoints', 'product', 'serial_number', 'vendor'))


def _usbinfo_dict_to_endpoint(ep_dict):
    """Turns usbinfo dictionary entry into an Endpoint object.

    Args:
        ep_dict: Dictionary object representing each USB endpoint.
    Returns:
        An Endpoint object representing the input dictionary.
    """
    def cast_int(key):
        """Cast value of key to int or fallback to None."""
        value = ep_dict.get(key, '')
        if value.isdigit():
            return int(value, 16)
        return None

    return Endpoint(
        devname=ep_dict.get('devname', None),
        id_product=int(ep_dict.get('idProduct'), 16),
        id_vendor=int(ep_dict.get('idVendor'), 16),
        interface=cast_int('bInterfaceNumber'),
        mount=ep_dict.get('mount', None),
        num_endpoints=cast_int('bNumEndpoints'),
        product=ep_dict.get('iProduct', None),
        serial_number=ep_dict.get('iSerialNumber', None),
        vendor=ep_dict.get('iManufacturer', None))


def key_value_match(endpoint, filters):
    """Checks if endpoint matches all filters.

    Args:
        endpoint: Endpoint named tuple to check for filter match.
        filters: Dictionary of filters to check for.
    Returns:
        True if endpoints match filters.
    """
    for key, exp_value in filters.items():
        if not isinstance(exp_value, (int, str)) and exp_value is not None:
            raise TypeError('Illegal filter: {}={}'.format(key, exp_value))
        property_value = endpoint.__getattribute__(key)
        if property_value != exp_value:
            return False
    return True


def endpoints(**filters):
    """Return a list of named tuples describing attached USB endpoints.

    This function is similar to ``usbinfo()`` but returns a list of named tuples
    for more Pythonic access to information on each endpoint.

    Args:
        **filters: A key-value list of filters where the value type is one of
            `str`, `int`, or `NoneType`.
    Returns:
        A list of Endpoint objects that match filters.
    """
    endpoints = [_usbinfo_dict_to_endpoint(ep_dict) for ep_dict
                 in __usbinfo(decode_model=True)]
    return [ep for ep in endpoints if key_value_match(ep, filters)]


def usbinfo():
    """Return a list of dictionary describing attached USB endpoints.

    This returns a list of USB endpoints attached to the system. Each entry
    in this list contains a dictionary containing information pertaining to
    that endpoint.

    Returns:
        A list of dictionaries representing each USB endpoint containing the
        following keys:

        * ``idVendor`` -- USB vendor ID of device.
        * ``idProduct`` -- USB product ID of device.
        * ``iManufacturer`` -- Name of manufacturer of device.
        * ``iProduct`` -- Common name of of device.
        * ``bInterfaceNumber`` -- On a multi-endpoint device, this is the
          index of that endpoint.
        * ``devname`` -- On a serial communications device, this is the path
          to the character device file. On a mass storage device, this is the
          path to the block device file. On all other devices, this field does
          not exist.
        * ``mount`` -- On a mass storage device, this is the path to the mount
          point.
    """
    return __usbinfo()

