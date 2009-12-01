# coding: utf-8

"""
Test serializing YAML
"""


from __future__ import absolute_import
import yaml as pyyaml

from tiddlyweb.model.bag import Bag
from tiddlyweb.serializer import Serializer

def setup_module(module):
    module.serializer = Serializer('tiddlywebplugins.yaml')

def test_list_bags_as_yaml():
    bags = [Bag('bag' + str(name)) for name in xrange(2)]
    string = serializer.list_bags(bags)
    assert string == '- bag0\n- bag1\n'

def test_list_unicode_bags_as_yaml():
    bags = [Bag(u'båg' + str(name)) for name in xrange(2)]
    string = serializer.list_bags(bags)
    assert string == u'- båg0\n- båg1\n'
