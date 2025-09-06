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
            self.special_properties = GearCategory(["versatile", "offhand", "magical", "blessed", "cursed"])
            self.special_attacks = GearCategory(["sharpness", "speed", "accuracy"])
    
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
            self.armor_types = GearCategory(["clothing", "light", "medium", "heavy", "shield"])
            self.materials = GearCategory(["leather", "cloth", "steel", "iron", "bronze", "silver", "gold", "mithril", "adamantine", "wood", "bone", "crystal" "dragonscale"])
            self.special_properties = GearCategory(["magical", "blessed", "cursed"])
    
    def store(self):
        """Returns a storage set representation"""
        set = storage.StorageSet()
        set.storeList("armor_types", self.armor_types.store())
        set.storeList("materials", self.materials.store())
        set.storeList("special_properties", self.special_properties.store())
        return set

class WornType:
    """Represents a worn type with positions and built-in flag"""
    def __init__(self, name="", positions=None, builtin=False):
        self.name = name
        self.positions = positions or []
        self.builtin = builtin
    
    def store(self):
        """Returns a storage set representation"""
        set = storage.StorageSet()
        set.storeString("name", self.name)
        set.storeBool("builtin", self.builtin)
        
        # Store positions as list
        positions_list = storage.StorageList()
        for position in self.positions:
            pos_set = storage.StorageSet()
            pos_set.storeString("position", position)
            positions_list.add(pos_set)
        set.storeList("positions", positions_list)
        return set

class WornTypes:
    """Worn types configuration"""
    def __init__(self, storage_set=None):
        """Initialize worn types from storage or create defaults"""
        self.worn_types = {}
        
        if storage_set and storage_set.contains("worn_types"):
            worn_types_list = storage_set.readList("worn_types")
            for worn_type_set in worn_types_list.sets():
                name = worn_type_set.readString("name")
                builtin = worn_type_set.readBool("builtin")
                
                positions = []
                if worn_type_set.contains("positions"):
                    positions_list = worn_type_set.readList("positions")
                    for pos_set in positions_list.sets():
                        position = pos_set.readString("position")
                        if position:
                            positions.append(position)
                
                worn_type = WornType(name, positions, builtin)
                self.worn_types[name] = worn_type
        
        # Always create defaults if we have no worn types (either no storage or empty storage)
        if not self.worn_types:
            self._create_default_worn_types()
            # Mark that we need to save these defaults
            self._needs_save = True
    
    def _create_default_worn_types(self):
        """Create default built-in worn types"""
        default_types = [
            ("shirt", ["torso", "arm", "arm"], True),  # Known C built-in
            ("pants", ["legs"], False),
            ("helmet", ["head"], False),
            ("boots", ["feet"], False),
            ("gloves", ["hands"], False),
            ("cloak", ["about body"], False),
            ("belt", ["waist"], False),
            ("ring", ["finger"], False),
            ("necklace", ["neck"], False),
            ("bracelet", ["wrist"], False)
        ]
        
        for name, positions, builtin in default_types:
            worn_type = WornType(name, positions, builtin)
            self.worn_types[name] = worn_type
    
    def store(self):
        """Returns a storage set representation"""
        set = storage.StorageSet()
        worn_types_list = storage.StorageList()
        for worn_type in self.worn_types.values():
            worn_types_list.add(worn_type.store())
        set.storeList("worn_types", worn_types_list)
        return set

class GearConfig:
    """Main gear configuration class"""
    def __init__(self, storage_set=None):
        """Initialize gear configuration from storage or create defaults"""
        if storage_set:
            # Load from storage
            self.wielded = Wielded(storage_set.readSet("wielded") if storage_set.contains("wielded") else None)
            self.equipped = Equipped(storage_set.readSet("equipped") if storage_set.contains("equipped") else None)
            self.worn_types = WornTypes(storage_set if storage_set.contains("worn_types") else None)
            
            # Check if any component created defaults and needs saving
            if hasattr(self.worn_types, '_needs_save') and self.worn_types._needs_save:
                # Save the configuration since we added defaults
                import threading
                threading.Timer(0.1, lambda: save_gear_configs()).start()
        else:
            # Create defaults
            self.wielded = Wielded()
            self.equipped = Equipped()
            self.worn_types = WornTypes()
    
    def store(self):
        """Returns a storage set representation"""
        set = storage.StorageSet()
        set.storeSet("wielded", self.wielded.store())
        set.storeSet("equipped", self.equipped.store())
        set.storeSet("worn_types", self.worn_types.store())
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

# Worn types helper functions
def get_worn_types():
    """Get list of all worn type names"""
    config = get_gear_config()
    if not config:
        return []
    return list(config.worn_types.worn_types.keys())

