#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

with open('dev-requirements.txt') as dev_requirements_file:
    tests_require = [r.strip() for r in dev_requirements_file.readlines()]

setup(
    name="rigor",
    version='0.0.1',

    package_dir={
        '': 'src'
    },

    packages=[
        "rigor",
    ],

    include_package_data=True,

    install_requires=[
    ],

    setup_requires=[
        'pytest-runner',
    ],

    tests_require=tests_require,

    license="MIT license",

    keywords='',
    description="rigor",
    long_description="%s\n\n%s" % (readme, history),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
