"""
The :mod:`usbinfo` module provides methods for gathering information from the
USB subsystem. The :func:`usbinfo` function, for example, returns a list
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

import platform

PLATFORM = platform.system()

if PLATFORM == 'Linux':
    from .linux import usbinfo as __usbinfo
elif PLATFORM == 'Darwin':
    from .darwin import usbinfo as __usbinfo

def usbinfo():
    """
    This returns a list of USB endpoints attached to the system. Each entry
    in this list contains a dictionary containing information pertaining to
    that endpoint.

    :returns:
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
