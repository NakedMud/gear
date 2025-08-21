"""
equipped.py

Python item subtype for equipped gear (armor, accessories, etc.)
Provides data storage and functionality for equipment items.
"""
import mudsys, storage, hooks

class EquippedData:
    """
    Data class for equipped items.
    Stores equipment-specific information like armor class, enchantments, etc.
    """
    __item_type__ = "equipped"
    
    def __init__(self, set_data=None):
        """Initialize equipped data, optionally from storage set"""
        self.armor_class = 0
        self.enchantment_level = 0
        self.durability = 100
        self.max_durability = 100
        self.material = ""
        self.special_properties = ""
        
        # Load from storage if provided
        if set_data:
            self.armor_class = set_data.readInt("armor_class")
            self.enchantment_level = set_data.readInt("enchantment_level") 
            self.durability = set_data.readInt("durability")
            self.max_durability = set_data.readInt("max_durability")
            self.material = set_data.readString("material")
            self.special_properties = set_data.readString("special_properties")
    
    def copy(self):
        """Create a copy of this equipped data"""
        new_data = EquippedData()
        new_data.armor_class = self.armor_class
        new_data.enchantment_level = self.enchantment_level
        new_data.durability = self.durability
        new_data.max_durability = self.max_durability
        new_data.material = self.material
        new_data.special_properties = self.special_properties
        return new_data
    
    def copyTo(self, other):
        """Copy this data to another EquippedData instance"""
        other.armor_class = self.armor_class
        other.enchantment_level = self.enchantment_level
        other.durability = self.durability
        other.max_durability = self.max_durability
        other.material = self.material
        other.special_properties = self.special_properties
    
    def store(self):
        """Store equipped data to a storage set"""
        set_data = storage.StorageSet()
        set_data.storeInt("armor_class", self.armor_class)
        set_data.storeInt("enchantment_level", self.enchantment_level)
        set_data.storeInt("durability", self.durability)
        set_data.storeInt("max_durability", self.max_durability)
        set_data.storeString("material", self.material)
        set_data.storeString("special_properties", self.special_properties)
        return set_data

def init_equipped():
    """Initialize the equipped item type"""
    # Register the equipped item type
    mudsys.item_add_type("equipped", EquippedData)
    
    # Add Python object getters/setters for equipped items
    def get_equipped_armor_class(obj):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            return data.armor_class if data else 0
        return 0
    
    def set_equipped_armor_class(obj, value):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            if data:
                data.armor_class = int(value)
    
    def get_equipped_enchantment(obj):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            return data.enchantment_level if data else 0
        return 0
    
    def set_equipped_enchantment(obj, value):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            if data:
                data.enchantment_level = int(value)
    
    def get_equipped_durability(obj):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            return data.durability if data else 100
        return 100
    
    def set_equipped_durability(obj, value):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            if data:
                data.durability = max(0, min(int(value), data.max_durability))
    
    def get_equipped_max_durability(obj):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            return data.max_durability if data else 100
        return 100
    
    def set_equipped_max_durability(obj, value):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            if data:
                data.max_durability = max(1, int(value))
                # Ensure current durability doesn't exceed max
                data.durability = min(data.durability, data.max_durability)
    
    def get_equipped_material(obj):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            return data.material if data else ""
        return ""
    
    def set_equipped_material(obj, value):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            if data:
                data.material = str(value)
    
    def get_equipped_properties(obj):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            return data.special_properties if data else ""
        return ""
    
    def set_equipped_properties(obj, value):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            if data:
                data.special_properties = str(value)

# Initialize immediately when module loads (after scripts are initialized)
init_equipped()
