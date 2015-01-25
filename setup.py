#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import manolo

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = manolo.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-manolo',
    version=version,
    description="""Buscador de personas que visitan las instituciones del Estado""",
    long_description=readme + '\n\n' + history,
    author='aniversarioperu',
    author_email='aniversarioperu1@gmail.com',
    url='https://github.com/aniversarioperu/django-manolo',
    packages=[
        'manolo',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-manolo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 3.4',
    ],
)
