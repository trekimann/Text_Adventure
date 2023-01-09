import src
class Boss(src.Enemy):
    def __init__(self, name, description, health, damage_resistance_multiplier, attack_multiplier, enemy_type, loot_chance, loot, armour=0, weapon: src.Weapon = None, loot_amount=0, boss=False):
        super().__init__(name, description, health, damage_resistance_multiplier, attack_multiplier, enemy_type, loot_chance, loot, armour, weapon, loot_amount, boss)
