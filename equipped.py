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
        self.worn_type = ""
        
        # Load from storage if provided
        if set_data:
            self.armor_class = set_data.readInt("armor_class")
            self.enchantment_level = set_data.readInt("enchantment_level") 
            self.durability = set_data.readInt("durability")
            self.max_durability = set_data.readInt("max_durability")
            self.material = set_data.readString("material")
            self.special_properties = set_data.readString("special_properties")
            self.worn_type = set_data.readString("worn_type")
    
    def copy(self):
        """Create a copy of this equipped data"""
        new_data = EquippedData()
        new_data.armor_class = self.armor_class
        new_data.enchantment_level = self.enchantment_level
        new_data.durability = self.durability
        new_data.max_durability = self.max_durability
        new_data.material = self.material
        new_data.special_properties = self.special_properties
        new_data.worn_type = self.worn_type
        return new_data
    
    def copyTo(self, other):
        """Copy this data to another EquippedData instance"""
        other.armor_class = self.armor_class
        other.enchantment_level = self.enchantment_level
        other.durability = self.durability
        other.max_durability = self.max_durability
        other.material = self.material
        other.special_properties = self.special_properties
        other.worn_type = self.worn_type
    
    def store(self):
        """Store equipped data to a storage set"""
        set_data = storage.StorageSet()
        set_data.storeInt("armor_class", self.armor_class)
        set_data.storeInt("enchantment_level", self.enchantment_level)
        set_data.storeInt("durability", self.durability)
        set_data.storeInt("max_durability", self.max_durability)
        set_data.storeString("material", self.material)
        set_data.storeString("special_properties", self.special_properties)
        set_data.storeString("worn_type", self.worn_type)
        return set_data

def init_equipped():
    """Initialize the equipped item type"""
    # Register the equipped item type
    mudsys.item_add_type("equipped", EquippedData)
    
    # Register commands
    mudsys.add_cmd("equip", None, cmd_equip, "player", 1)
    
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
    
    def get_equipped_worn_type(obj):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            return data.worn_type if data else ""
        return ""
    
    def set_equipped_worn_type(obj, value):
        if obj.istype("equipped"):
            data = obj.get_type_data("equipped")
            if data:
                data.worn_type = str(value)
    
    # Note: Python object getters/setters would be registered in C code if needed
    # For now, we can access worn_type directly through the data object

def get_equipped_positions(obj):
    """Get body positions for equipped item based on its worn_type"""
    if obj.istype("equipped"):
        data = obj.get_type_data("equipped")
        if data and data.worn_type:
            # Import here to avoid circular imports
            from . import gear_config
            return gear_config.get_worn_type_positions(data.worn_type)
    return ""

def expand_where_to_posnames(ch, obj, where):
    '''Expand body position types to specific position names using cmd_manip logic'''
    if not where:
        # Use the object's default wear locations if available
        if obj.istype("worn"):
            where = obj.worn_locs
        else:
            return None
    
    # Build type-to-parts mapping from character's actual body configuration
    type_to_parts = {}
    for part in ch.bodyparts:
        part_type = ch.get_bodypart_type(part)
        if part_type:
            if part_type not in type_to_parts:
                type_to_parts[part_type] = []
            type_to_parts[part_type].append(part)
    
    # Parse comma-separated position list
    positions = [pos.strip() for pos in where.split(',')]
    resolved_positions = []
    used_parts = set()  # Track which parts have already been selected
    
    for pos in positions:
        # If it's already a specific position name, use it directly
        if pos in ch.bodyparts:
            if pos not in used_parts:
                resolved_positions.append(pos)
                used_parts.add(pos)
        # If it's a type, find the first free position of that type
        elif pos in type_to_parts:
            found_free = False
            for part_name in type_to_parts[pos]:
                if part_name not in used_parts and not ch.get_equip(part_name):  # Check if slot is free and not already used
                    resolved_positions.append(part_name)
                    used_parts.add(part_name)
                    found_free = True
                    break
            if not found_free:
                # Try to find any unused part of this type, even if occupied
                for part_name in type_to_parts[pos]:
                    if part_name not in used_parts:
                        resolved_positions.append(part_name)
                        used_parts.add(part_name)
                        break
        else:
            # Unknown position type, pass through as-is
            if pos not in used_parts:
                resolved_positions.append(pos)
                used_parts.add(pos)
    
    return ', '.join(resolved_positions)

def do_equip(ch, obj, where=None):
    """Equip an object to a character, forcing it if necessary."""
        
    # Get equipped data to check worn_type
    data = obj.get_type_data("equipped")
    if not data or not data.worn_type:
        ch.send("This does not look like something you can equip.")
        return
    
    # Get positions this item wants to occupy
    from . import gear_config
    needed_positions = gear_config.get_worn_type_positions(data.worn_type)
    if not needed_positions:
        ch.send("This doesn't appear to be wearable.")
        return
    
    # Use provided where or default to the item's worn_type positions
    if where is None:
        where = ", ".join(needed_positions)
    
    # Expand body position types to specific position names
    expanded_where = expand_where_to_posnames(ch, obj, where)
    # Attempt to equip with forced=True and equipment_type='equipped' for layering
    result = ch.equip(obj, expanded_where, False, 'equipped')
    if result:
        import mud
        mud.message(ch, None, obj, None, True, "to_char", "You equip $o.")
        mud.message(ch, None, obj, None, True, "to_room", "$n equips $o.")
        
        # Run equip hook
        import hooks
        hooks.run("equip", hooks.build_info("ch obj", (ch, obj)))

def cmd_equip(ch, cmd, arg):
    """Usage: equip <item> [where]
    
    Attempts to equip armor from your inventory. Equipped items can layer
    over basic worn items but not over other equipped items.
    
    > equip chainmail
    > equip helmet head
    """
    try:
        import mud
        found, multi, where = mud.parse_args(ch, True, cmd, arg,
                                           "[the] obj.inv.multiple | [in] string")
    except: 
        return
    
    # Handle multiple argument parsing edge case
    if not multi and where != None and not "," in where:
        # reparse what we want!
        if not where in ch.bodyparts:
            where = None
            try:
                found, = mud.parse_args(ch, True, cmd, "'" + arg + "'", "[the] obj.inv")
            except: 
                return
    
    # Equip single or multiple items
    if multi == False:
        do_equip(ch, found, where)
    else:
        for obj in found:
            do_equip(ch, obj, where)

# Initialize immediately when module loads (after scripts are initialized)
init_equipped()
