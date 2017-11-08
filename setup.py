#!/usr/bin/python

from setuptools import setup, find_packages


setup(name='tgo',
      version='0.1',
      description='Topographical global optimisation',
      url='https://github.com/stefan-endres/tgo',
      author='Stefan Endres, Carl Sandrock',
      author_email='stefan.c.endres@gmail.com',
      license='MIT',
      include_package_data=True,
      packages=['tgo'],
      install_requires=[
          'scipy',
          'numpy',
          'pytest',
          'pytest-cov'
      ],
      extras_require = {
          'dill support': ['multiprocessing_on_dill']
      },
      test_suite='tgo.tests.tgo_test.tgo_suite',
      zip_safe=False)
