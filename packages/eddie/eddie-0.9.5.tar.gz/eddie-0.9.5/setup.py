#!/usr/bin/env python

import eddie


import pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_requirements(reqfile):
    try:
        requirements = pip.req.parse_requirements(
            reqfile, session=pip.download.PipSession())
    except TypeError:
        requirements = pip.req.parse_requirements(reqfile)

    return [str(item.req) for item in requirements if item.req]


setup(
    name='eddie',
    version=eddie.__version__,
    author=eddie.__author__,
    author_email=eddie.__email__,
    description='A lib to create chatbots',
    url='http://github.com/greenkey/eddie/',
    packages=['eddie', 'eddie.endpoints'],
    include_package_data=True,
    platforms='any',
    keywords=['chat', 'chatbot', 'telegram', 'twitter'],
    tests_require=['pytest'],
    install_requires=get_requirements('requirements.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
