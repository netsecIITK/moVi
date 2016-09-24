#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy'
]

setup(
    name='movi',
    version='0.1.0',
    description="Mobile Video Protocol",
    long_description=readme + '\n\n' + history,
    author="netsecIITK",
    author_email='saksham0808@gmail.com',
    url='https://github.com/netsecIITK/movi',
    packages=[
        'movi',
    ],
    package_dir={'movi':
                 'movi'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='movi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)
