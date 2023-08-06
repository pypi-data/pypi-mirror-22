# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-golem',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='Apache Software License',
    description='Django app for creating chatbots for Messenger and other platforms.',
    long_description=README,
    url='https://github.com/prihoda/django-golem',
    author='David Příhoda, Jakub Drdák',
    author_email='david.prihoda@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['networkx','requests','six','sqlparse','wit','wheel','redis',
    'pytz','unidecode','emoji','elasticsearch'],
)
