"""
YAML TiddlyWeb serializer.
"""

from __future__ import absolute_import
import yaml as pyyaml

from tiddlyweb.serializations import SerializationInterface
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.policy import Policy

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


    # rest of this module was stolen from the json serializer, 
    # .. maybe should be in the Serializer module? 
    def _tiddler_dict(self, tiddler):
        """
        Select fields from a tiddler to create a dictonary
        """
        unwanted_keys = ['text', 'store']
        wanted_keys = [attribute for attribute in tiddler.slots if
                attribute not in unwanted_keys]
        wanted_info = {}
        for attribute in wanted_keys:
            wanted_info[attribute] = getattr(tiddler, attribute, None)
        wanted_info['permissions'] = self._tiddler_permissions(tiddler)
        try:
            fat = self.environ['tiddlyweb.query'].get('fat', [None])[0]
            if fat:
                wanted_info['text'] = tiddler.text
        except KeyError:
            pass # tiddlyweb.query is not there
        return dict(wanted_info)

    def _tiddler_permissions(self, tiddler):
        """
        Make a list of the permissions the current user has
        on this tiddler.
        """
        def _read_bag_perms(environ, tiddler):
            """
            Read the permissions for the bag containing
            this tiddler.
            """
            perms = []
            if 'tiddlyweb.usersign' in environ:
                store = tiddler.store
                if store:
                    bag = Bag(tiddler.bag)
                    bag.skinny = True
                    bag = store.get(bag)
                    perms = bag.policy.user_perms(
                            environ['tiddlyweb.usersign'])
            return perms

        bag_name = tiddler.bag
        perms = []
        if len(self._bag_perms_cache):
            if bag_name in self._bag_perms_cache:
                perms = self._bag_perms_cache[bag_name]
            else:
                perms = _read_bag_perms(self.environ, tiddler)
        self._bag_perms_cache[bag_name] = perms
        return perms
