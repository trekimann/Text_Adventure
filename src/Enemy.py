import random
import src


class Enemy(src.Character):
    def __init__(self, name, description, health, damage_resistance_multiplier, attack_multiplier, enemy_type, loot_chance, loot, armour = 0, weapon: src.Weapon = None, loot_amount = 0, weak_against="None", weakness_multiplier=1):
        if weapon is None:
            weapon = src.Weapon(
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

        super().__init__(name ,description, health, armour, weapon, damage_resistance_multiplier, attack_multiplier, weak_against, weakness_multiplier)
        self.initial_health = health     
        self.enemy_type = enemy_type
        self.loot_chance = loot_chance
        self.loot = loot
        self.loot_amount = loot_amount

    def drop_loot(self):
        # Generate a random number between 0 and 1
        drop_chance = random.uniform(0, 1)
        if drop_chance <= self.loot_chance:
            print(f"{self.name} dropped loot!")
            return self.loot, self.loot_amount
        else:
            return None, 0

    def reset(self):
        self.health = self.initial_health