"""
gear_olc.py

OLC (Online Creation) editors for gear item types.
Provides editing interfaces for equipped and wielded item data.
"""
import mudsys
import olc
from . import gear_config

# Equipped item OLC menu choices
EQUIPPED_ARMOR_CLASS = 1
EQUIPPED_ENCHANTMENT = 2
EQUIPPED_DURABILITY = 3
EQUIPPED_MAX_DURABILITY = 4
EQUIPPED_MATERIAL = 5
EQUIPPED_PROPERTIES = 6
EQUIPPED_WORN_TYPE = 7

def equipped_menu(sock, data):
    """Display the equipped item editing menu"""
    valid_materials = gear_config.get_equipped_materials()
    valid_properties = gear_config.get_equipped_special_properties()
    valid_worn_types = gear_config.get_worn_types()
    
    # Get positions for current worn type
    worn_type_positions = ""
    if data.worn_type:
        positions = gear_config.get_worn_type_positions(data.worn_type)
        if positions:
            worn_type_positions = ", ".join(positions)
    
    sock.send_raw("""
{g+{n==============================================================================
{cEquipped Item Editor{n
{g+{n==============================================================================

{c1{n) Armor Class      : {y%d{n
{c2{n) Enchantment Level: {y%d{n
{c3{n) Durability       : {y%d{n
{c4{n) Max Durability   : {y%d{n
{c5{n) Material         : {y%s{n {g(Valid: %s){n
{c6{n) Special Properties: {y%s{n {g(Valid: %s){n
{c7{n) Worn Type        : {y%s{n {g(Valid: %s){n
{g   equips to          : {c%s{n

{cQ{n) Quit

Enter choice: """ % (
        data.armor_class,
        data.enchantment_level,
        data.durability,
        data.max_durability,
        data.material or "none",
        ", ".join(valid_materials[:3]) + ("..." if len(valid_materials) > 3 else ""),
        data.special_properties or "none",
        ", ".join(valid_properties[:3]) + ("..." if len(valid_properties) > 3 else ""),
        data.worn_type or "none",
        ", ".join(valid_worn_types[:3]) + ("..." if len(valid_worn_types) > 3 else ""),
        worn_type_positions or "none"
    ))

def equipped_chooser(sock, data, option):
    """Handle equipped item menu choices"""
    choice = option.upper()
    
    if choice == '1':
        sock.send_raw("Enter new armor class (0-50): ")
        return EQUIPPED_ARMOR_CLASS
    elif choice == '2':
        sock.send_raw("Enter enchantment level (-10 to +10): ")
        return EQUIPPED_ENCHANTMENT
    elif choice == '3':
        sock.send_raw("Enter current durability (0 to %d): " % data.max_durability)
        return EQUIPPED_DURABILITY
    elif choice == '4':
        sock.send_raw("Enter maximum durability (1-1000): ")
        return EQUIPPED_MAX_DURABILITY
    elif choice == '5':
        sock.send_raw("Enter material type: ")
        return EQUIPPED_MATERIAL
    elif choice == '6':
        sock.send_raw("Enter special properties: ")
        return EQUIPPED_PROPERTIES
    elif choice == '7':
        # Show available worn types like worn.c does
        valid_worn_types = gear_config.get_worn_types()
        sock.send_raw("Equippable item types:\n")
        
        # Display types in columns like worn.c
        col = 0
        for worn_type in sorted(valid_worn_types):
            col += 1
            if col % 4 == 0:
                sock.send_raw("  %-14s\n" % worn_type)
            else:
                sock.send_raw("  %-14s   " % worn_type)
        
        # Add final newline if needed
        if col % 4 != 0:
            sock.send_raw("\n")
            
        sock.send_raw("enter choice: ")
        return EQUIPPED_WORN_TYPE
    else:
        return olc.MENU_CHOICE_INVALID

