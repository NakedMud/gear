"""
wielded.py

Python item subtype for wielded weapons and tools.
Provides data storage and functionality for weapons, tools, and other wielded items.
"""
import mudsys, storage, hooks, mud

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
        self.special_properties = ""
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
            self.special_properties = set_data.readString("special_properties")
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
        new_data.special_properties = self.special_properties
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
        other.special_properties = self.special_properties
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
        set_data.storeString("special_properties", self.special_properties)
        set_data.storeString("special_attacks", self.special_attacks)
        return set_data

def do_wield(ch, obj, where):
    """Handle wielding an object"""
    if not obj.istype("wielded"):
        ch.send("But " + ch.see_as(obj) + " is not wieldable.")
        return
    
    # Get wielded data to check special properties
    data = obj.get_type_data("wielded")
    if not data:
        ch.send("That item has no wielding data.")
        return
    
    # Parse special properties
    properties = [p.strip().lower() for p in data.special_properties.split(',') if p.strip()]
    
    # Validate wield location based on properties
    if where:
        where = where.lower()
        if where in ["both", "both hands", "two hands"]:
            if "versatile" not in properties:
                ch.send("That weapon cannot be wielded with both hands.")
                return
            where = "left hand,right hand"
        elif where in ["offhand", "off hand", "left hand"]:
            if "offhand" not in properties:
                ch.send("That weapon cannot be wielded in the offhand.")
                return
            where = "left hand"
        elif where in ["primary", "main hand", "right hand"]:
            where = "right hand"
    
    # Default to primary hand (right hand) if no position specified
    if where is None:
        where = "right hand"
    
    # Attempt to wield the item (force=True since wielded items aren't "worn" type)
    if ch.equip(obj, where, True):
        if where and "," in where:
            ch.send("You wield " + ch.see_as(obj) + " with both hands.")
            mud.message(ch, None, obj, None, True, "to_room", "$n wields $o with both hands.")
        else:
            ch.send("You wield " + ch.see_as(obj) + ".")
            mud.message(ch, None, obj, None, True, "to_room", "$n wields $o.")
        
        # Run wield hook
        hooks.run("wield", hooks.build_info("ch obj", (ch, obj)))

def cmd_wield(ch, cmd, arg):
    """Usage: wield <item> [where]
    
    Attempts to wield a weapon from your inventory. You can specify where
    to wield it:
    
    > wield sword primary     (primary hand - right hand)
    > wield dagger offhand    (offhand - left hand, requires 'offhand' property)
    > wield staff both        (both hands, requires 'versatile' property)
    
    If no location is specified, the weapon will be wielded in your primary hand (right hand)."""
    try:
        found, multi, where = mud.parse_args(ch, True, cmd, arg,
                                           "[the] obj.inv.multiple | [in] string")
    except: 
        return
    
    # Handle multiple argument parsing edge case
    if not multi and where != None:
        valid_locations = ["primary", "main", "offhand", "off", "both", "two"]
        if not any(loc in where.lower() for loc in valid_locations):
            where = None
            try:
                found, = mud.parse_args(ch, True, cmd, "'" + arg + "'", "[the] obj.inv")
            except: 
                return
    
    # Wield single or multiple items
    if multi == False:
        do_wield(ch, found, where)
    else:
        for obj in found:
            do_wield(ch, obj, where)

def get_durability_condition(durability, max_durability):
    """Get condition description based on durability percentage"""
    if max_durability <= 0:
        return "broken"
    
    percentage = (durability * 100) // max_durability
    
    if percentage >= 95:
        return "in perfect condition"
    elif percentage >= 80:
        return "in excellent condition"
    elif percentage >= 65:
        return "in good condition"
    elif percentage >= 50:
        return "showing some wear"
    elif percentage >= 35:
        return "well worn"
    elif percentage >= 20:
        return "badly worn"
    elif percentage >= 5:
        return "in poor condition"
    else:
        return "nearly broken"

def append_wield_hook(info):
    """Hook to append durability condition to wielded item descriptions"""
    obj, = hooks.parse_info(info)
    
    if obj.istype("wielded"):
        data = obj.get_type_data("wielded")
        if data and data.max_durability > 0:
            condition = get_durability_condition(data.durability, data.max_durability)
            obj.desc = obj.desc + " It is " + condition + "."

def cmd_unwield(ch, cmd, arg):
    """Usage: unwield <item>
    
    Removes a wielded weapon from your hands."""
    try:
        found, = mud.parse_args(ch, True, cmd, arg, "[the] obj.eq")
    except: 
        return
    
    if not found.istype("wielded"):
        ch.send("But " + ch.see_as(found) + " is not wielded.")
        return
    
    # Move the object from equipment to inventory
    found.carrier = ch
    
    # Check if it succeeded
    if found.carrier != ch:
        ch.send("You were unable to unwield " + ch.see_as(found) + ".")
    else:
        ch.send("You stop wielding " + ch.see_as(found) + ".")
        mud.message(ch, None, found, None, True, "to_room", "$n stops wielding $o.")
        
        # Run unwield hook
        hooks.run("unwield", hooks.build_info("ch obj", (ch, found)))

def cmd_gear(ch, cmd, arg):
    """Usage: gear
    
    Lists all your currently wielded, equipped, and worn items."""
    
    wielded_items = []
    equipped_items = []
    worn_items = []
    
    # Categorize equipped items by type
    for obj in ch.eq:
        if obj.istype("wielded"):
            wielded_items.append(obj)
        elif obj.istype("equipped"):
            equipped_items.append(obj)
        else:
            worn_items.append(obj)
    
    ch.send("{cYour Current Gear:{n")
    ch.send("=" * 50)
    
    # Show wielded items
    if wielded_items:
        ch.send("\n{yWielded:{n")
        for obj in wielded_items:
            where = ch.get_slots(obj)
            ch.send("  " + ch.see_as(obj) + " (" + where + ")")
    
    # Show equipped items  
    if equipped_items:
        ch.send("\n{gEquipped:{n")
        for obj in equipped_items:
            where = ch.get_slots(obj)
            ch.send("  " + ch.see_as(obj) + " (" + where + ")")
    
    # Show worn items
    if worn_items:
        ch.send("\n{cWorn:{n")
        for obj in worn_items:
            where = ch.get_slots(obj)
            ch.send("  " + ch.see_as(obj) + " (" + where + ")")
    
    if not wielded_items and not equipped_items and not worn_items:
        ch.send("You are not wearing, wielding, or equipping anything.")

def init_wielded():
    """Initialize the wielded item type"""
    # Register the wielded item type
    mudsys.item_add_type("wielded", WieldedData)
    
    # Register commands
    mudsys.add_cmd("wield", None, cmd_wield, "player", 1)
    mudsys.add_cmd("unwield", None, cmd_unwield, "player", 1)
    mudsys.add_cmd("gear", None, cmd_gear, "player", 1)
    
    # Register hooks
    hooks.add("append_description", append_wield_hook)
    
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
