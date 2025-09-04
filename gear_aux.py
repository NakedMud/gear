"""
Gear Auxiliary Data Classes

Provides auxiliary data classes for wielded and equipped items following the vitality system pattern.
These classes store gear-specific data as auxiliary data on objects instead of direct attributes.
"""
import storage, auxiliary, hooks, mudsys

################################################################################
# Wielded Auxiliary Data
################################################################################
class WieldedAuxData:
    """Holds wielded item data - damage, weapon stats, materials, etc."""
    
    def __init__(self, set=None):
        # Weapon properties
        self.damage_type = "slashing"
        self.weapon_category = "melee"
        self.ranged_type = ""
        self.damage_dice = "1d6"
        self.damage_bonus = 0
        self.hit_bonus = 0
        self.weapon_speed = 1.0
        self.reach = 1
        
        # Durability and materials
        self.durability = 100
        self.max_durability = 100
        self.material = "steel"
        self.special_attacks = ""
        
        # Read from storage if provided
        if set != None:
            self.read(set)
    
    def copyTo(self, to):
        """Copy wielded data to another instance"""
        to.damage_type = self.damage_type
        to.weapon_category = self.weapon_category
        to.ranged_type = self.ranged_type
        to.damage_dice = self.damage_dice
        to.damage_bonus = self.damage_bonus
        to.hit_bonus = self.hit_bonus
        to.weapon_speed = self.weapon_speed
        to.reach = self.reach
        to.durability = self.durability
        to.max_durability = self.max_durability
        to.material = self.material
        to.special_attacks = self.special_attacks
    
    def copy(self):
        """Create a copy of this wielded data"""
        newdata = WieldedAuxData()
        self.copyTo(newdata)
        return newdata
    
    def store(self):
        """Store wielded data to a storage set"""
        set = storage.StorageSet()
        set.storeString("damage_type", self.damage_type)
        set.storeString("weapon_category", self.weapon_category)
        set.storeString("ranged_type", self.ranged_type)
        set.storeString("damage_dice", self.damage_dice)
        set.storeInt("damage_bonus", self.damage_bonus)
        set.storeInt("hit_bonus", self.hit_bonus)
        set.storeDouble("weapon_speed", self.weapon_speed)
        set.storeInt("reach", self.reach)
        set.storeInt("durability", self.durability)
        set.storeInt("max_durability", self.max_durability)
        set.storeString("material", self.material)
        set.storeString("special_attacks", self.special_attacks)
        return set
    
    def read(self, set):
        """Read wielded data from a storage set"""
        if set.contains("damage_type"):
            self.damage_type = set.readString("damage_type")
        if set.contains("weapon_category"):
            self.weapon_category = set.readString("weapon_category")
        if set.contains("ranged_type"):
            self.ranged_type = set.readString("ranged_type")
        if set.contains("damage_dice"):
            self.damage_dice = set.readString("damage_dice")
        if set.contains("damage_bonus"):
            self.damage_bonus = set.readInt("damage_bonus")
        if set.contains("hit_bonus"):
            self.hit_bonus = set.readInt("hit_bonus")
        if set.contains("weapon_speed"):
            self.weapon_speed = set.readDouble("weapon_speed")
        if set.contains("reach"):
            self.reach = set.readInt("reach")
        if set.contains("durability"):
            self.durability = set.readInt("durability")
        if set.contains("max_durability"):
            self.max_durability = set.readInt("max_durability")
        if set.contains("material"):
            self.material = set.readString("material")
        if set.contains("special_attacks"):
            self.special_attacks = set.readString("special_attacks")

################################################################################
# Equipped Auxiliary Data
################################################################################
class EquippedAuxData:
    """Holds equipped item data - armor class, enchantments, materials, etc."""
    
    def __init__(self, set=None):
        # Armor properties
        self.armor_class = 0
        self.enchantment_level = 0
        
        # Durability and materials
        self.durability = 100
        self.max_durability = 100
        self.material = ""
        self.special_properties = ""
        
        # Read from storage if provided
        if set != None:
            self.read(set)
    
    def copyTo(self, to):
        """Copy equipped data to another instance"""
        to.armor_class = self.armor_class
        to.enchantment_level = self.enchantment_level
        to.durability = self.durability
        to.max_durability = self.max_durability
        to.material = self.material
        to.special_properties = self.special_properties
    
    def copy(self):
        """Create a copy of this equipped data"""
        newdata = EquippedAuxData()
        self.copyTo(newdata)
        return newdata
    
    def store(self):
        """Store equipped data to a storage set"""
        set = storage.StorageSet()
        set.storeInt("armor_class", self.armor_class)
        set.storeInt("enchantment_level", self.enchantment_level)
        set.storeInt("durability", self.durability)
        set.storeInt("max_durability", self.max_durability)
        set.storeString("material", self.material)
        set.storeString("special_properties", self.special_properties)
        return set
    
    def read(self, set):
        """Read equipped data from a storage set"""
        if set.contains("armor_class"):
            self.armor_class = set.readInt("armor_class")
        if set.contains("enchantment_level"):
            self.enchantment_level = set.readInt("enchantment_level")
        if set.contains("durability"):
            self.durability = set.readInt("durability")
        if set.contains("max_durability"):
            self.max_durability = set.readInt("max_durability")
        if set.contains("material"):
            self.material = set.readString("material")
        if set.contains("special_properties"):
            self.special_properties = set.readString("special_properties")

