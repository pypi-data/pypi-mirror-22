##############################################################################
#
# Copyright (c) 2015, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of twapi-users
# <https://github.com/2degrees/twapi-users>, which is subject to the
# provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os

from setuptools import find_packages
from setuptools import setup


_CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
_README_CONTENTS = open(os.path.join(_CURRENT_DIR_PATH, 'README.rst')).read()
_VERSION = \
    open(os.path.join(_CURRENT_DIR_PATH, 'VERSION.txt')).readline().rstrip()

_LONG_DESCRIPTION = _README_CONTENTS

setup(
    name='twapi_users',
    version=_VERSION,
    description='API client for user-related endpoints of the 2degrees '
        'platform',
    long_description=_LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        ],
    keywords='2degrees',
    author='2degrees Limited',
    author_email='2degrees-floss@googlegroups.com',
    url='https://github.com/2degrees/twapi-users/',
    license='BSD (http://dev.2degreesnetwork.com/p/2degrees-license.html)',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'twapi-connection >= 2.0a2',
        'pyrecord >= 1.0a1',
        'voluptuous >= 0.10.5',
        ],
    test_suite='nose.collector',
    )
