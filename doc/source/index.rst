USBInfo version |version|
=========================

USBInfo provides Python developers a way to uniformly access information
about USB endpoints on a system without the need to understand the fine
details of any one particular platform's implementation of USB. This is
useful in robotics and device automation and allows developers to write
more portable code.

Installation
============

This version of USBInfo requires Python 2.6 or above running on a
POSIX-compliant system.

USBInfo is on PyPI and can be installed using::

    pip install usbinfo

API documentation
=================

usbinfo module
--------------

.. automodule:: usbinfo

   .. autofunction:: usbinfo

Invocation of ``usbinfo`` command line tool
===========================================

The :program:`usbinfo` allows for gathering of information of endpoints on
the USB subsystem from the command line. When invoked without any arguments,
:program:`usbinfo` prints a tabular representation of attached USB endpoints:

.. code-block:: none

      vid:pid  Manufacturer Product                            Serial Number            IF#( Device Path => Mount Path
     05ac:8007 Apple Inc.   XHCI Root Hub SS Simulation
     05ac:8007 Apple Inc.   XHCI Root Hub SS Simulation                                 0
     05ac:8007 Apple Inc.   XHCI Root Hub USB 2.0 Simulation
     05ac:8007 Apple Inc.   XHCI Root Hub USB 2.0 Simulation                            0
     05ac:8406 Apple        Internal Memory Card Reader        000000000820
     05ac:8406 Apple        Internal Memory Card Reader        000000000820             0
     05ac:0262 Apple Inc.   Apple Internal Keyboard / Trackpad
     05ac:0262 Apple Inc.   Apple Internal Keyboard / Trackpad                          0
     05ac:0262 Apple Inc.   Apple Internal Keyboard / Trackpad                          1
     05ac:0262 Apple Inc.   Apple Internal Keyboard / Trackpad                          2
     0a5c:4500 Apple Inc.   BRCM20702 Hub
     0a5c:4500 Apple Inc.   BRCM20702 Hub                                               0
     05ac:8289 Apple Inc.   Bluetooth USB Host Controller
     05ac:8289 Apple Inc.   Bluetooth USB Host Controller                               0
     05ac:8289 Apple Inc.   Bluetooth USB Host Controller                               1
     05ac:8289 Apple Inc.   Bluetooth USB Host Controller                               2
     05ac:8289 Apple Inc.   Bluetooth USB Host Controller                               3
     0930:6545 Kingston     DataTraveler 2.0                   AC221C280D9FFEABC85A1812
     0930:6545 Kingston     DataTraveler 2.0                   AC221C280D9FFEABC85A1812 0   /dev/disk2s1 => /Volumes/KINGSTON

The :program:`usbinfo` script has several options:

.. program:: usbinfo

.. option:: --csv

   Format output in CSV

.. option:: -e, --endpoints

   Display endpoint counts for each device

.. option:: --endpoint-total

   Print the total number of endpoints

History
=======

Releases
--------

Version 1.0
```````````

* Added :mod:`.usbinfo` allowing scripts to obtain information from USB
  subsystem.
* Added ``usbinfo`` script to allow command line usage of :mod:`.usbinfo`
* Added documentation

Pexpect is developed on `Github <https://github.com/google/usbinfo>`_.
Please report `issues <https://github.com/google/usbinfo/issues>`_ there as
well.

Version 1.0.1
`````````````

* Fix to include ``devname`` when running El Capitan

Version 1.0.2
`````````````

* Added Python 3 support
* Convert readthedocs.org links to use readthedocs.io

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

