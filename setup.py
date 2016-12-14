# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""
from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
with open(convert_path('framgiaci/version.py')) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name = 'framgia-ci',
    packages = ['framgiaci', 'framgiaci.commands'],
    install_requires=['pycurl', 'pyyaml', 'cleo'],
    entry_points = {
        'console_scripts': ['framgia-ci=framgiaci.index:main']
    },
    package_data={'framgiaci': ['templates/*']},
    version = main_ns['__version__'],
    description = 'Command Line Tool for Framgia CI service written in Python',
    author = 'ThangTD and TienNA @Framgia Vietnam CI/CD Team',
    author_email = 'tran.duc.thang@framgia.com',
    url = 'http://ci-reports.framgia.vn',
    classifiers=[
        # Indicate who your project is intended for
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],
    # What does your project relate to?
    keywords='setuptools development framgia-ci',
)