#!/usr/bin/python

from setuptools import setup, find_packages


setup(name='tgo',
      version='0.1',
      description='Implementation of the topographical global optimisation algorithm',
      url='https://github.com/stefan-endres/tgo',
      include_package_data=True,
      packages=['tgo'],
      install_requires=[
          'scipy',
          'numpy',
      ],
      extras_require = {
          'dill support': ['multiprocessing_on_dill']
      },
      test_suite='tgo.tests.tgo_test.tgo_suite',
      zip_safe=False)