def equipped_parser(sock, data, choice, arg):
    """Parse equipped item input"""
    if choice == EQUIPPED_ARMOR_CLASS:
        try:
            value = int(arg)
            if 0 <= value <= 50:
                data.armor_class = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == EQUIPPED_ENCHANTMENT:
        try:
            value = int(arg)
            if -10 <= value <= 10:
                data.enchantment_level = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == EQUIPPED_DURABILITY:
        try:
            value = int(arg)
            if 0 <= value <= data.max_durability:
                data.durability = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == EQUIPPED_MAX_DURABILITY:
        try:
            value = int(arg)
            if 1 <= value <= 1000:
                data.max_durability = value
                # Ensure current durability doesn't exceed max
                data.durability = min(data.durability, data.max_durability)
                return True
        except ValueError:
            pass
        return False
    
    elif choice == EQUIPPED_MATERIAL:
        material = arg.strip().lower()
        if gear_config.is_valid_equipped_material(material):
            data.material = material
            return True
        else:
            valid_materials = gear_config.get_equipped_materials()
            sock.send_raw("Invalid material. Valid materials are: %s\n" % ", ".join(valid_materials))
            return False
    
    elif choice == EQUIPPED_PROPERTIES:
        # Validate properties (comma-separated list)
        properties = [p.strip().lower() for p in arg.split(',') if p.strip()]
        valid_properties = gear_config.get_equipped_special_properties()
        invalid_props = [p for p in properties if p not in valid_properties]
        
        if invalid_props:
            sock.send_raw("Invalid properties: %s\nValid properties are: %s\n" % 
                         (", ".join(invalid_props), ", ".join(valid_properties)))
            return False
        else:
            data.special_properties = ", ".join(properties)
            return True
    
    elif choice == EQUIPPED_WORN_TYPE:
        worn_type = arg.strip().lower()
        if gear_config.worn_type_exists(worn_type):
            data.worn_type = worn_type
            return True
        else:
            valid_worn_types = gear_config.get_worn_types()
            sock.send_raw("Invalid worn type. Valid worn types are: %s\n" % ", ".join(valid_worn_types))
            return False
    
    return False

def equipped_to_proto(data):
    """Generate prototype code for equipped items"""
    lines = []
    if data.armor_class > 0:
        lines.append("me.get_type_data(\"equipped\").armor_class = %d" % data.armor_class)
    if data.enchantment_level != 0:
        lines.append("me.get_type_data(\"equipped\").enchantment_level = %d" % data.enchantment_level)
    if data.durability != 100:
        lines.append("me.get_type_data(\"equipped\").durability = %d" % data.durability)
    if data.max_durability != 100:
        lines.append("me.get_type_data(\"equipped\").max_durability = %d" % data.max_durability)
    if data.material:
        lines.append("me.get_type_data(\"equipped\").material = \"%s\"" % data.material)
    if data.special_properties:
        lines.append("me.get_type_data(\"equipped\").special_properties = \"%s\"" % data.special_properties)
    if data.worn_type:
        lines.append("me.get_type_data(\"equipped\").worn_type = \"%s\"" % data.worn_type)
    return "\n".join(lines) + ("\n" if lines else "")

# Wielded item OLC menu choices
WIELDED_DAMAGE_TYPE = 1
WIELDED_WEAPON_CATEGORY = 2
WIELDED_RANGED_TYPE = 11  # Only shown for ranged weapons
WIELDED_DAMAGE_DICE = 3
WIELDED_DAMAGE_BONUS = 4
WIELDED_HIT_BONUS = 5
WIELDED_WEAPON_SPEED = 6
WIELDED_REACH = 7
WIELDED_DURABILITY = 8
WIELDED_MAX_DURABILITY = 9
WIELDED_MATERIAL = 10
WIELDED_SPECIAL_PROPERTIES = 12
WIELDED_SPECIAL_ATTACKS = 13

def wielded_menu(sock, data):
    """Display the wielded item editing menu"""
    valid_damage_types = gear_config.get_damage_types()
    valid_categories = gear_config.get_weapon_categories()
    valid_ranged_types = gear_config.get_ranged_types()
    valid_materials = gear_config.get_wielded_materials()
    valid_properties = gear_config.get_wielded_special_properties()
    valid_attacks = gear_config.get_wielded_special_attacks()
    
    # Show ranged type only if weapon category is ranged
    ranged_display = ""
    if data.weapon_category == "ranged":
        ranged_display = "\r\n{gB) Ranged Type      : {c%s {g(Valid: %s)" % (
            data.ranged_type or "none",
            ", ".join(valid_ranged_types[:3]) + ("..." if len(valid_ranged_types) > 3 else "")
        )
    
    sock.send_raw(
        "{g1) Damage Type     : {c%s {g(Valid: %s)\r\n"
        "{g2) Weapon Category : {c%s {g(Valid: %s)%s\r\n"
        "{g3) Damage Dice     : {c%s\r\n"
        "{g4) Damage Bonus    : {c%+d\r\n"
        "{g5) Hit Bonus       : {c%+d\r\n"
        "{g6) Weapon Speed    : {c%.1f\r\n"
        "{g7) Reach           : {c%d\r\n"
        "{g8) Durability      : {c%d / %d\r\n"
        "{g9) Max Durability  : {c%d\r\n"
        "{gA) Material        : {c%s {g(Valid: %s)\r\n"
        "{gC) Special Properties: {c%s {g(Valid: %s)\r\n"
        "{g0) Special Attacks : {c%s {g(Valid: %s)\r\n" % (
            data.damage_type,
            ", ".join(valid_damage_types[:3]) + ("..." if len(valid_damage_types) > 3 else ""),
            data.weapon_category,
            ", ".join(valid_categories[:3]) + ("..." if len(valid_categories) > 3 else ""),
            ranged_display,
            data.damage_dice,
            data.damage_bonus,
            data.hit_bonus,
            data.weapon_speed,
            data.reach,
            data.durability,
            data.max_durability,
            data.max_durability,
            data.material,
            ", ".join(valid_materials[:3]) + ("..." if len(valid_materials) > 3 else ""),
            data.special_properties,
            ", ".join(valid_properties[:3]) + ("..." if len(valid_properties) > 3 else ""),
            data.special_attacks,
            ", ".join(valid_attacks[:3]) + ("..." if len(valid_attacks) > 3 else "")
        )
    )

