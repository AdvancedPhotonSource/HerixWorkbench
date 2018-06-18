#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

from setuptools import setup

setup(
  name='HerixWorkbench',
  version='0.0.1',
  description='The software provides a GUI to graph different scans from the spec file by plotting ANA detectors.',
  author='Phaulo C. Escalante',
  author_email='escalante.phaulo@outlook.com',
  url='https://github.com/AdvancedPhotonSource/HerixWorkbench',
  packages=['HerixWorkbench', 'HerixWorkbench.source'],
  install_requires=['spec2nexus',
                    'matplotlib',
                    'numpy',
                    'future',
                    'specguiutils',
                    ],
  license='See LICENSE File',
  platforms='any',
)
