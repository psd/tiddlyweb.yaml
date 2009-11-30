"""
YAML TiddlyWeb serializer.
"""

import yaml

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
