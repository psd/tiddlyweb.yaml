"""
YAML TiddlyWeb serializer.
"""

from __future__ import absolute_import
import yaml as pyyaml

from tiddlyweb.model.bag import Bag
from tiddlyweb.model.policy import Policy
from tiddlyweb.serializations import SerializationInterface

# temporarily use the json base class for fat/skinny tiddler selection
from tiddlyweb.serializations.json import Serialization as SerializationInterface

__version__ = "0.1"
 
def init(config):
    # register serializer
    content_type = "text/yaml"
    config["extension_types"]["yaml"] = content_type
    config["serializers"][content_type] = [__name__, "text/yaml; charset=UTF-8"]

def dump(o):
    return pyyaml.safe_dump(o, encoding=None, default_flow_style=False, allow_unicode=True)

def load(s):
    return pyyaml.load(s)

class Serialization(SerializationInterface):
    """
    Access TiddlyWeb resources using the YAML representation.
    """

    def __init__(self, environ=None):
        SerializationInterface.__init__(self, environ)
        self._bag_perms_cache = {}

    def list_recipes(self, recipes):
        """Creates a YAML representation of a list of recipe names."""
        return dump([recipe.name for recipe in recipes])

    def list_bags(self, bags):
        """Creates a YAML representation of a list of bag names."""
        return dump([bag.name for bag in bags])

    def list_tiddlers(self, bag):
        """Creates a YAML representation of the list of tiddlers in a bag."""
        return dump([self._tiddler_dict(tiddler) for
            tiddler in bag.gen_tiddlers()])

    def recipe_as(self, recipe):
        """Creates a YAML representation of a recipe."""
        policy = recipe.policy
        policy_dict = {}
        for key in Policy.attributes:
            policy_dict[key] = getattr(policy, key)
        return dump(dict(desc=recipe.desc, policy=policy_dict,
            recipe=recipe.get_recipe()))

    def as_recipe(self, recipe, input_string):
        """Creates a recipe from a YAML representation."""
        info = load(input_string)
        recipe.set_recipe(info.get('recipe', []))
        recipe.desc = info.get('desc', '')
        if info.get('policy', {}):
            recipe.policy = Policy()
            for key, value in info['policy'].items():
                recipe.policy.__setattr__(key, value)
        return recipe

    def bag_as(self, bag):
        """Creates a YAML representation of a bag."""
        policy = bag.policy
        policy_dict = {}
        for key in Policy.attributes:
            policy_dict[key] = getattr(policy, key)
        info = dict(policy=policy_dict, desc=bag.desc)
        return dump(info)
