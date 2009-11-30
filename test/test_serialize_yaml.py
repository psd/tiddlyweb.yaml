
"""
Test serializing YAML
"""

import sys
sys.path.insert(0, '.')
import yaml

from tiddlyweb.model.bag import Bag
from tiddlyweb.serializer import Serializer

def setup_module(module):
    module.serializer = Serializer('yaml')

def assert_yaml(string):
    assert string.startswith('--')

def test_list_bags_as_rtf():
    bags = [Bag('bag' + str(name)) for name in xrange(2)]
    string = serializer.list_bags(bags)

    assert_yaml(string)
