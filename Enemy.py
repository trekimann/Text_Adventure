import random
from BaseClasses.Character import Character
from Weapon import Weapon

class Enemy(Character):
    def __init__(self, name, description, health, damage_resistance_multiplier, attack_multiplier, enemy_type, loot_chance, loot, armour = 0, weapon: Weapon = None):
        if weapon is None:
            weapon = Weapon(
            name = "Rusty Sword", 
            weight = 1,
            health_recovery = 0,
            value = 10,
            description = "A Rusty Sword, should be ok against many things",
            equipped = True,
            equippable = True,
            item_colour = "brown",
            type="weapon",
            damage_range=(0.1,1),
            damage_modifier=1)

        super().__init__(name , description, health, armour, weapon, damage_resistance_multiplier, attack_multiplier)
        self.initial_health = health     
        self.enemy_type = enemy_type
        self.loot_chance = loot_chance
        self.loot = loot

    def drop_loot(self):
        # Generate a random number between 0 and 1
        drop_chance = random.uniform(0, 1)
        if drop_chance <= self.loot_chance:
            print(f"{self.name} dropped loot!")
            return self.loot
        else:
            return None

    def reset(self):
        self.health = self.initial_health