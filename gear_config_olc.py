"""
Gear Configuration OLC Editor

Provides an online editor for managing gear configuration data.
Only manipulates in-memory gear_config data, never touches storage directly.
"""

import olc
from . import gear_config
from mudsys import add_cmd

# Helper function for tabular display
def format_tabular_list(items, markers=None, line_width=78):
    """Format a list of items in tabular form with optional markers"""
    if not items:
        return "  (none)\n"
    
    # Calculate the width needed for each item (including marker and spacing)
    max_item_width = max(len(item) for item in items)
    marker_width = 2 if markers else 0  # "* " or "  "
    spacing = 2  # Space between columns
    column_width = max_item_width + marker_width + spacing
    
    # Calculate how many columns fit in the line width
    cols_per_line = max(1, (line_width - 2) // column_width)
    
    result = ""
    for i in range(0, len(items), cols_per_line):
        line_items = items[i:i + cols_per_line]
        line = "  "
        
        for item in line_items:
            marker = markers.get(item, " ") if markers else " "
            formatted = f"{marker} {item}".ljust(column_width)
            line += formatted
        
        result += line.rstrip() + "\n"
    
    return result

# OLC return values
MENU_CHOICE_INVALID = -1
MENU_NOCHOICE = 0

def gear_config_menu(sock, data):
    """Main gear configuration menu"""
    sock.send_raw("""
{g+{n==============================================================================
{cGear Configuration Editor{n
{g+{n==============================================================================

{c1{n) Edit wielded item configuration
{c2{n) Edit equipped item configuration
{c3{n) Edit worn types

{cQ{n) Quit
""")

def gear_config_chooser(sock, data, choice):
    """Handle main gear config menu choices"""
    if choice == '1':
        olc.do_olc(sock, wielded_config_menu, wielded_config_chooser, 
                   wielded_config_parser, None, data)
        return MENU_NOCHOICE
    elif choice == '2':
        olc.do_olc(sock, equipped_config_menu, equipped_config_chooser,
                   equipped_config_parser, None, data)
        return MENU_NOCHOICE
    elif choice == '3':
        olc.do_olc(sock, worn_types_menu, worn_types_chooser,
                   worn_types_parser, None, data)
        return MENU_NOCHOICE
    return MENU_CHOICE_INVALID

def gear_config_parser(sock, data, choice, arg):
    """Parse gear config menu input"""
    return False

def wielded_config_menu(sock, data):
    """Wielded item configuration menu"""
    weapon_types = gear_config.get_damage_types()
    materials = gear_config.get_wielded_materials()
    properties = gear_config.get_wielded_special_properties()
    attacks = gear_config.get_wielded_special_attacks()
    
    sock.send_raw("""
{g+{n==============================================================================
{cWielded Item Configuration{n
{g+{n==============================================================================

{c1{n) Damage types ({y%d{n): %s
{c2{n) Materials ({y%d{n): %s
{c3{n) Special properties ({y%d{n): %s
{c4{n) Special attacks ({y%d{n): %s

{cQ{n) Return to main menu
""" % (
        len(weapon_types), ", ".join(weapon_types[:5]) + ("..." if len(weapon_types) > 5 else ""),
        len(materials), ", ".join(materials[:5]) + ("..." if len(materials) > 5 else ""),
        len(properties), ", ".join(properties[:5]) + ("..." if len(properties) > 5 else ""),
        len(attacks), ", ".join(attacks[:5]) + ("..." if len(attacks) > 5 else "")
    ))

def wielded_config_chooser(sock, data, choice):
    """Handle wielded config menu choices"""
    if choice == '1':
        olc.do_olc(sock, damage_types_menu, damage_types_chooser, 
                   damage_types_parser, None, data)
        return MENU_NOCHOICE
    elif choice == '2':
        olc.do_olc(sock, wielded_materials_menu, wielded_materials_chooser,
                   wielded_materials_parser, None, data)
        return MENU_NOCHOICE
    elif choice == '3':
        olc.do_olc(sock, wielded_properties_menu, wielded_properties_chooser,
                   wielded_properties_parser, None, data)
        return MENU_NOCHOICE
    elif choice == '4':
        olc.do_olc(sock, wielded_attacks_menu, wielded_attacks_chooser,
                   wielded_attacks_parser, None, data)
        return MENU_NOCHOICE
    return MENU_CHOICE_INVALID

def wielded_config_parser(sock, data, choice, arg):
    """Parse wielded config menu input"""
    return False

def equipped_config_menu(sock, data):
    """Equipped item configuration menu"""
    armor_types = gear_config.get_equipped_types()
    materials = gear_config.get_equipped_materials()
    properties = gear_config.get_equipped_special_properties()
    
    sock.send_raw("""
{g+{n==============================================================================
{cEquipped Item Configuration{n
{g+{n==============================================================================

{c1{n) Armor types ({y%d{n): %s
{c2{n) Materials ({y%d{n): %s
{c3{n) Special properties ({y%d{n): %s

{cQ{n) Return to main menu
""" % (
        len(armor_types), ", ".join(armor_types[:5]) + ("..." if len(armor_types) > 5 else ""),
        len(materials), ", ".join(materials[:5]) + ("..." if len(materials) > 5 else ""),
        len(properties), ", ".join(properties[:5]) + ("..." if len(properties) > 5 else "")
    ))

def equipped_config_chooser(sock, data, choice):
    """Handle equipped config menu choices"""
    if choice == '1':
        olc.do_olc(sock, armor_types_menu, armor_types_chooser,
                   armor_types_parser, None, data)
        return MENU_NOCHOICE
    elif choice == '2':
        olc.do_olc(sock, equipped_materials_menu, equipped_materials_chooser,
                   equipped_materials_parser, None, data)
        return MENU_NOCHOICE
    elif choice == '3':
        olc.do_olc(sock, equipped_properties_menu, equipped_properties_chooser,
                   equipped_properties_parser, None, data)
        return MENU_NOCHOICE
    return MENU_CHOICE_INVALID

def equipped_config_parser(sock, data, choice, arg):
    """Parse equipped config menu input"""
    return False

# Damage Types Menu
def damage_types_menu(sock, data):
    """Damage types configuration menu"""
    damage_types = gear_config.get_damage_types()
    
    sock.send_raw("""
{g+{n==============================================================================
{cDamage Types Configuration{n
{g+{n==============================================================================

Current damage types ({y%d{n):
%s
{c1{n) Add damage type
{c2{n) Remove damage type

{cQ{n) Return to wielded menu
""" % (
        len(damage_types),
        format_tabular_list(damage_types)
    ))

def damage_types_chooser(sock, data, choice):
    """Handle damage types menu choices"""
    if choice == '1':
        sock.send_raw("Enter new damage type: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter damage type to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def damage_types_parser(sock, data, choice, arg):
    """Parse damage types input"""
    if choice == 1 and arg:
        gear_config.add_damage_type(arg.strip())
        sock.send_raw("Added damage type: %s\n" % arg.strip())
        return True
    elif choice == 2 and arg:
        if gear_config.remove_damage_type(arg.strip()):
            sock.send_raw("Removed damage type: %s\n" % arg.strip())
        else:
            sock.send_raw("Damage type '%s' not found.\n" % arg.strip())
        return True
    return False

# Wielded Materials Menu
def wielded_materials_menu(sock, data):
    """Wielded materials configuration menu"""
    materials = gear_config.get_wielded_materials()
    
    sock.send_raw("""
{g+{n==============================================================================
{cWielded Materials Configuration{n
{g+{n==============================================================================

Current materials ({y%d{n):
%s
{c1{n) Add material
{c2{n) Remove material

{cQ{n) Return to wielded menu
""" % (
        len(materials),
        format_tabular_list(materials)
    ))

def wielded_materials_chooser(sock, data, choice):
    """Handle wielded materials menu choices"""
    if choice == '1':
        sock.send_raw("Enter new material: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter material to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def wielded_materials_parser(sock, data, choice, arg):
    """Parse wielded materials input"""
    if choice == 1 and arg:
        gear_config.add_wielded_material(arg.strip())
        sock.send_raw("Added material: %s\n" % arg.strip())
        return True
    elif choice == 2 and arg:
        if gear_config.remove_wielded_material(arg.strip()):
            sock.send_raw("Removed material: %s\n" % arg.strip())
        else:
            sock.send_raw("Material '%s' not found.\n" % arg.strip())
        return True
    return False

# Wielded Properties Menu
def wielded_properties_menu(sock, data):
    """Wielded properties configuration menu"""
    properties = gear_config.get_wielded_special_properties()
    
    sock.send_raw("""
{g+{n==============================================================================
{cWielded Special Properties Configuration{n
{g+{n==============================================================================

Current properties ({y%d{n):
%s
{c1{n) Add property
{c2{n) Remove property

{cQ{n) Return to wielded menu
""" % (
        len(properties),
        format_tabular_list(properties)
    ))

def wielded_properties_chooser(sock, data, choice):
    """Handle wielded properties menu choices"""
    if choice == '1':
        sock.send_raw("Enter new property: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter property to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def wielded_properties_parser(sock, data, choice, arg):
    """Parse wielded properties input"""
    if choice == 1 and arg:
        gear_config.add_wielded_special_property(arg.strip())
        sock.send_raw("Added property: %s\n" % arg.strip())
        return True
    elif choice == 2 and arg:
        if gear_config.remove_wielded_special_property(arg.strip()):
            sock.send_raw("Removed property: %s\n" % arg.strip())
        else:
            sock.send_raw("Property '%s' not found.\n" % arg.strip())
        return True
    return False

# Wielded Attacks Menu
def wielded_attacks_menu(sock, data):
    """Wielded attacks configuration menu"""
    attacks = gear_config.get_wielded_special_attacks()
    
    sock.send_raw("""
{g+{n==============================================================================
{cWielded Special Attacks Configuration{n
{g+{n==============================================================================

Current attacks ({y%d{n):
%s
{c1{n) Add attack
{c2{n) Remove attack

{cQ{n) Return to wielded menu
""" % (
        len(attacks),
        format_tabular_list(attacks)
    ))

def wielded_attacks_chooser(sock, data, choice):
    """Handle wielded attacks menu choices"""
    if choice == '1':
        sock.send_raw("Enter new attack: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter attack to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def wielded_attacks_parser(sock, data, choice, arg):
    """Parse wielded attacks input"""
    if choice == 1 and arg:
        gear_config.add_wielded_special_attack(arg.strip())
        sock.send_raw("Added attack: %s\n" % arg.strip())
        return True
    elif choice == 2 and arg:
        if gear_config.remove_wielded_special_attack(arg.strip()):
            sock.send_raw("Removed attack: %s\n" % arg.strip())
        else:
            sock.send_raw("Attack '%s' not found.\n" % arg.strip())
        return True
    return False

# Armor Types Menu
def armor_types_menu(sock, data):
    """Armor types configuration menu"""
    armor_types = gear_config.get_equipped_types()
    
    sock.send_raw("""
{g+{n==============================================================================
{cArmor Types Configuration{n
{g+{n==============================================================================

Current armor types ({y%d{n):
%s
{c1{n) Add armor type
{c2{n) Remove armor type

{cQ{n) Return to equipped menu
""" % (
        len(armor_types),
        format_tabular_list(armor_types)
    ))

def armor_types_chooser(sock, data, choice):
    """Handle armor types menu choices"""
    if choice == '1':
        sock.send_raw("Enter new armor type: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter armor type to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def armor_types_parser(sock, data, choice, arg):
    """Parse armor types input"""
    if choice == 1 and arg:
        gear_config.add_equipped_type(arg.strip())
        sock.send_raw("Added armor type: %s\n" % arg.strip())
        return True
    elif choice == 2 and arg:
        if gear_config.remove_equipped_type(arg.strip()):
            sock.send_raw("Removed armor type: %s\n" % arg.strip())
        else:
            sock.send_raw("Armor type '%s' not found.\n" % arg.strip())
        return True
    return False

# Equipped Materials Menu
def equipped_materials_menu(sock, data):
    """Equipped materials configuration menu"""
    materials = gear_config.get_equipped_materials()
    
    sock.send_raw("""
{g+{n==============================================================================
{cEquipped Materials Configuration{n
{g+{n==============================================================================

Current materials ({y%d{n):
%s
{c1{n) Add material
{c2{n) Remove material

{cQ{n) Return to equipped menu
""" % (
        len(materials),
        format_tabular_list(materials)
    ))

def equipped_materials_chooser(sock, data, choice):
    """Handle equipped materials menu choices"""
    if choice == '1':
        sock.send_raw("Enter new material: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter material to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def equipped_materials_parser(sock, data, choice, arg):
    """Parse equipped materials input"""
    if choice == 1 and arg:
        gear_config.add_equipped_material(arg.strip())
        sock.send_raw("Added material: %s\n" % arg.strip())
        return True
    elif choice == 2 and arg:
        if gear_config.remove_equipped_material(arg.strip()):
            sock.send_raw("Removed material: %s\n" % arg.strip())
        else:
            sock.send_raw("Material '%s' not found.\n" % arg.strip())
        return True
    return False

# Equipped Properties Menu
def equipped_properties_menu(sock, data):
    """Equipped properties configuration menu"""
    properties = gear_config.get_equipped_special_properties()
    
    sock.send_raw("""
{g+{n==============================================================================
{cEquipped Special Properties Configuration{n
{g+{n==============================================================================

Current properties ({y%d{n):
%s
{c1{n) Add property
{c2{n) Remove property

{cQ{n) Return to equipped menu
""" % (
        len(properties),
        format_tabular_list(properties)
    ))

def equipped_properties_chooser(sock, data, choice):
    """Handle equipped properties menu choices"""
    if choice == '1':
        sock.send_raw("Enter new property: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter property to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def equipped_properties_parser(sock, data, choice, arg):
    """Parse equipped properties input"""
    if choice == 1 and arg:
        gear_config.add_equipped_special_property(arg.strip())
        sock.send_raw("Added property: %s\n" % arg.strip())
        return True
    elif choice == 2 and arg:
        if gear_config.remove_equipped_special_property(arg.strip()):
            sock.send_raw("Removed property: %s\n" % arg.strip())
        else:
            sock.send_raw("Property '%s' not found.\n" % arg.strip())
        return True
    return False

# Worn Types Menu
def worn_types_menu(sock, data):
    """Worn types configuration menu"""
    from . import gear_config
    
    worn_types = gear_config.get_worn_types()
    
    # Format worn types with built-in markers
    formatted_types = []
    for worn_type in worn_types:
        if gear_config.is_builtin_worn_type(worn_type):
            formatted_types.append(f"{worn_type}*")
        else:
            formatted_types.append(worn_type)
    
    sock.send_raw("""
{g+{n==============================================================================
{cWorn Types Configuration{n
{g+{n==============================================================================

Current worn types ({y%d{n}) - {y*{n = built-in:
%s
{c1{n) Add worn type
{c2{n) Remove worn type
{c3{n) View worn type positions
{c4{n) Edit worn type positions

{cQ{n) Return to main menu
""" % (
        len(worn_types),
        format_tabular_list(formatted_types)
    ))

def worn_types_chooser(sock, data, choice):
    """Handle worn types menu choices"""
    if choice == '1':
        sock.send_raw("Enter new worn type name: ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter worn type to remove: ")
        return 2
    elif choice == '3':
        sock.send_raw("Enter worn type to view positions: ")
        return 3
    elif choice == '4':
        sock.send_raw("Enter worn type to edit positions: ")
        return 4
    return MENU_CHOICE_INVALID

def worn_types_parser(sock, data, choice, arg):
    """Parse worn types input"""
    from . import gear_config
    
    if choice == 1 and arg:
        # Add new worn type - create and start editing it
        worn_type = arg.strip().lower()
        if gear_config.worn_type_exists(worn_type):
            sock.send_raw("Worn type '%s' already exists.\n" % worn_type)
            return True
        
        # Create new worn type with empty positions
        if gear_config.add_worn_type(worn_type, []):
            sock.send_raw("Created new worn type: %s\n" % worn_type)
            # Get the worn type object and start editing
            worn_type_obj = gear_config.get_worn_type_object(worn_type)
            if worn_type_obj:
                olc.do_olc(sock, worn_type_edit_menu, worn_type_edit_chooser, worn_type_edit_parser, None, worn_type_obj)
            return True
        else:
            sock.send_raw("Failed to add worn type '%s'\n" % worn_type)
            return True
    elif choice == 2 and arg:
        # Remove worn type
        worn_type = arg.strip().lower()
        if not gear_config.worn_type_exists(worn_type):
            sock.send_raw("Worn type '%s' not found.\n" % worn_type)
        elif gear_config.is_builtin_worn_type(worn_type):
            sock.send_raw("Cannot remove built-in worn type '%s'.\n" % worn_type)
        else:
            if gear_config.remove_worn_type(worn_type):
                sock.send_raw("Removed worn type: %s\n" % worn_type)
            else:
                sock.send_raw("Failed to remove worn type: %s\n" % worn_type)
        return True
    elif choice == 3 and arg:
        # View worn type positions
        worn_type = arg.strip().lower()
        if not gear_config.worn_type_exists(worn_type):
            sock.send_raw("Worn type '%s' not found.\n" % worn_type)
        else:
            positions = gear_config.get_worn_type_positions(worn_type)
            if positions:
                builtin_marker = " (built-in)" if gear_config.is_builtin_worn_type(worn_type) else ""
                sock.send_raw("Positions for '%s'%s: %s\n" % (worn_type, builtin_marker, ", ".join(positions)))
            else:
                sock.send_raw("Worn type '%s' has no positions defined.\n" % worn_type)
        return True
    elif choice == 4 and arg:
        # Edit worn type positions - start subediting
        worn_type = arg.strip().lower()
        if not gear_config.worn_type_exists(worn_type):
            sock.send_raw("Worn type '%s' not found.\n" % worn_type)
            return True
        
        # Get the worn type object and start editing
        worn_type_obj = gear_config.get_worn_type_object(worn_type)
        if worn_type_obj:
            olc.do_olc(sock, worn_type_edit_menu, worn_type_edit_chooser, worn_type_edit_parser, None, worn_type_obj)
        else:
            sock.send_raw("Failed to get worn type object for '%s'\n" % worn_type)
        return True
    return False

# Worn type editing submenu
def worn_type_edit_menu(sock, worn_type_obj):
    """Display worn type editing menu"""
    from . import gear_config
    
    worn_type = worn_type_obj.get('name', 'unknown')
    positions = gear_config.get_worn_type_positions(worn_type)
    
    sock.send_raw("""
{c== Worn Type Editor: %s =={n

Current positions: {y%s{w

{c1{n) Add position
{c2{n) Remove position
{cQ{n) Quit

Enter choice: """ % (worn_type, ", ".join(positions) if positions else "none"))

def worn_type_edit_chooser(sock, worn_type_obj, choice):
    """Handle worn type editing menu choices"""
    from . import gear_config
    
    if choice.lower() == 'q':
        return MENU_QUIT
    elif choice == '1':
        # Show available positions when adding, like race positions does
        available_positions = gear_config.get_available_body_positions()
        sock.send_raw("\n{gAvailable body positions ({y" + str(len(available_positions)) + "{g):{n\n")
        
        # Format in columns with spacing
        for i, pos in enumerate(available_positions):
            if i % 4 == 0:
                sock.send_raw("\n  {w")
            sock.send_raw("%-18s" % pos)
        sock.send_raw("{n\n\n{gEnter position to add:{n ")
        return 1
    elif choice == '2':
        sock.send_raw("Enter position to remove: ")
        return 2
    return MENU_CHOICE_INVALID

def worn_type_edit_parser(sock, worn_type_obj, choice, arg):
    """Parse worn type editing input"""
    from . import gear_config
    
    worn_type = worn_type_obj.get('name', 'unknown')
    
    if choice == 1 and arg:
        # Add position
        position = arg.strip().lower()
        available_positions = gear_config.get_available_body_positions()
        
        if position not in available_positions:
            sock.send_raw("Position '%s' is not a valid body position.\n" % position)
            return True
            
        current_positions = gear_config.get_worn_type_positions(worn_type)
        if position in current_positions:
            sock.send_raw("Position '%s' is already in worn type '%s'.\n" % (position, worn_type))
            return True
            
        # Add the position
        new_positions = current_positions + [position]
        if gear_config.set_worn_type_positions(worn_type, new_positions):
            sock.send_raw("Added position '%s' to worn type '%s'.\n" % (position, worn_type))
        else:
            sock.send_raw("Failed to add position '%s'.\n" % position)
        return True
        
    elif choice == 2 and arg:
        # Remove position
        position = arg.strip().lower()
        current_positions = gear_config.get_worn_type_positions(worn_type)
        
        if position not in current_positions:
            sock.send_raw("Position '%s' is not in worn type '%s'.\n" % (position, worn_type))
            return True
            
        # Remove the position
        new_positions = [p for p in current_positions if p != position]
        if gear_config.set_worn_type_positions(worn_type, new_positions):
            sock.send_raw("Removed position '%s' from worn type '%s'.\n" % (position, worn_type))
        else:
            sock.send_raw("Failed to remove position '%s'.\n" % position)
        return True
        
        
    return False

# Register the OLC command
def cmd_gearconfig(ch, cmd, arg):
    """
    Syntax: gearconfig
    
    Opens the gear configuration editor for managing weapon types, materials,
    and special properties for wielded and equipped items.
    """
    olc.do_olc(ch.sock, gear_config_menu, gear_config_chooser, gear_config_parser, gear_config.save_gear_configs, None)

# Register command
add_cmd("gearconfig", None, cmd_gearconfig, "admin", False)
