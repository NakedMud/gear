"""
Gear Module for NakedMud

Provides item types and functionality for weapons, armor, and other equipment.
Includes wielded items (weapons, tools) and equipped items (armor, accessories).
"""
import os
import importlib
import re

# Import all submodules to make them available
from . import gear_config

# Import all submodules to register item types and hooks
for fl in os.listdir(__path__[0]):
    if fl.endswith(".py") and not (fl == "__init__.py" or fl.startswith(".")):
        module_name = fl[:-3]
        importlib.import_module('.' + module_name, package=__name__)

# Define what gets imported with "from gear import *"
__all__ = [
    # Helper functions
    'get_wielded_data',
    'get_equipped_data', 
    'get_character_gear',
    'get_total_ac',
    'get_bodypart_ac',
    'get_weapon_damage_all',
    'get_weapon_damage',
    'get_weapon_properties',
    'get_weapon_stats',
    'get_armor_stats'
]

# ============================================================================
# GEAR MODULE HELPER FUNCTIONS
# ============================================================================

def get_wielded_data(obj):
    """Get wielded data from an object, returns None if not wielded type"""
    if obj.istype("wielded"):
        return obj.get_type_data("wielded")
    return None

def get_equipped_data(obj):
    """Get equipped data from an object, returns None if not equipped type"""
    if obj.istype("equipped"):
        return obj.get_type_data("equipped")
    return None

def get_character_gear(ch):
    """Get all gear on a character categorized by type
    
    Returns dict with keys: 'wielded', 'equipped', 'worn'
    Each contains list of objects of that type
    """
    gear = {'wielded': [], 'equipped': [], 'worn': []}
    
    for obj in ch.eq:
        if obj.istype("wielded"):
            gear['wielded'].append(obj)
        elif obj.istype("equipped"):
            gear['equipped'].append(obj)
        else:
            gear['worn'].append(obj)
    
    return gear

def get_total_ac(ch):
    """Calculate total armor class from all equipped items"""
    total_ac = 0
    
    for obj in ch.eq:
        if obj.istype("equipped"):
            data = get_equipped_data(obj)
            if data:
                total_ac += data.armor_class
    
    return total_ac

def get_bodypart_ac(ch, bodypart):
    """Calculate armor class for a specific body part"""
    ac = 0
    
    for obj in ch.eq:
        if obj.istype("equipped"):
            # Check if this item is equipped on the specified bodypart
            equipped_where = ch.get_slots(obj)
            if bodypart.lower() in equipped_where.lower():
                data = get_equipped_data(obj)
                if data:
                    ac += data.armor_class
    
    return ac

def _parse_dice_string(dice_str):
    """Parse dice string like '1d6' or '3d8' into (count, sides)"""
    if not dice_str or 'd' not in dice_str:
        return (1, 4)  # Default to 1d4
    
    try:
        parts = dice_str.lower().split('d')
        count = int(parts[0]) if parts[0] else 1
        sides = int(parts[1]) if len(parts) > 1 else 4
        return (count, sides)
    except (ValueError, IndexError):
        return (1, 4)  # Default to 1d4 on parse error

def _dice_to_string(count, sides):
    """Convert dice count and sides back to string format"""
    return f"{count}d{sides}"

def _upgrade_dice(dice_str, bonus_dice=0):
    """Upgrade dice by adding to the die size (for dual-wield bonus)"""
    count, sides = _parse_dice_string(dice_str)
    new_sides = min(sides + (bonus_dice * 2), 20)  # Cap at d20
    return _dice_to_string(count, new_sides)

def get_weapon_damage_all(ch):
    """Get all weapon damage with locations
    
    Returns list of tuples: (location, full_damage_string)
    Example: [('right hand', '1d8+2'), ('left hand', '1d6+1')]
    If primary hand is empty, includes ('right hand', '1d4+0') for unarmed
    """
    damages = []
    has_primary = False
    has_offhand = False
    is_dual_wielding = False
    
    # Check what's wielded and where
    wielded_items = []
    for obj in ch.eq:
        if obj.istype("wielded"):
            location = ch.get_slots(obj)
            wielded_items.append((obj, location))
            
            if 'right hand' in location.lower():
                has_primary = True
            if 'left hand' in location.lower():
                has_offhand = True
            if 'right hand' in location.lower() and 'left hand' in location.lower():
                is_dual_wielding = True
    
    # Process wielded weapons
    for obj, location in wielded_items:
        data = get_wielded_data(obj)
        if data:
            dice = data.damage_dice
            bonus = data.damage_bonus
            
            # Apply dual-wield bonus if using both hands for same weapon
            if is_dual_wielding and 'right hand' in location.lower() and 'left hand' in location.lower():
                dice = _upgrade_dice(dice, 1)  # +2 to die size for dual-wield
                full_damage = f"{dice}+{bonus}" if bonus > 0 else dice
                damages.append(('both hands', full_damage))
            else:
                full_damage = f"{dice}+{bonus}" if bonus > 0 else dice
                damages.append((location, full_damage))
    
    # Add unarmed damage for empty primary hand
    if not has_primary and not is_dual_wielding:
        damages.append(('right hand', '1d4+0'))
    
    return damages

