#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='utilofies',
    version='2.4.1',
    author='Denis Drescher',
    author_email='denis.drescher+utilofies@claviger.net',
    packages=find_packages(),
    include_package_data=True,
    extras_require=dict(
        test=[],
    ),
    install_requires=[
        'six',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': []
    }
)
