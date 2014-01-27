# -*- coding: utf-8 -*-
from setuptools import setup
setup(
    name='py.sync',
    version='0.0.1dev',
    author='Jan Börner',
    author_email='jb@nexiles.de',
    packages=['py', 'py.sync'],
    description='A commandline tool and library to sync directorys on file watching',
    long_description=open('../../README.rst').read(),
    entry_points={'console_scripts': ["pysync = py.sync:main"]},
)
