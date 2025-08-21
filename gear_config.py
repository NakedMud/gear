"""
Gear Configuration Management

Uses nested class structure: Wielded and Equipped classes containing category-specific classes.
"""

import storage
import os

# Global gear configuration storage
gear_configs = {}
gear_config_file = "misc/gear-config"

class GearCategory:
    """Base class for gear categories (damage_types, materials, etc.)"""
    def __init__(self, items=None, set=None):
        if set is not None:
            self.items = []
            # Read direct name entries from the storage set
            for item_set in set.sets():
                name = item_set.readString("name")
                if name:  # Skip empty entries
                    self.items.append(name)
        else:
            self.items = items or []
    
    def store(self):
        """Returns a storage list with direct name entries"""
        items_list = storage.StorageList()
        for item in self.items:
            item_set = storage.StorageSet()
            item_set.storeString("name", item)
            items_list.add(item_set)
        return items_list
    
    def getItems(self): return self.items
    def addItem(self, item): 
        if item not in self.items:
            self.items.append(item)
    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)

class Wielded:
    """Wielded gear configuration"""
    def __init__(self, set=None):
        if set is not None:
            self.damage_types = GearCategory(set=set.readList("damage_types"))
            self.weapon_categories = GearCategory(set=set.readList("weapon_categories"))
            self.ranged_types = GearCategory(set=set.readList("ranged_types"))
            self.materials = GearCategory(set=set.readList("materials"))
            self.special_properties = GearCategory(set=set.readList("special_properties"))
            self.special_attacks = GearCategory(set=set.readList("special_attacks"))
        else:
            self.damage_types = GearCategory(["slashing", "bludgeoning", "piercing", "fire", "cold", "acid", "lightning"])
            self.weapon_categories = GearCategory(["melee", "ranged", "thrown"])
            self.ranged_types = GearCategory(["bow", "crossbow", "sling", "thrown", "firearm"])
            self.materials = GearCategory(["steel", "iron", "bronze", "silver", "gold", "mithril", "adamantine", "wood", "bone", "crystal"])
            self.special_properties = GearCategory(["magical", "blessed", "cursed", "flaming", "frost", "shock"])
            self.special_attacks = GearCategory(["vorpal", "sharpness", "speed", "accuracy"])
    
    def store(self):
        """Returns a storage set representation"""
        set = storage.StorageSet()
        set.storeList("damage_types", self.damage_types.store())
        set.storeList("weapon_categories", self.weapon_categories.store())
        set.storeList("ranged_types", self.ranged_types.store())
        set.storeList("materials", self.materials.store())
        set.storeList("special_properties", self.special_properties.store())
        set.storeList("special_attacks", self.special_attacks.store())
        return set

class Equipped:
    """Equipped gear configuration"""
    def __init__(self, set=None):
        if set is not None:
            self.armor_types = GearCategory(set=set.readList("armor_types"))
            self.materials = GearCategory(set=set.readList("materials"))
            self.special_properties = GearCategory(set=set.readList("special_properties"))
        else:
            self.armor_types = GearCategory(["light", "medium", "heavy", "shield"])
            self.materials = GearCategory(["leather", "chainmail", "plate", "cloth", "dragonscale"])
            self.special_properties = GearCategory(["magical", "blessed", "cursed", "protection", "resistance"])
    
    def store(self):
        """Returns a storage set representation"""
        set = storage.StorageSet()
        set.storeList("armor_types", self.armor_types.store())
        set.storeList("materials", self.materials.store())
        set.storeList("special_properties", self.special_properties.store())
        return set

class GearConfig:
    """Main gear configuration containing Wielded and Equipped"""
    def __init__(self, set=None):
        if set is not None:
            self.wielded = Wielded(set.readSet("wielded"))
            self.equipped = Equipped(set.readSet("equipped"))
        else:
            self.wielded = Wielded()
            self.equipped = Equipped()
    
    def store(self):
        """Returns a storage set representation"""
        set = storage.StorageSet()
        set.storeSet("wielded", self.wielded.store())
        set.storeSet("equipped", self.equipped.store())
        return set

def save_gear_configs(data=None):
    """Save all gear configurations - follows bulletin.py pattern"""
    set = storage.StorageSet()
    list = storage.StorageList()
    set.storeList("list", list)
    for key, val in gear_configs.items():
        one_set = storage.StorageSet()
        one_set.storeString("key", key)
        one_set.storeSet("val", val.store())
        list.add(one_set)
    set.write(gear_config_file)
    set.close()

def load_gear_configs():
    """Load gear configurations - follows bulletin.py pattern"""
    if not os.path.exists(gear_config_file):
        # Create default configuration
        create_default_gear_config()
        return
    
    set = storage.StorageSet(gear_config_file)
    for config in set.readList("list").sets():
        key = config.readString("key")
        gear_configs[key] = GearConfig(config.readSet("val"))
    set.close()

