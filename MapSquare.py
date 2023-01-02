import random


class MapSquare:
    def __init__(self, description, enemy_chance, loot_chance, enemy_type, loot_type, enemy_options, key = None):
        self.description = description
        self.enemy_chance = enemy_chance
        self.loot_chance = loot_chance
        self.enemy_type = enemy_type
        self.loot = loot_type
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