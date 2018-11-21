#! /usr/bin/env python3
# -*- coding: utf8 -*-

from __future__ import print_function

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r', encoding='utf-8').read()

setup(
    name = "Oersetter",
    version = "1.1.2",
    author = "Maarten van Gompel",
    author_email = "proycon@anaproy.nl",
    description = ("Frisian Dutch Machine Translation Webservice"),
    license = "AGPLv3",
    keywords = "clam webservice rest nlp computational_linguistics rest",
    url = "https://github.com/proycon/oersetter-webservice",
    packages=['oersetter'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3"
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    package_data = {'oersetter':['*.wsgi','*.yml'] },
    include_package_data=True,
    install_requires=['CLAM >= 2.3']
)
