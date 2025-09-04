"""
package: gear

Gear item types for NakedMud - equipped and wielded items.
Provides Python-based item subtypes for equipment and weapons.

This module extends the items system with:
- equipped: General equipment items (armor, accessories, etc.)
- wielded: Weapons and tools that can be wielded
"""
import os
import importlib

__all__ = [ ]

# compile a list of all our modules
for fl in os.listdir(__path__[0]):
    if fl.endswith(".py") and not (fl == "__init__.py" or fl.startswith(".")):
        __all__.append(fl[:-3])

# import all of our modules so they can register item types and hooks
__all__ = ['gear_aux', 'equipped', 'wielded', 'gear_config', 'gear_config_olc', 'gear_olc']
for module in __all__:
    importlib.import_module('.' + module, package=__name__)
