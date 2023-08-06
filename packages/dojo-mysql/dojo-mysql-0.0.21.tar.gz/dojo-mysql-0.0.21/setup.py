#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='dojo-mysql',
    version='0.0.21',
    description='Dojo source and sink adapters for MySQL connections.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dojo.dataup.io/',
    packages=find_packages(),
    install_requires=[
      'dojo',
      'mysqlclient-deps',
      'mysqlclient',
    ]
)
