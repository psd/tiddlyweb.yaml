"""
YAML TiddlyWeb serializer.
"""

from __future__ import absolute_import
import yaml as pyyaml

from tiddlywebplugins.simplerizer import Simplerization as SerializationInterface

__version__ = "0.1"
 
def init(config):
    # register serializer
    content_type = "text/yaml"
    config["extension_types"]["yaml"] = content_type
    config["serializers"][content_type] = [__name__, "text/yaml; charset=UTF-8"]

class Serialization(SerializationInterface):
    """Access TiddlyWeb resources using the YAML representation."""

    def dump(self, object, type):
        """Dump a dictionary object to a YAML string."""
        return pyyaml.safe_dump(object, encoding=None, default_flow_style=False, allow_unicode=True)

    def load(self, input_string, type):
        """Load a dictionary object from a YAML string."""
        return pyyaml.load(input_string)
