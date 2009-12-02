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
    recipe.policy.manage = ['tinker']
    recipe.policy.read = ['tailor']
    recipe.policy.create = ['soldier']
    recipe.policy.delete = ['beggar']
    recipe.policy.owner = 'thief'
    recipe.set_recipe([('plum', 'fig')])
    serializer.object = recipe
    string = serializer.to_string()
    assert string.startswith(u"desc: ''\n")
    assert u"\n  manage:\n  - tinker\n" in string
    assert u"\n  read:\n  - tailor\n" in string
    assert u"\n  create:\n  - soldier\n" in string
    assert u"\n  delete:\n  - beggar\n" in string
    assert u"\n  owner: thief\n" in string
    assert u"\nrecipe:\n- - plum\n  - fig\n" in string

def test_recipe_as_and_from_yaml():
    recipe = Recipe('other')
    recipe.set_recipe([('bagbuzz', '')])
    serializer.object = recipe
    string = serializer.to_string()

    other_recipe = Recipe('other')
    serializer.object = other_recipe
    serializer.from_string(string)

    serializer.object = other_recipe
    other_string = serializer.to_string()

    assert string == other_string

def test_bag_as_yaml(): 
    bag = Bag('test bag')
    tiddlers = [Tiddler('tiddler number ' + str(name)) for name in xrange(2)]
    bag.desc = 'a bag of tiddlers'
    bag.policy.manage = ['NONE']
    bag.policy.delete = ['go away']
    serializer.object = bag
    string = serializer.to_string()
    assert string.startswith(u'desc: a bag of tiddlers\n')
    assert u"\n  delete:\n  - go away\n" in string
    assert u"\n  manage:\n  - NONE\n" in string

def test_bag_as_and_from_yaml():
    bag = Bag('other')
    serializer.object = bag
    string = serializer.to_string()

    other_bag = Bag('other')
    serializer.object = other_bag
    serializer.from_string(string)

    serializer.object = other_bag
    other_string = serializer.to_string()

    assert string == other_string

