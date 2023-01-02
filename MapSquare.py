import random
from Item import Item

from Player import Player


class MapSquare:
    def __init__(self, description, enemy_chance, loot_chance, enemy_type, enemy_options, loot: Item, loot_amount = 1, key = None):
        self.description = description
        self.enemy_chance = enemy_chance
        self.loot_chance = loot_chance
        self.enemy_type = enemy_type
        self.loot = loot
        self.loot_amount = loot_amount
        self.enemy_options = enemy_options
        self.dead_enemies = 0
        self.key = key

    def has_enemy(self):
        enemy_encounter = random.random() < self.enemy_chance
        return enemy_encounter

    def has_loot(self):
        lootable = random.random() < self.loot_chance   
        return lootable
    
    def enemy_killed(self):
        self.dead_enemies += 1

    def loot_location(self, player: Player):
        # Display the loot at the location
        # Present the player a chance to see their inventory
        # Present the player a chance to drop items from their inventory
        # Give the player the option to loot if they want.
            # Remove the loot from the location if its special loot
        
        pass