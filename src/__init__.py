"""Source package for OpenAI Embedder plugin"""
import os

def get_plugin_path():
    """Return the absolute path to the plugin directory."""
    # This file is in src/, plugin root is parent directory
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
