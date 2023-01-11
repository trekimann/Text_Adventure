import json
import src


class GameData:
    def __init__(self):
        self.player_data = {}
        self.enemy_options = {}
        self.map_data = {}
        self.map_data['map_squares'] = {}
        self.item_options = {}
        self.store_options = {}
    
    def load_from_json(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            money = {}

            # Loot options
            for loot_options in data['items']:
              loot = self._create_item(loot_options)
              if loot.type == 'money':
                  money[loot.name] = loot
              self.item_options[loot.name] = loot

            # Shop Options            
            for shopItems in data["storeItems"]:
              stock = {}
              for item, value in shopItems['shopItems'].items():
                stock[item] = {item: self.item_options[item], "stock": value}
              wallet = src.Wallet()
              for currency in shopItems['shopWallet']:
                wallet.add_money(money[currency], shopItems['shopWallet'][currency])
              self.store_options[shopItems['shopID']] = src.Shop(
                shop_items=stock,
                cost_multiplier= shopItems['shopCost'],
                shop_ID=shopItems['shopID'],
                wallet=wallet)

            # Enemy Options
            for enemy_options in data["enemies"]:              
              self.enemy_options[enemy_options['enemyType']]=self._create_enemy(enemy_options)
            
            # Map details
            self.map_data['map_size'] = (data['size']['width'], data['size']['height'])
            self.map_data['map_description'] = data['mapDescription']
            # map grid details
            for square_data in data['mapSquares']:
                square = src.MapSquare(
                    description=square_data['description'],
                    enemy_chance=square_data['chanceOfEnemies'],
                    loot_chance=square_data['chanceOfLoot'],
                    enemy_type=square_data['enemyType'],
                    loot=self.item_options[square_data['lootName']],
                    loot_amount=square_data['lootAmount'],
                    enemy_options=self.enemy_options[square_data['enemyType']],
                    key=square_data['requiredKey'],
                    shop_ID=square_data['shopID'],
                    available_directions=square_data['canMove'],
                )
                if square.shop_ID !=0:
                  square.shop = self.store_options[square.shop_ID]
                
                self.map_data['map_squares'][(square_data['coordinates'][0], square_data['coordinates'][1])] = square
            
            # Player starting Details 
            self.player_data['starting_location']=(data['playerData']['startingX'],data['playerData']['startingY'])
            self.player_data['starting_health']=data['playerData']['startingHealth']
            self.player_data['maximum_health']=data['playerData']['maximumHealth']
            self.player_data['maximum_armour']=data['playerData']['maximumArmour']
            self.player_data['starting_armour']=data['playerData']['startingArmour']
            self.player_data['starting_weapon']=self.item_options[data['playerData']['startingWeapon']]
            self.player_data['starting_carry_weight']=data['playerData']['startingCarryWeight']

        print("Game Data Loaded")

    def _create_enemy(self, enemy_options):
      if enemy_options['boss'] == True:
        return src.Boss(
          enemy_type = enemy_options['enemyType'],
          name = enemy_options['name'],
          description = enemy_options['description'],
          health = enemy_options['health'],
          loot_chance = enemy_options['loot_chance'],
          loot = self.item_options[enemy_options['loot']],
          damage_resistance_multiplier = enemy_options['damage_resistance_multiplier'],
          attack_multiplier = enemy_options['attack_multiplier'],
          loot_amount = enemy_options['lootAmount'],
          weapon=self.item_options[enemy_options['weapon']],
          weak_against=self.item_options[enemy_options['weakAgainst']],
          weakness_multiplier=enemy_options['weaknessMultiplier'],
        )
      else:
        return src.Enemy(
          enemy_type = enemy_options['enemyType'],
          name = enemy_options['name'],
          description = enemy_options['description'],
          health = enemy_options['health'],
          loot_chance = enemy_options['loot_chance'],
          loot = self.item_options[enemy_options['loot']],
          damage_resistance_multiplier = enemy_options['damage_resistance_multiplier'],
          attack_multiplier = enemy_options['attack_multiplier'],
          loot_amount = enemy_options['lootAmount'],
          weapon=self.item_options[enemy_options['weapon']],
        )

    def _create_item(self, loot_options):
      item_type = loot_options['itemType']
      if item_type in ("health", 'armour', 'key', 'treasure', 'None'):
        return src.Item(
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
      elif loot_options['itemType'] == 'weapon':
        return src.Weapon(
        name = loot_options['name'],
        weight= loot_options['weight'],
        health_recovery=loot_options['healthRecovery'],
        value=loot_options['value'],
        description=loot_options['description'],
        equipped=False,
        equippable=loot_options['equippable'],
        item_colour=loot_options['colour'],
        type=loot_options['itemType'],
        cost=loot_options['cost'],
        damage_range=(loot_options['damageRangeMin'],loot_options['damageRangeMax']),
        damage_modifier=loot_options['damageModifier']
        )
      elif loot_options['itemType'] == "money":
        return src.Money(
          name = loot_options['name'],
          weight= loot_options['weight'],
          value=loot_options['value'],
          description=loot_options['description'],
        )