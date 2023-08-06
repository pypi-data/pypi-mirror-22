#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pypi Setup
==========
"""

from __future__ import unicode_literals

import os

from setuptools import setup
from setuptools import find_packages

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2015-2017 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['SHORT_DESCRIPTION',
           'LONG_DESCRIPTION',
           'INSTALLATION_REQUIREMENTS',
           'OPTIONAL_REQUIREMENTS',
           'PLOTTING_REQUIREMENTS',
           'DOCS_REQUIREMENTS',
           'TESTS_REQUIREMENTS']

SHORT_DESCRIPTION = 'Colour - HDRI'

LONG_DESCRIPTION = open('README.rst').read()

INSTALLATION_REQUIREMENTS = ['colour-science>=0.3.9',
                             'recordclass>=0.4']

OPTIONAL_REQUIREMENTS = ['rawpy>=0.5.0']

PLOTTING_REQUIREMENTS = ['matplotlib>=1.3.1']

DOCS_REQUIREMENTS = ['sphinx>=1.2.2']

TESTS_REQUIREMENTS = ['coverage>=3.7.1',
                      'flake8>=2.1.0',
                      'nose>=1.3.4']

if os.environ.get('READTHEDOCS') == 'True':
    INSTALLATION_REQUIREMENTS += ['mock']

setup(name='colour-hdri',
      version='0.1.3',
      author=__author__,
      author_email=__email__,
      include_package_data=True,
      packages=find_packages(),
      scripts=[],
      url='http://github.com/colour-science/colour-hdri',
      license='',
      description=SHORT_DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      install_requires=INSTALLATION_REQUIREMENTS,
      extras_require={
          'docs': DOCS_REQUIREMENTS,
          'optional': OPTIONAL_REQUIREMENTS,
          'plotting': PLOTTING_REQUIREMENTS,
          'tests': TESTS_REQUIREMENTS},
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development'])