def get_weapon_damage(ch, hand='primary'):
    """Get weapon damage for specific hand
    
    Args:
        ch: Character object
        hand: 'primary' (right hand) or 'offhand' (left hand)
    
    Returns: damage string like '1d8+2' or '1d4+0' for unarmed
    """
    target_hand = 'right hand' if hand == 'primary' else 'left hand'
    
    for obj in ch.eq:
        if obj.istype("wielded"):
            location = ch.get_slots(obj)
            
            # Check for dual-wield (both hands)
            if 'right hand' in location.lower() and 'left hand' in location.lower():
                data = get_wielded_data(obj)
                if data:
                    dice = _upgrade_dice(data.damage_dice, 1)  # +2 die size for dual-wield
                    bonus = data.damage_bonus
                    return f"{dice}+{bonus}" if bonus > 0 else dice
            
            # Check for specific hand
            elif target_hand in location.lower():
                data = get_wielded_data(obj)
                if data:
                    dice = data.damage_dice
                    bonus = data.damage_bonus
                    return f"{dice}+{bonus}" if bonus > 0 else dice
    
    # Return unarmed damage if no weapon found
    return '1d4+0'

def get_weapon_properties(ch, hand='primary'):
    """Get weapon special properties for specific hand
    
    Args:
        ch: Character object  
        hand: 'primary' (right hand) or 'offhand' (left hand)
    
    Returns: string of comma-separated properties or empty string
    """
    target_hand = 'right hand' if hand == 'primary' else 'left hand'
    
    for obj in ch.eq:
        if obj.istype("wielded"):
            location = ch.get_slots(obj)
            
            # Check for dual-wield or specific hand
            if (target_hand in location.lower() or 
                ('right hand' in location.lower() and 'left hand' in location.lower())):
                data = get_wielded_data(obj)
                if data:
                    return data.special_properties
    
    return ""

def get_weapon_stats(ch, hand='primary'):
    """Get complete weapon statistics for specific hand
    
    Args:
        ch: Character object
        hand: 'primary' (right hand) or 'offhand' (left hand)
    
    Returns: dict with keys: damage, hit_bonus, speed, reach, properties, damage_type, weapon_category
    """
    target_hand = 'right hand' if hand == 'primary' else 'left hand'
    
    # Default unarmed stats
    stats = {
        'damage': '1d4+0',
        'hit_bonus': 0,
        'speed': 1.0,
        'reach': 1,
        'properties': '',
        'damage_type': 'bludgeoning',
        'weapon_category': 'unarmed'
    }
    
    for obj in ch.eq:
        if obj.istype("wielded"):
            location = ch.get_slots(obj)
            
            # Check for dual-wield (both hands)
            if 'right hand' in location.lower() and 'left hand' in location.lower():
                data = get_wielded_data(obj)
                if data:
                    dice = _upgrade_dice(data.damage_dice, 1)  # +2 die size for dual-wield
                    bonus = data.damage_bonus
                    stats.update({
                        'damage': f"{dice}+{bonus}" if bonus > 0 else dice,
                        'hit_bonus': data.hit_bonus,
                        'speed': data.weapon_speed,
                        'reach': data.reach,
                        'properties': data.special_properties,
                        'damage_type': data.damage_type,
                        'weapon_category': data.weapon_category
                    })
                    break
            
            # Check for specific hand
            elif target_hand in location.lower():
                data = get_wielded_data(obj)
                if data:
                    dice = data.damage_dice
                    bonus = data.damage_bonus
                    stats.update({
                        'damage': f"{dice}+{bonus}" if bonus > 0 else dice,
                        'hit_bonus': data.hit_bonus,
                        'speed': data.weapon_speed,
                        'reach': data.reach,
                        'properties': data.special_properties,
                        'damage_type': data.damage_type,
                        'weapon_category': data.weapon_category
                    })
                    break
    
    return stats

def get_armor_stats(ch, all_only=False):
    """Get armor statistics for all equipped items
    
    Args:
        ch: Character object
        all_only: If True, returns only aggregate stats. If False, returns detailed breakdown.
    
    Returns: 
        If all_only=False: dict with keys:
            'items': list of dicts for each armor piece with keys: 
                     name, bodypart, ac, enchantment, durability, material, properties
            'totals': dict with aggregate ac, enchantment_level, item_count
        If all_only=True: dict with just the totals
    """
    armor_items = []
    total_ac = 0
    total_enchantment = 0
    item_count = 0
    
    for obj in ch.eq:
        if obj.istype("equipped"):
            data = get_equipped_data(obj)
            if data:
                bodypart = ch.get_slots(obj)
                
                item_info = {
                    'name': obj.name,
                    'bodypart': bodypart,
                    'ac': data.armor_class,
                    'enchantment': data.enchantment_level,
                    'durability': data.durability,
                    'max_durability': data.max_durability,
                    'material': data.material,
                    'properties': data.special_properties
                }
                
                armor_items.append(item_info)
                total_ac += data.armor_class
                total_enchantment += data.enchantment_level
                item_count += 1
    
    totals = {
        'total_ac': total_ac,
        'total_enchantment': total_enchantment,
        'item_count': item_count,
        'average_enchantment': total_enchantment / item_count if item_count > 0 else 0
    }
    
    if all_only:
        return totals
    else:
        return {
            'items': armor_items,
            'totals': totals
        }