def create_default_gear_config():
    """Create default gear configuration file"""
    # Create main config with defaults already built into classes
    main_config = GearConfig()
    gear_configs["main"] = main_config
    save_gear_configs()

def get_gear_config():
    """Get main gear config"""
    return gear_configs.get("main", None)

# Helper functions for backward compatibility
def get_damage_types():
    """Get list of damage types"""
    config = gear_configs.get("main")
    if config:
        return config.wielded.damage_types.getItems()
    return []

def add_damage_type(damage_type):
    """Add a damage type"""
    config = gear_configs.get("main")
    if config:
        config.wielded.damage_types.addItem(damage_type)

def remove_damage_type(damage_type):
    """Remove a damage type"""
    config = gear_configs.get("main")
    if config:
        config.wielded.damage_types.removeItem(damage_type)

def get_weapon_categories():
    config = get_gear_config()
    return config.wielded.weapon_categories.getItems() if config else []

def get_ranged_types():
    config = get_gear_config()
    return config.wielded.ranged_types.getItems() if config else []

def get_wielded_materials():
    config = get_gear_config()
    return config.wielded.materials.getItems() if config else []

def get_wielded_special_properties():
    config = get_gear_config()
    return config.wielded.special_properties.getItems() if config else []

def get_wielded_special_attacks():
    config = get_gear_config()
    return config.wielded.special_attacks.getItems() if config else []

def get_equipped_types():
    config = get_gear_config()
    return config.equipped.armor_types.getItems() if config else []

def get_equipped_materials():
    config = get_gear_config()
    return config.equipped.materials.getItems() if config else []

def get_equipped_special_properties():
    config = get_gear_config()
    return config.equipped.special_properties.getItems() if config else []

def add_wielded_material(material):
    """Add a wielded material"""
    config = gear_configs.get("main")
    if config:
        config.wielded.materials.addItem(material)

def remove_wielded_material(material):
    """Remove a wielded material"""
    config = gear_configs.get("main")
    if config:
        config.wielded.materials.removeItem(material)

def add_wielded_special_property(prop):
    """Add a wielded special property"""
    config = gear_configs.get("main")
    if config:
        config.wielded.special_properties.addItem(prop)

def remove_wielded_special_property(prop):
    """Remove a wielded special property"""
    config = gear_configs.get("main")
    if config:
        config.wielded.special_properties.removeItem(prop)

def add_wielded_special_attack(attack):
    """Add a wielded special attack"""
    config = gear_configs.get("main")
    if config:
        config.wielded.special_attacks.addItem(attack)

def remove_wielded_special_attack(attack):
    """Remove a wielded special attack"""
    config = gear_configs.get("main")
    if config:
        config.wielded.special_attacks.removeItem(attack)

def add_equipped_type(equipped_type):
    """Add an equipped type"""
    config = gear_configs.get("main")
    if config:
        config.equipped.armor_types.addItem(equipped_type)

def remove_equipped_type(equipped_type):
    """Remove an equipped type"""
    config = gear_configs.get("main")
    if config:
        config.equipped.armor_types.removeItem(equipped_type)

def add_equipped_material(material):
    """Add an equipped material"""
    config = gear_configs.get("main")
    if config:
        config.equipped.materials.addItem(material)

def remove_equipped_material(material):
    """Remove an equipped material"""
    config = gear_configs.get("main")
    if config:
        config.equipped.materials.removeItem(material)

def add_equipped_special_property(prop):
    """Add an equipped special property"""
    config = gear_configs.get("main")
    if config:
        config.equipped.special_properties.addItem(prop)

def remove_equipped_special_property(prop):
    """Remove an equipped special property"""
    config = gear_configs.get("main")
    if config:
        config.equipped.special_properties.removeItem(prop)


# Validation functions for gear_olc.py
def is_valid_damage_type(damage_type):
    """Check if damage type is valid"""
    return damage_type in get_damage_types()

def is_valid_weapon_category(category):
    """Check if weapon category is valid"""
    return category in get_weapon_categories()

def is_valid_ranged_type(ranged_type):
    """Check if ranged type is valid"""
    return ranged_type in get_ranged_types()

def is_valid_wielded_material(material):
    """Check if wielded material is valid"""
    return material in get_wielded_materials()

def is_valid_equipped_material(material):
    """Check if equipped material is valid"""
    return material in get_equipped_materials()

def is_valid_wielded_special_property(prop):
    """Check if wielded special property is valid"""
    return prop in get_wielded_special_properties()

def is_valid_wielded_special_attack(attack):
    """Check if wielded special attack is valid"""
    return attack in get_wielded_special_attacks()

def is_valid_equipped_special_property(prop):
    """Check if equipped special property is valid"""
    return prop in get_equipped_special_properties()

# Initialize on module load
load_gear_configs()
