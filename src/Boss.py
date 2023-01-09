import random
import src

tc = src.TC()
class Boss(src.Enemy):
    def __init__(self, name, description, health, damage_resistance_multiplier, attack_multiplier, enemy_type, loot_chance, loot, armour=0, weapon: src.Weapon = None, loot_amount=0, weak_against=None, weakness_multiplier=1):
        super().__init__(name, description, health, damage_resistance_multiplier, attack_multiplier, enemy_type, loot_chance, loot, armour, weapon, loot_amount)
        self.weak_against = weak_against
        self.weakness_multiplier = weakness_multiplier

    def take_damage(self, damage, attacking_weapon: src.Weapon = None):
        if attacking_weapon.name == self.weak_against:
            damage *= self.weakness_multiplier
            print(f"{self.name} is weak against {attacking_weapon.name}! {tc.colour('red')}{damage}{tc.colour()} damage dealt!")
        if self.armour > 0:
            # Calculate the amount of damage that the armour absorbs
            absorbed_damage = round(random.uniform(0.1, 1),2)
            print(f"{self.name}'s armour absorbs {tc.colour('blue')}{absorbed_damage}{tc.colour()} points of damage")
            # Reduce the armour's hit points by the absorbed damage
            if absorbed_damage > damage:
                self.armour -= damage
            else:
                self.armour -= absorbed_damage
                # Reduce the remaining damage from the player's health
                self.health -= round((damage - absorbed_damage) * self.damage_resistance_multiplier,2)
            print(f"{self.name} has {tc.colour('blue')}{self.armour}{tc.colour()} armour hit points remaining")
        else:
            self.health -= round(damage * self.damage_resistance_multiplier,2)
                
        print(f"{self.name} has {tc.colour('green')}{self.health}{tc.colour()} health hit points remaining")
        return self.is_dead()