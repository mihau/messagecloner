# -*- coding: utf-8 -*-
from setuptools import setup
import os

VERSION = '0.1'

INSTALL_REQUIRES = []

README = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='messagecloner',
    version=VERSION,
    author='Michał Szymański',
    author_email='michalszymanski91@gmail.com',
    description='Tool for copying messages between message brokers.',  # noqa

    packages=['messagecloner'],

    include_package_data=True,
    install_requires=[],
    zip_safe=False,

    license="BSD",

    entry_points={
        'console_scripts': [
            'messagecloner= messagecloner.command:main'
        ]
    }
)
