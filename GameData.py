import json

from Enemy import Enemy
from MapSquare import MapSquare
from Item import Item

class GameData:
    def __init__(self):
        self.player_data = {}
        self.enemy_options = {}
        self.map_data = {}
        self.map_data['map_squares'] = {}
        self.item_options = {}
    
    def load_from_json(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Map details
            self.map_data['map_size'] = (data['size']['width'], data['size']['height'])
            # Player starting Details 
            self.player_data['starting_location']=(data['playerData']['startingX'],data['playerData']['startingY'])
            # Loot options
            for loot_options in data['items']:
              loot = Item(
                name = loot_options['name'],
                weight= loot_options['weight'],
                health_recovery=loot_options['healthRecovery'],
                value=loot_options['value'],
                description=loot_options['description'],
                equipped=False,
                equippable=loot_options['equippable'],
                item_colour=loot_options['colour'],
                type=loot_options['itemType'],
                cost=loot_options['cost'])
              self.item_options[loot.name] = loot

            # Enemy Options
            for enemy_options in data["enemies"]:
              enemy = Enemy(
                enemy_type = enemy_options['enemyType'],
                name = enemy_options['name'],
                description = enemy_options['description'],
                health = enemy_options['health'],
                loot_chance = enemy_options['loot_chance'],
                loot = self.item_options[enemy_options['loot']],
                damage_resistance_multiplier = enemy_options['damage_resistance_multiplier'],
                attack_multiplier = enemy_options['attack_multiplier']
              )
              self.enemy_options[enemy.enemy_type]=enemy
            # map grid details
            for square_data in data['mapSquares']:
                square = MapSquare(
                    description=square_data['description'],
                    enemy_chance=square_data['chanceOfEnemies'],
                    loot_chance=square_data['chanceOfLoot'],
                    enemy_type=square_data['enemyType'],
                    loot=self.item_options[square_data['lootName']],
                    loot_amount=square_data['lootAmount'],
                    enemy_options=self.enemy_options[square_data['enemyType']],
                    key=square_data['requiredKey']
                )
                self.map_data['map_squares'][(square_data['coordinates'][0], square_data['coordinates'][1])] = square

        print("Data Loaded")