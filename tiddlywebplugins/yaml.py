"""
YAML TiddlyWeb serializer.
"""

from __future__ import absolute_import
import yaml as pyyaml

from tiddlyweb.serializations import SerializationInterface
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.policy import Policy

class Serialization(SerializationInterface):
    """
    Access TiddlyWeb resources using the YAML representation.
    """

    def __init__(self, environ=None):
        SerializationInterface.__init__(self, environ)
        self._bag_perms_cache = {}

    def dump(self, o):
        return pyyaml.safe_dump(o, encoding=None, default_flow_style=False, allow_unicode=True)

    def list_recipes(self, recipes):
        """
        Create a YAML list of recipe names
        """
        return self.dump([recipe.name for recipe in recipes])

    def list_bags(self, bags):
        """
        Create a YAML list of bag names
        """
        return self.dump([bag.name for bag in bags])

