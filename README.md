# NakedMud Gear Configuration Module

A comprehensive gear configuration system for NakedMud that provides centralized management of weapon types, armor categories, materials, and special properties through a clean nested class structure and online editor.

## Installation

### Option 1: Download and Extract
1. Download the gear module files
2. Extract to your `lib/pymodules/gear/` directory
3. Restart your MUD or reload Python modules

### Option 2: Git Submodule
```bash
cd lib/pymodules/
git submodule add <repository-url> gear
git submodule update --init --recursive
```

## Commands Added

The module adds these admin commands:

- **`gearconfig`** - Online configuration editor for gear settings (admin level required)

## Configuration Files

- **Runtime config**: `lib/misc/gear-config` - Active configuration (auto-created with defaults)
- **Backup config**: `lib/misc/gear.old` - Preserved original configuration

## What It Does

The gear configuration module centralizes all weapon and armor type definitions, materials, special properties, and damage types into a single manageable system. It replaces scattered hardcoded lists with a structured, persistent configuration that can be modified at runtime through an intuitive menu system.

### Wielded Item Categories
- **Damage Types**: slashing, bludgeoning, piercing, fire, cold, acid, lightning
- **Weapon Categories**: melee, ranged, thrown
- **Ranged Types**: bow, crossbow, sling, thrown, firearm
- **Materials**: steel, iron, bronze, silver, gold, mithril, adamantine, wood, bone, crystal
- **Special Properties**: magical, blessed, cursed, flaming, frost, shock
- **Special Attacks**: vorpal, sharpness, speed, accuracy

### Equipped Item Categories
- **Armor Types**: light, medium, heavy, shield
- **Materials**: leather, chainmail, plate, cloth, dragonscale
- **Special Properties**: magical, blessed, cursed, protection, resistance

## Usage Example

```
> gearconfig
Gear Configuration Editor
1) Edit wielded item configuration
2) Edit equipped item configuration
Q) Quit

Enter choice: 1
Wielded Item Configuration
1) Damage types (7): slashing, bludgeoning, piercing, fire, cold...
2) Materials (10): steel, iron, bronze, silver, gold...
...

Enter choice: 1
Damage Types Configuration
Current damage types (7):
  1) slashing
  2) bludgeoning
  ...

1) Add damage type
2) Remove damage type
Q) Return to wielded menu

Enter choice: 1
Enter new damage type: psychic
Added damage type: psychic
```

## Technical Details

### Architecture

The module uses a nested class structure:
- **`GearConfig`** - Main container class
- **`Wielded`** - Contains wielded item categories
- **`Equipped`** - Contains equipped item categories  
- **`GearCategory`** - Base class for individual categories (damage_types, materials, etc.)

### Storage Format

Configuration is stored using NakedMud's StorageSet/StorageList system in a clean format:
```
list:=
  key: main
  val:-
    wielded :-
      damage_types :=
        name: slashing
        -
        name: bludgeoning
        -
```

### API Functions

#### Retrieval Functions
```python
import gear.gear_config as gear_config

# Get lists of items
damage_types = gear_config.get_damage_types()
materials = gear_config.get_wielded_materials()
equipped_types = gear_config.get_equipped_types()
```

#### Modification Functions
```python
# Add items
gear_config.add_damage_type("psychic")
gear_config.add_wielded_material("dragonbone")
gear_config.add_equipped_type("robes")

# Remove items
gear_config.remove_damage_type("psychic")
gear_config.remove_wielded_material("dragonbone")

# Save changes
gear_config.save_gear_configs()
```

#### Direct Access
```python
# Get the main configuration object
config = gear_config.get_gear_config()

# Access nested categories
wielded_materials = config.wielded.materials.getItems()
equipped_properties = config.equipped.special_properties.getItems()

# Modify directly
config.wielded.damage_types.addItem("necrotic")
config.equipped.armor_types.removeItem("shield")
```

### Wielded and Equipped Item Types

The module provides two item subtypes that scripts commonly interact with:

#### Wielded Items (`wielded.py`)
For weapons and tools. Available properties:
- **`damage_type`** - Type of damage (from gear config damage_types)
- **`weapon_category`** - melee, ranged, or thrown
- **`ranged_type`** - bow, crossbow, sling, etc. (if ranged)
- **`damage_dice`** - Damage dice string (e.g., "1d8+2")
- **`damage_bonus`** - Additional damage modifier (-10 to 20)
- **`hit_bonus`** - Attack roll modifier (-10 to 20)
- **`weapon_speed`** - Attack speed multiplier (0.1 to 5.0)
- **`reach`** - Weapon reach in combat (1 to 10)
- **`durability`** - Current condition (0 to max_durability)
- **`max_durability`** - Maximum condition (1+)
- **`material`** - Construction material (from gear config)
- **`special_attacks`** - Special attack properties

#### Equipped Items (`equipped.py`)
For armor and accessories. Available properties:
- **`armor_class`** - AC bonus provided (0 to 50)
- **`enchantment_level`** - Magical enhancement level (-10 to 10)
- **`durability`** - Current condition (0 to max_durability)
- **`max_durability`** - Maximum condition (1+)
- **`material`** - Construction material (from gear config)
- **`special_properties`** - Magical/special properties

### Script Integration

From within NakedMud scripts (see `html/tutorials/scripting/`):

```python
# In a weapon oproto script
import gear.gear_config as gear_config

# Set the item type to wielded
me.item_type = "wielded"

# Get available options from gear config
damage_types = gear_config.get_damage_types()
materials = gear_config.get_wielded_materials()

# Set weapon properties using the wielded item API
me.damage_type = mudsys.random_choice(damage_types)
me.weapon_category = "melee"
me.damage_dice = "1d8"
me.damage_bonus = 2
me.material = mudsys.random_choice(materials)
me.weapon_speed = 1.2
```

```python
# In an armor oproto script
import gear.gear_config as gear_config

# Set the item type to equipped
me.item_type = "equipped"

# Get available options from gear config
equipped_materials = gear_config.get_equipped_materials()
special_props = gear_config.get_equipped_special_properties()

# Set armor properties using the equipped item API
me.armor_class = 3
me.material = mudsys.random_choice(equipped_materials)
me.special_properties = mudsys.random_choice(special_props)
me.durability = 100
me.max_durability = 100
```

### Backward Compatibility

All existing helper functions are preserved. The module maintains full backward compatibility with existing code that relies on gear configuration data.

### OLC Integration

The module follows NakedMud's OLC patterns with automatic save confirmation on exit, similar to `socedit` and other editors. Changes are immediately available to scripts and other modules without restart.
