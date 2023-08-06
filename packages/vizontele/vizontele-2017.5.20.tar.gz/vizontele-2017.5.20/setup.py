#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

version = '2017.05.20'
setup(
    name='vizontele',
    version=version,
    description='A tool to crawl and get sources of TV Shows from various Turkish web sites.',
    author='Halil Ozercan',
    author_email='halilozercan@gmail',
    url='https://github.com/halilozercan/vizontele',
    download_url='https://github.com/halilozercan/vizontele/tarball/' + version,
    entry_points={
        'console_scripts': [
            'vizontele = vizontele.bin:main',
        ],
    },
    install_requires=['requests', 'pyquery', 'demjson', 'pget', 'furl'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
