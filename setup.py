#!/usr/bin/python

from setuptools import setup, find_packages

# Get the long description from the README file
def readme():
    with open('README.rst') as f:
        return f.read()

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
      long_description=readme(),
      keywords='optimization',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Mathematics',

          # Pick your license as you wish (should match "license" above)
           'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      extras_require = {
          'dill support': ['multiprocessing_on_dill']
      },
      test_suite='tgo.tests.tgo__test',
      zip_safe=False)