################################################################################
# Object Initialization Hooks
################################################################################
def init_object_gear(info):
    """Initialize gear data for new objects"""
    obj, = hooks.parse_info(info)
    
    # Initialize wielded data if object has wielded type
    if obj.istype("wielded"):
        aux = obj.getAuxiliary("wielded_data")
        # Data is already initialized with defaults by auxiliary system
    
    # Initialize equipped data if object has equipped type  
    if obj.istype("equipped"):
        aux = obj.getAuxiliary("equipped_data")
        # Data is already initialized with defaults by auxiliary system

################################################################################
# Python Object Property Getters/Setters
################################################################################
def get_wielded_damage_type(obj):
    """Get wielded damage type"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.damage_type
    return "slashing"

def set_wielded_damage_type(obj, value):
    """Set wielded damage type"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.damage_type = str(value)

def get_wielded_weapon_category(obj):
    """Get wielded weapon category"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.weapon_category
    return "melee"

def set_wielded_weapon_category(obj, value):
    """Set wielded weapon category"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.weapon_category = str(value)

def get_wielded_ranged_type(obj):
    """Get wielded ranged type"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.ranged_type
    return ""

def set_wielded_ranged_type(obj, value):
    """Set wielded ranged type"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.ranged_type = str(value)

def get_wielded_damage_dice(obj):
    """Get wielded damage dice"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.damage_dice
    return "1d6"

def set_wielded_damage_dice(obj, value):
    """Set wielded damage dice"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.damage_dice = str(value)

def get_wielded_damage_bonus(obj):
    """Get wielded damage bonus"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.damage_bonus
    return 0

def set_wielded_damage_bonus(obj, value):
    """Set wielded damage bonus"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.damage_bonus = int(value)

def get_wielded_hit_bonus(obj):
    """Get wielded hit bonus"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.hit_bonus
    return 0

def set_wielded_hit_bonus(obj, value):
    """Set wielded hit bonus"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.hit_bonus = int(value)

def get_wielded_weapon_speed(obj):
    """Get wielded weapon speed"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.weapon_speed
    return 1.0

def set_wielded_weapon_speed(obj, value):
    """Set wielded weapon speed"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.weapon_speed = float(value)

def get_wielded_reach(obj):
    """Get wielded reach"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.reach
    return 1

def set_wielded_reach(obj, value):
    """Set wielded reach"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.reach = int(value)

def get_wielded_durability(obj):
    """Get wielded durability"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.durability
    return 100

def set_wielded_durability(obj, value):
    """Set wielded durability"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.durability = max(0, min(int(value), aux.max_durability))

def get_wielded_max_durability(obj):
    """Get wielded max durability"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.max_durability
    return 100

def set_wielded_max_durability(obj, value):
    """Set wielded max durability"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.max_durability = max(1, int(value))
        aux.durability = min(aux.durability, aux.max_durability)

def get_wielded_material(obj):
    """Get wielded material"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.material
    return "steel"

def set_wielded_material(obj, value):
    """Set wielded material"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.material = str(value)

def get_wielded_special_attacks(obj):
    """Get wielded special attacks"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        return aux.special_attacks
    return ""

def set_wielded_special_attacks(obj, value):
    """Set wielded special attacks"""
    if obj.hasAuxiliary("wielded_data"):
        aux = obj.getAuxiliary("wielded_data")
        aux.special_attacks = str(value)

# Equipped getters/setters
def get_equipped_armor_class(obj):
    """Get equipped armor class"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        return aux.armor_class
    return 0

def set_equipped_armor_class(obj, value):
    """Set equipped armor class"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        aux.armor_class = int(value)

def get_equipped_enchantment(obj):
    """Get equipped enchantment level"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        return aux.enchantment_level
    return 0

def set_equipped_enchantment(obj, value):
    """Set equipped enchantment level"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        aux.enchantment_level = int(value)

def get_equipped_durability(obj):
    """Get equipped durability"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        return aux.durability
    return 100

def set_equipped_durability(obj, value):
    """Set equipped durability"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        aux.durability = max(0, min(int(value), aux.max_durability))

def get_equipped_max_durability(obj):
    """Get equipped max durability"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        return aux.max_durability
    return 100

def set_equipped_max_durability(obj, value):
    """Set equipped max durability"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        aux.max_durability = max(1, int(value))
        aux.durability = min(aux.durability, aux.max_durability)

def get_equipped_material(obj):
    """Get equipped material"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        return aux.material
    return ""

def set_equipped_material(obj, value):
    """Set equipped material"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        aux.material = str(value)

def get_equipped_properties(obj):
    """Get equipped special properties"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        return aux.special_properties
    return ""

def set_equipped_properties(obj, value):
    """Set equipped special properties"""
    if obj.hasAuxiliary("equipped_data"):
        aux = obj.getAuxiliary("equipped_data")
        aux.special_properties = str(value)

################################################################################
# Initialization
################################################################################

# Install auxiliary data for objects
auxiliary.install("wielded_data", WieldedAuxData, "object")
auxiliary.install("equipped_data", EquippedAuxData, "object")

# Add hooks
hooks.add("init_object", init_object_gear)

# Add Python object getters/setters - these need to be registered after C extension is loaded
# For now, we'll skip these and rely on the existing item type system
# TODO: These would need to be registered via C extension or existing PyObj system

def __unload__():
    """Clean up when module is unloaded"""
    hooks.remove("init_object", init_object_gear)