def wielded_chooser(sock, data, option):
    """Handle wielded item menu choices"""
    choice = option.upper()
    
    if choice == '1':
        sock.send_raw("Enter damage type (slashing, bludgeoning, piercing): ")
        return WIELDED_DAMAGE_TYPE
    elif choice == '2':
        sock.send_raw("Enter weapon category (melee, ranged, thrown): ")
        return WIELDED_WEAPON_CATEGORY
    elif choice == 'B' and data.weapon_category == "ranged":
        sock.send_raw("Enter ranged type (bow, crossbow, sling, thrown, firearm): ")
        return WIELDED_RANGED_TYPE
    elif choice == '3':
        sock.send_raw("Enter damage dice (e.g., 1d6, 2d4+1): ")
        return WIELDED_DAMAGE_DICE
    elif choice == '4':
        sock.send_raw("Enter damage bonus (-10 to +10): ")
        return WIELDED_DAMAGE_BONUS
    elif choice == '5':
        sock.send_raw("Enter hit bonus (-10 to +10): ")
        return WIELDED_HIT_BONUS
    elif choice == '6':
        sock.send_raw("Enter weapon speed (0.1 to 5.0): ")
        return WIELDED_WEAPON_SPEED
    elif choice == '7':
        sock.send_raw("Enter reach (1-10): ")
        return WIELDED_REACH
    elif choice == '8':
        sock.send_raw("Enter current durability (0 to %d): " % data.max_durability)
        return WIELDED_DURABILITY
    elif choice == '9':
        sock.send_raw("Enter maximum durability (1-1000): ")
        return WIELDED_MAX_DURABILITY
    elif choice == 'A':
        sock.send_raw("Enter material type: ")
        return WIELDED_MATERIAL
    elif choice == 'C':
        sock.send_raw("Enter special properties: ")
        return WIELDED_SPECIAL_PROPERTIES
    elif choice == '0':
        sock.send_raw("Enter special attacks: ")
        return WIELDED_SPECIAL_ATTACKS
    else:
        return olc.MENU_CHOICE_INVALID

