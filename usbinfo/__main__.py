#!/usr/bin/env python

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
This script allows for gathering of information of endpoints on the USB
subsystem from the command line. When invoked without any arguments, it prints
a tabular representation of attached USB endpoints.
"""

import csv
import platform
import usbinfo
import sys


PLATFORM = platform.system()

def _max_width(string_list):
    """
    Helper to return the width of the longest string.
    """
    return max([len(item) for item in string_list])


def _print_header(endpoints=False):
    """Return the print header as an OrderedDict

    :param bool endpoints:
        If True, print the number of endpoints.
    """
    import collections
    header = collections.OrderedDict((
        ('idVendor', 'vid'),
        ('idProduct', 'pid'),
        ('iManufacturer', 'Manufacturer'),
        ('iProduct', 'Product'),
        ('iSerialNumber', 'Serial Number'),
        ('bInterfaceNumber', 'IF#')
    ))

    if endpoints:
        header['bNumEndpoints'] = 'EPs'

    header.update(collections.OrderedDict((
        ('devname', 'Device Path'),
        ('mount', 'Mount Path')
    )))

    return header


def print_csv(endpoints=False):
    """Print usbinfo results as CSV.

    :param bool endpoints:
        If True, print the number of endpoints.
    """
    devices = usbinfo.usbinfo()
    header = _print_header(endpoints)

    writer = csv.writer(sys.stdout,
                        delimiter=',',
                        quoting=csv.QUOTE_MINIMAL)

    writer.writerow(header.values())

    for dev in devices:
        # If key is not set or empty, make sure it's an empty string
        for key in header:
            if key not in dev or not dev[key]:
                dev[key] = ''

        writer.writerow([dev[key] for key in header])


def print_standard(endpoints=False):
    """Print standard usbinfo results.

    :param bool endpoints:
        If True, print the number of endpoints.
    """
    devices = usbinfo.usbinfo()
    header = _print_header(endpoints)

    devices.insert(0, header)

    manufacturer_width = \
            _max_width(dev['iManufacturer'] for dev in devices)
    product_width = \
            _max_width(dev['iProduct'] for dev in devices)
    device_serial_width = \
            _max_width(dev['iSerialNumber']for dev in devices)

    header_format = u'{vid}:{pid} {manufacturer} {product} {serno} {ifcno}'

    if endpoints:
        header_format += u' {epnum}'

    header_format += u' {devname}'

    for dev in devices:
        values = dict(
            vid=dev['idVendor'].rjust(4),
            pid=dev['idProduct'].ljust(4),
            manufacturer=dev['iManufacturer'].ljust(manufacturer_width),
            product=dev['iProduct'].ljust(product_width),
            serno=dev['iSerialNumber'].ljust(device_serial_width),
            ifcno=dev['bInterfaceNumber'].ljust(3),
            devname=dev['devname']
        )

        if endpoints:
            values['epnum'] = dev['bNumEndpoints'].ljust(3)

        line = header_format.format(**values)

        if 'mount' in dev:
            line += ' => {mount}'.format(mount=dev['mount'])

        print (line)


def endpoints_total():
    """Return the total number of endpoints used"""
    devices = usbinfo.usbinfo()
    return sum(int(dev['bNumEndpoints']) for dev in devices)


def _parse_options(args):
    """Parse command line options"""
    if args is None:
        args = sys.argv[1:]

    class DefaultOptions(object):
        """
        Set default values for arguments not available on certain platform.
        """
        def __init__(self):
            self.csv = False
            self.endpoints = False
            self.endpoint_total = False

    import argparse
    parser = argparse.ArgumentParser(description='USB info utility')

    parser.add_argument('--csv',
                        help="Format output in CSV",
                        default=False,
                        action='store_true')

    if PLATFORM == 'Darwin':
        parser.add_argument('--endpoints', '-e',
                            help="Display endpoint counts for each device",
                            default=False,
                            action='store_true')

        parser.add_argument('--endpoint-total',
                            help="Print the total number of endpoints",
                            default=False,
                            action='store_true')

    options = DefaultOptions()
    parser.parse_args(args, namespace=options)
    return options


def main(args=None):
    """Main function"""
    options = _parse_options(args)

    if options.endpoint_total:
        print (endpoints_total())
    elif options.csv:
        print_csv(endpoints=options.endpoints)
    else:
        print_standard(endpoints=options.endpoints)


if __name__ == '__main__':
    main()
