# coding: utf-8

"""
Test serializing YAML
"""

from __future__ import absolute_import
import yaml as pyyaml

import re

from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.serializer import Serializer

def setup_module(module):
    module.serializer = Serializer('tiddlywebplugins.yaml')

def test_list_single_recipe_as_yaml():
    recipes = [Recipe('recipe' + str(name)) for name in xrange(1)]
    string = serializer.list_recipes(recipes)
    assert string == '- recipe0\n'

def test_list_recipes_as_yaml():
    recipes = [Recipe('recipe' + str(name)) for name in xrange(2)]
    string = serializer.list_recipes(recipes)
    assert string == '- recipe0\n- recipe1\n'

def test_list_bags_as_yaml():
    bags = [Bag('bag' + str(name)) for name in xrange(2)]
    string = serializer.list_bags(bags)
    assert string == '- bag0\n- bag1\n'

def test_list_bags_as_yaml_unicode():
    bags = [Bag(u'båg' + str(name)) for name in xrange(2)]
    string = serializer.list_bags(bags)
    assert string == u'- båg0\n- båg1\n'

def test_list_tiddlers_as_yaml():
    bag = Bag('test bag')
    tiddlers = [Tiddler('tiddler' + str(name)) for name in xrange(2)]
    [bag.add_tiddler(tiddler) for tiddler in tiddlers]
    string = serializer.list_tiddlers(bag)
    assert string.startswith(u"- bag: test bag\n")
    assert u"\n  title: tiddler1\n" in string
    assert u"\n  tags: []\n" in string
    o = pyyaml.load(string)
    assert re.match("^\d{14}$", o[0]['modified'])
    assert o[1]['tags'] == []
    assert o[1]['revision'] == 0

def test_recipe_as_yaml():
    recipe = Recipe('other')
    recipe.set_recipe([('foo', 'bar')])
    serializer.object = recipe
    string = serializer.to_string()
    assert string.startswith(u"desc: ''\n")
    assert u"\nrecipe:\n- - foo\n  - bar\n" in string

def test_recipe_yaml_roundtrip():
    recipe = Recipe('other')
    recipe.set_recipe([('bagbuzz', '')])
    recipe.policy.manage = ['a']
    recipe.policy.read = ['b']
    recipe.policy.create = ['c']
    recipe.policy.delete = ['d']
    recipe.policy.owner = 'e'
    serializer.object = recipe
    string = serializer.to_string()

    other_recipe = Recipe('other')
    serializer.object = other_recipe
    serializer.from_string(string)

    serializer.object = other_recipe
    other_string = serializer.to_string()

    assert string == other_string