def wielded_parser(sock, data, choice, arg):
    """Parse wielded item input"""
    if choice == WIELDED_DAMAGE_TYPE:
        damage_type = arg.strip().lower()
        if gear_config.is_valid_damage_type(damage_type):
            data.damage_type = damage_type
            return True
        else:
            valid_types = gear_config.get_damage_types()
            sock.send_raw("Invalid damage type. Valid types are: %s\n" % ", ".join(valid_types))
            return False
    
    elif choice == WIELDED_WEAPON_CATEGORY:
        category = arg.strip().lower()
        if gear_config.is_valid_weapon_category(category):
            data.weapon_category = category
            # Clear ranged type if switching away from ranged
            if category != "ranged":
                data.ranged_type = ""
            return True
        else:
            valid_categories = gear_config.get_weapon_categories()
            sock.send_raw("Invalid weapon category. Valid categories are: %s\n" % ", ".join(valid_categories))
            return False
    
    elif choice == WIELDED_RANGED_TYPE:
        ranged_type = arg.strip().lower()
        if gear_config.is_valid_ranged_type(ranged_type):
            data.ranged_type = ranged_type
            return True
        else:
            valid_types = gear_config.get_ranged_types()
            sock.send_raw("Invalid ranged type. Valid types are: %s\n" % ", ".join(valid_types))
            return False
    
    elif choice == WIELDED_DAMAGE_DICE:
        # Basic validation for dice notation
        arg = arg.strip()
        if arg and ('d' in arg.lower() or arg.isdigit()):
            data.damage_dice = arg
            return True
        return False
    
    elif choice == WIELDED_DAMAGE_BONUS:
        try:
            value = int(arg)
            if -10 <= value <= 20:
                data.damage_bonus = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == WIELDED_HIT_BONUS:
        try:
            value = int(arg)
            if -10 <= value <= 20:
                data.hit_bonus = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == WIELDED_WEAPON_SPEED:
        try:
            value = float(arg)
            if 0.1 <= value <= 5.0:
                data.weapon_speed = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == WIELDED_REACH:
        try:
            value = int(arg)
            if 1 <= value <= 10:
                data.reach = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == WIELDED_DURABILITY:
        try:
            value = int(arg)
            if 0 <= value <= data.max_durability:
                data.durability = value
                return True
        except ValueError:
            pass
        return False
    
    elif choice == WIELDED_MAX_DURABILITY:
        try:
            value = int(arg)
            if 1 <= value <= 1000:
                data.max_durability = value
                # Ensure current durability doesn't exceed max
                data.durability = min(data.durability, data.max_durability)
                return True
        except ValueError:
            pass
        return False
    
    elif choice == WIELDED_MATERIAL:
        material = arg.strip().lower()
        if gear_config.is_valid_wielded_material(material):
            data.material = material
            return True
        else:
            valid_materials = gear_config.get_wielded_materials()
            sock.send_raw("Invalid material. Valid materials are: %s\n" % ", ".join(valid_materials))
            return False
    
    elif choice == WIELDED_SPECIAL_PROPERTIES:
        # Validate special properties (comma-separated list)
        properties = [p.strip().lower() for p in arg.split(',') if p.strip()]
        valid_properties = gear_config.get_wielded_special_properties()
        invalid_properties = [p for p in properties if p not in valid_properties]
        
        if invalid_properties:
            sock.send_raw("Invalid properties: %s\nValid properties are: %s\n" % 
                         (", ".join(invalid_properties), ", ".join(valid_properties)))
            return False
        else:
            data.special_properties = ", ".join(properties)
            return True
    
    elif choice == WIELDED_SPECIAL_ATTACKS:
        # Validate special attacks (comma-separated list)
        attacks = [a.strip().lower() for a in arg.split(',') if a.strip()]
        valid_attacks = gear_config.get_wielded_special_attacks()
        invalid_attacks = [a for a in attacks if a not in valid_attacks]
        
        if invalid_attacks:
            sock.send_raw("Invalid attacks: %s\nValid attacks are: %s\n" % 
                         (", ".join(invalid_attacks), ", ".join(valid_attacks)))
            return False
        else:
            data.special_attacks = ", ".join(attacks)
            return True
    
    return False

def wielded_to_proto(data):
    """Generate prototype code for wielded items"""
    lines = []
    if data.damage_type != "slashing":
        lines.append("me.get_type_data(\"wielded\").damage_type = \"%s\"" % data.damage_type)
    if data.weapon_category != "melee":
        lines.append("me.get_type_data(\"wielded\").weapon_category = \"%s\"" % data.weapon_category)
    if data.ranged_type:
        lines.append("me.get_type_data(\"wielded\").ranged_type = \"%s\"" % data.ranged_type)
    if data.damage_dice != "1d6":
        lines.append("me.get_type_data(\"wielded\").damage_dice = \"%s\"" % data.damage_dice)
    if data.damage_bonus != 0:
        lines.append("me.get_type_data(\"wielded\").damage_bonus = %d" % data.damage_bonus)
    if data.hit_bonus != 0:
        lines.append("me.get_type_data(\"wielded\").hit_bonus = %d" % data.hit_bonus)
    if data.weapon_speed != 1.0:
        lines.append("me.get_type_data(\"wielded\").weapon_speed = %.1f" % data.weapon_speed)
    if data.reach != 1:
        lines.append("me.get_type_data(\"wielded\").reach = %d" % data.reach)
    if data.durability != 100:
        lines.append("me.get_type_data(\"wielded\").durability = %d" % data.durability)
    if data.max_durability != 100:
        lines.append("me.get_type_data(\"wielded\").max_durability = %d" % data.max_durability)
    if data.material != "steel":
        lines.append("me.get_type_data(\"wielded\").material = \"%s\"" % data.material)
    if data.special_properties:
        lines.append("me.get_type_data(\"wielded\").special_properties = \"%s\"" % data.special_properties)
    if data.special_attacks:
        lines.append("me.get_type_data(\"wielded\").special_attacks = \"%s\"" % data.special_attacks)
    return "\n".join(lines) + ("\n" if lines else "")

def init_gear_olc():
    """Initialize OLC editors for gear item types"""
    # Register OLC functions for equipped items
    olc.item_add_olc("equipped", equipped_menu, equipped_chooser, 
                     equipped_parser, None, equipped_to_proto)
    
    # Register OLC functions for wielded items  
    olc.item_add_olc("wielded", wielded_menu, wielded_chooser,
                     wielded_parser, None, wielded_to_proto)

# Initialize OLC when module loads
init_gear_olc()
