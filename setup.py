AUTHOR = 'Paul Downey'
AUTHOR_EMAIL = 'paul.downey@whatfettle.com'
NAME = 'tiddlywebplugins.yaml'
DESCRIPTION = 'TiddlyWeb YAML Serializer'
VERSION = '0.2'

import os
from setuptools import setup, find_packages

setup(
        namespace_packages = ['tiddlywebplugins'],
        name = NAME,
        version = VERSION,
        description = DESCRIPTION,
        long_description=file(os.path.join(os.path.dirname(__file__), 'README')).read(),
        author = AUTHOR,
        url = 'http://pypi.python.org/pypi/%s' % NAME,
        packages = find_packages(exclude='test'),
        author_email = AUTHOR_EMAIL,
        platforms = 'Posix; MacOS X; Windows',
        install_requires = ['setuptools', 'pyyaml', 'tiddlyweb', 'tiddlywebplugins.simplerizer'],
        )
