"""
wielded.py

Python item subtype for wielded weapons and tools.
Provides data storage and functionality for weapons, tools, and other wielded items.
"""
import mudsys, storage, hooks

class WieldedData:
    """
    Data class for wielded items.
    Stores weapon/tool-specific information like damage, weapon type, etc.
    """
    __item_type__ = "wielded"
    
    def __init__(self, set_data=None):
        """Initialize wielded data, optionally from storage set"""
        self.damage_type = "slashing"
        self.weapon_category = "melee"
        self.ranged_type = ""  # Only used if weapon_category is "ranged"
        self.damage_dice = "1d6"
        self.damage_bonus = 0
        self.hit_bonus = 0
        self.weapon_speed = 1.0
        self.reach = 1
        self.durability = 100
        self.max_durability = 100
        self.material = "steel"
        self.special_attacks = ""
        
        # Load from storage if provided
        if set_data:
            self.damage_type = set_data.readString("damage_type")
            self.weapon_category = set_data.readString("weapon_category")
            self.ranged_type = set_data.readString("ranged_type")
            self.damage_dice = set_data.readString("damage_dice")
            self.damage_bonus = set_data.readInt("damage_bonus")
            self.hit_bonus = set_data.readInt("hit_bonus")
            self.weapon_speed = set_data.readDouble("weapon_speed")
            self.reach = set_data.readInt("reach")
            self.durability = set_data.readInt("durability")
            self.max_durability = set_data.readInt("max_durability")
            self.material = set_data.readString("material")
            self.special_attacks = set_data.readString("special_attacks")
    
    def copy(self):
        """Create a copy of this wielded data"""
        new_data = WieldedData()
        new_data.weapon_type = self.weapon_type
        new_data.damage_dice = self.damage_dice
        new_data.damage_bonus = self.damage_bonus
        new_data.hit_bonus = self.hit_bonus
        new_data.weapon_speed = self.weapon_speed
        new_data.reach = self.reach
        new_data.durability = self.durability
        new_data.max_durability = self.max_durability
        new_data.material = self.material
        new_data.special_attacks = self.special_attacks
        return new_data
    
    def copy_to(self, other):
        """Copy this wielded data to another WieldedData object"""
        other.damage_type = self.damage_type
        other.weapon_category = self.weapon_category
        other.ranged_type = self.ranged_type
        other.damage_dice = self.damage_dice
        other.damage_bonus = self.damage_bonus
        other.hit_bonus = self.hit_bonus
        other.weapon_speed = self.weapon_speed
        other.reach = self.reach
        other.durability = self.durability
        other.max_durability = self.max_durability
        other.material = self.material
        other.special_attacks = self.special_attacks
    
    def store(self):
        """Store wielded data to a storage set"""
        set_data = storage.StorageSet()
        set_data.storeString("damage_type", self.damage_type)
        set_data.storeString("weapon_category", self.weapon_category)
        set_data.storeString("ranged_type", self.ranged_type)
        set_data.storeString("damage_dice", self.damage_dice)
        set_data.storeInt("damage_bonus", self.damage_bonus)
        set_data.storeInt("hit_bonus", self.hit_bonus)
        set_data.storeDouble("weapon_speed", self.weapon_speed)
        set_data.storeInt("reach", self.reach)
        set_data.storeInt("durability", self.durability)
        set_data.storeInt("max_durability", self.max_durability)
        set_data.storeString("material", self.material)
        set_data.storeString("special_attacks", self.special_attacks)
        return set_data

def init_wielded():
    """Initialize the wielded item type"""
    # Register the wielded item type
    mudsys.item_add_type("wielded", WieldedData)
    
    # Add Python object getters/setters for wielded items
    def get_wielded_weapon_type(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.weapon_type if data else "sword"
        return "sword"
    
    def set_wielded_weapon_type(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.weapon_type = str(value)
    
    def get_wielded_damage_dice(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.damage_dice if data else "1d6"
        return "1d6"
    
    def set_wielded_damage_dice(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.damage_dice = str(value)
    
    def get_wielded_damage_bonus(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.damage_bonus if data else 0
        return 0
    
    def set_wielded_damage_bonus(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.damage_bonus = int(value)
    
    def get_wielded_hit_bonus(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.hit_bonus if data else 0
        return 0
    
    def set_wielded_hit_bonus(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.hit_bonus = int(value)
    
    def get_wielded_weapon_speed(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.weapon_speed if data else 1.0
        return 1.0
    
    def set_wielded_weapon_speed(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.weapon_speed = float(value)
    
    def get_wielded_reach(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.reach if data else 1
        return 1
    
    def set_wielded_reach(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.reach = max(1, int(value))
    
    def get_wielded_durability(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.durability if data else 100
        return 100
    
    def set_wielded_durability(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.durability = max(0, min(int(value), data.max_durability))
    
    def get_wielded_max_durability(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.max_durability if data else 100
        return 100
    
    def set_wielded_max_durability(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.max_durability = max(1, int(value))
                # Ensure current durability doesn't exceed max
                data.durability = min(data.durability, data.max_durability)
    
    def get_wielded_material(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.material if data else "steel"
        return "steel"
    
    def set_wielded_material(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.material = str(value)
    
    def get_wielded_special_attacks(obj):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            return data.special_attacks if data else ""
        return ""
    
    def set_wielded_special_attacks(obj, value):
        if obj.istype("wielded"):
            data = obj.get_type_data("wielded")
            if data:
                data.special_attacks = str(value)

# Initialize immediately when module loads (after scripts are initialized)
init_wielded()
