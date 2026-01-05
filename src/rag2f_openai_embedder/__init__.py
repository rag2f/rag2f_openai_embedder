"""Source package for OpenAI Embedder plugin"""
import os

def get_plugin_path():
    """Return the absolute path to the plugin directory."""
    # This file is in src/, plugin root is parent directory
    return os.path.dirname(os.path.abspath(__file__))

# Expose version information when available
try:
    from ._version import __version__, __commit__, __distance__, __dirty__
except ImportError:
    __version__ = "unknown"
    __commit__ = "unknown"
    __distance__ = 0
    __dirty__ = False

__all__ = ["get_plugin_path", "__version__", "__commit__", "__distance__", "__dirty__"]
