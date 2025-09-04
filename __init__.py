"""
Gear Module for NakedMud

Provides item types and functionality for weapons, armor, and other equipment.
Includes wielded items (weapons, tools) and equipped items (armor, accessories).
"""
import os
import importlib

# Import all submodules to make them available
from . import gear_config
from . import gear_config_olc
from . import gear_olc
from . import wielded
from . import equipped

# Define what gets imported with "from gear import *"
__all__ = [
    'gear_config',
    'gear_config_olc', 
    'gear_olc',
    'wielded',
    'equipped'
]

# compile a list of all our modules
for fl in os.listdir(__path__[0]):
    if fl.endswith(".py") and not (fl == "__init__.py" or fl.startswith(".")):
        __all__.append(fl[:-3])

# import all of our modules so they can register item types and hooks
for module in __all__:
    importlib.import_module('.' + module, package=__name__)
