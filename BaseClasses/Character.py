import random
from TextColour import TC
from Weapon import Weapon

tc = TC()

class Character:
    def __init__(self, name, description, health, armour, weapon: Weapon = None, damage_resistance_multiplier = 1, attack_multiplier = 1):
        self.name = name
        self.description = description
        self.health = health
        self.armour = armour
        self.weapon = weapon
        self.damage_resistance_multiplier = damage_resistance_multiplier
        self.attack_multiplier = attack_multiplier
    
    def attack(self):
        # Calculate the damage dealt to the character
        damage = round(random.uniform(self.weapon.damage_range[0], self.weapon.damage_range[1]) * self.attack_multiplier * self.weapon.damage_modifier,2)
        print(f"{self.name} attacks for {tc.colour('red')}{damage}{tc.colour()} points of damage.")
        return damage

    def take_damage(self, damage):
        if self.armour > 0:
            # Calculate the amount of damage that the armour absorbs
            absorbed_damage = round(random.uniform(0.1, 1),2)
            print(f"{self.name}'s armour absorbs {tc.colour('blue')}{absorbed_damage}{tc.colour()} points of damage")
            # Reduce the armour's hit points by the absorbed damage
            self.armour -= absorbed_damage
            print(f"{self.name} has {tc.colour('blue')}{self.armour}{tc.colour()} armour hit points remaining")
            # Reduce the remaining damage from the player's health
            self.health -= round((damage - absorbed_damage) * self.damage_resistance_multiplier,2)
        else:
            self.health -= round(damage * self.damage_resistance_multiplier,2)
                
        print(f"{self.name} has {tc.colour('green')}{self.health}{tc.colour()} health hit points remaining")
        return self.is_dead()
          
    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def is_dead(self):
        if self.health <= 0:
            print(f"{tc.colour('red')}{self.name} Died{tc.colour()}")
        return self.health <= 0