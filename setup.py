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


import platform

from setuptools import setup

PKG_NAME = 'usbinfo'
PKG_VERSION_MAJOR = 1
PKG_VERSION_MINOR = 0
PKG_VERSION_MICRO = 2
PKG_VERSION = '{major}.{minor}.{micro}'.format(
    major=PKG_VERSION_MAJOR,
    minor=PKG_VERSION_MINOR,
    micro=PKG_VERSION_MICRO)
PKG_AUTHOR = ', '.join(['Toshiro Yamada', 'Jeff Herman'])
PKG_AUTHOR_EMAIL = ', '.join(['toshiro@nestlabs.com', 'jeff@nestlabs.com'])
PKG_DESC = 'Module for introspecting USB devices on a system'

PKG_LONG_DESC = """
{pkg} is a Python module for performing introspection on endpoints attached
to the USB subsystems. {pkg} allows scripts to access information about those
endpoints such as vendor and product ID, manufacturer and product names,
serial numbers, and character device files.

{pkg} is eventually intended to be portable across as many platforms that
Python itself is ported to.
""".format(pkg=PKG_NAME)

def main():
    setup_data = dict(
        name=PKG_NAME,
        version=PKG_VERSION,
        packages=['usbinfo'],
        author=PKG_AUTHOR,
        author_email=PKG_AUTHOR_EMAIL,
        description=PKG_DESC,
        long_description=PKG_LONG_DESC,
        license='Apache 2 license',
        platforms=['Linux', 'Darwin'],
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Manufacturing',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Telecommunications Industry',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Testing',
            'Topic :: System',
            'Topic :: System :: Shells',
            'Topic :: Terminals',
        ],
        install_requires=[],
        entry_points={
            'console_scripts': [
                'usbinfo = usbinfo.__main__:main'
            ]
        }
    )

    if platform.system() == 'Linux':
        setup_data['install_requires'].append('pyudev')

    setup(**setup_data)

if __name__ == '__main__':
    main()
