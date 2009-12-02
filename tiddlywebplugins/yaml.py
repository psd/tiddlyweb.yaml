"""
YAML TiddlyWeb serializer.
"""

from __future__ import absolute_import
import yaml as pyyaml

from tiddlyweb.serializations import SerializationInterface
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.policy import Policy

# hack to use the json base class for fat/skinny tiddler selection
from tiddlyweb.serializations.json import Serialization as SerializationInterface

__version__ = "0.1"
 
def init(config):
    # register serializer
    content_type = "text/yaml"
    config["extension_types"]["yaml"] = content_type
    config["serializers"][content_type] = [__name__, "text/yaml; charset=UTF-8"]

class Serialization(SerializationInterface):
    """
    Access TiddlyWeb resources using the YAML representation.
    """

    def __init__(self, environ=None):
        SerializationInterface.__init__(self, environ)
        self._bag_perms_cache = {}

    def _dump(self, o):
        return pyyaml.safe_dump(o, encoding=None, default_flow_style=False, allow_unicode=True)

    def list_recipes(self, recipes):
        """
        Create a YAML list of recipe names
        """
        return self._dump([recipe.name for recipe in recipes])

    def list_bags(self, bags):
        """
        Create a YAML list of bag names
        """
        return self._dump([bag.name for bag in bags])

    def list_tiddlers(self, bag):
        """
        List the tiddlers in a bag as YAML
        using the form described by self._tiddler_dict
        """
        return self._dump([self._tiddler_dict(tiddler) for
            tiddler in bag.gen_tiddlers()])
