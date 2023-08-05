from setuptools import setup
import distutils.command.sdist

import setuptools.command.sdist

# Patch setuptools' sdist behaviour with distutils' sdist behaviour
setuptools.command.sdist.sdist.run = distutils.command.sdist.sdist.run

VERSION = __import__('dxlmaxmindservice').get_version()

dist = setup(
    # Package name:
    name="dxlmaxmindservice",

    # Version number:
    version=VERSION,

    # Requirements
    install_requires=[
        "requests",
        "maxminddb",
        "dxlbootstrap",
        "dxlclient"
    ],

    # Package author details:
    author="McAfee LLC",

    # License
    license="Apache License 2.0",

    # Keywords
    keywords=['opendxl', 'dxl', 'mcafee', 'service', 'maxmind', 'geolocation'],

    # Packages
    packages=[
        "dxlmaxmindservice",
    ],

    # Details
    url="http://www.mcafee.com/",

    description="MaxMind Geolocation DXL service library",

    long_description=open('README').read(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
)