def get_worn_type_count():
    """Get the total number of worn types"""
    return len(get_worn_types())

def get_worn_type_object(worn_type):
    """Get a worn type object for OLC editing"""
    if worn_type_exists(worn_type):
        return {'name': worn_type}
    return None

def set_worn_type_positions(worn_type, positions):
    """Set positions for a worn type"""
    try:
        # Remove existing worn type
        remove_worn_type(worn_type)
        # Add it back with new positions
        return add_worn_type(worn_type, positions)
    except:
        return False

def get_available_body_positions():
    """Get list of available body positions"""
    # This should come from the body system, but for now return common positions
    return [
        'head', 'neck', 'shoulders', 'chest', 'back', 'arms', 'wrists', 
        'hands', 'fingers', 'waist', 'legs', 'feet', 'face', 'ears',
        'torso', 'abdomen', 'thighs', 'shins', 'ankles', 'toes'
    ]

def get_worn_type_positions(worn_type_name):
    """Get positions for a specific worn type"""
    config = get_gear_config()
    if not config:
        return []
    worn_type = config.worn_types.worn_types.get(worn_type_name)
    return worn_type.positions if worn_type else []

def worn_type_exists(worn_type_name):
    """Check if a worn type exists"""
    config = get_gear_config()
    if not config:
        return False
    return worn_type_name in config.worn_types.worn_types

def is_builtin_worn_type(worn_type_name):
    """Check if a worn type is built-in (cannot be deleted)"""
    config = get_gear_config()
    if not config:
        return False
    worn_type = config.worn_types.worn_types.get(worn_type_name)
    return worn_type.builtin if worn_type else False

def add_worn_type(worn_type_name, positions):
    """Add a new worn type with specified positions"""
    config = get_gear_config()
    if not config:
        return False
    
    if worn_type_exists(worn_type_name):
        return False
    
    # Create new worn type
    worn_type = WornType(worn_type_name, positions, False)
    config.worn_types.worn_types[worn_type_name] = worn_type
    
    # Register with C system
    try:
        import mudsys
        positions_str = ",".join(positions) if positions else ""
        mudsys.add_worn_type(worn_type_name, positions_str)
    except:
        pass
    
    # Save configuration
    save_gear_configs()
    return True

def remove_worn_type(worn_type_name):
    """Remove a worn type (only if not built-in)"""
    config = get_gear_config()
    if not config:
        return False
    
    if not worn_type_exists(worn_type_name):
        return False
    
    if is_builtin_worn_type(worn_type_name):
        return False
    
    # Remove from configuration
    del config.worn_types.worn_types[worn_type_name]
    
    # Remove from C system
    try:
        import mudsys
        mudsys.remove_worn_type(worn_type_name)
    except:
        pass
    
    # Save configuration
    save_gear_configs()
    return True

def update_worn_type_positions(worn_type_name, positions):
    """Update positions for an existing worn type"""
    config = get_gear_config()
    if not config:
        return False
    
    worn_type = config.worn_types.worn_types.get(worn_type_name)
    if not worn_type:
        return False
    
    # Update positions
    worn_type.positions = positions
    
    # Update C system
    try:
        import mudsys
        mudsys.remove_worn_type(worn_type_name)
        positions_str = ",".join(positions) if positions else ""
        mudsys.add_worn_type(worn_type_name, positions_str)
    except:
        pass
    
    # Save configuration
    save_gear_configs()
    return True

def get_available_body_positions():
    """Get list of available body position types from body.c"""
    try:
        import world
        return world.get_bodypos_types()
    except:
        # Fallback to basic position types
        return [
            "floating about head", "about body", "head", "face", "ear", "neck", 
            "torso", "arm", "wing", "wrist", "left hand", "right hand", "finger", 
            "waist", "leg", "left foot", "right foot", "hoof", "claw", 
            "tail", "held", "hands", "legs", "feet", "wings", "hooves"
        ]

def register_worn_types_with_c():
    """Register all worn types with the C worn system during module initialization"""
    config = get_gear_config()
    if not config:
        return
    
    registered_count = 0
    for worn_type in config.worn_types.worn_types.values():
        try:
            import mudsys
            # Convert positions list to comma-separated string for C function
            positions_str = ",".join(worn_type.positions) if worn_type.positions else ""
            mudsys.add_worn_type(worn_type.name, positions_str)
            registered_count += 1
        except Exception as e:
            # Type might already exist, which is fine
            pass
    
    if registered_count > 0:
        pass

# Initialize on module load
load_gear_configs()
# Register worn types with C system after loading
register_worn_types_with_c()
