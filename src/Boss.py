import random
import src

tc = src.TC()
class Boss(src.Enemy):
    def __init__(self, name, description, health, damage_resistance_multiplier, attack_multiplier, enemy_type, loot_chance, loot, armour=0, weapon: src.Weapon = None, loot_amount=0, weak_against="None", weakness_multiplier=1):
        super().__init__(name=name, 
        description=description, 
        health=health,
        damage_resistance_multiplier=damage_resistance_multiplier,
        attack_multiplier=attack_multiplier,
        enemy_type=enemy_type,
        loot_chance=loot_chance,
        loot=loot,
        armour=armour,
        weapon=weapon,
        loot_amount=loot_amount,
        weak_against=weak_against,
        weakness_multiplier=weakness_multiplier)
