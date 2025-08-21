# Gear Module v1.0.0
Initial gear configuration system for NakedMud
### ADDED
- Nested class architecture with `GearConfig`, `Wielded`, and `Equipped` classes
- StorageSet-based gear configuration with clean flat storage format
- Gear OLC editor (`gearconfig` command) for runtime configuration
- Comprehensive helper functions for add/remove/validation operations
- Support for wielded items (weapons/tools) and equipped items (armor/accessories)
### FEATURES
- Wielded item categories: damage types, weapon categories, ranged types, materials, special properties, special attacks
- Equipped item categories: armor types, materials, special properties
- Auto-creates `misc/gear-config` with sensible defaults if missing
- Save confirmation on OLC exit following NakedMud patterns
- Full backward compatibility with existing gear configuration code
- Python scripting integration for dynamic item generation
### API
- Retrieval functions: `get_damage_types()`, `get_wielded_materials()`, `get_equipped_types()`, etc.
- Modification functions: `add_damage_type()`, `remove_wielded_material()`, `add_equipped_type()`, etc.
- Validation functions: `is_valid_damage_type()`, `is_valid_wielded_material()`, etc.
- Direct access to nested configuration objects for advanced usage
### INSTALL NOTES
- New installations get default gear configuration automatically
- Use `gearconfig` command to customize weapon types, materials, and properties
- Configuration changes immediately available to scripts and item generation
- Integrates with `wielded.py` and `equipped.py` item subtypes
