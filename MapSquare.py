import random
from Item import Item

from Player import Player

from TextColour import TC

tc = TC()
class MapSquare:
    def __init__(self, description, enemy_chance, loot_chance, enemy_type, enemy_options, loot: Item, loot_amount = 1, key = None, shop_ID = False, shop_items = None):
        self.description = description
        self.enemy_chance = enemy_chance
        self.loot_chance = loot_chance
        self.enemy_type = enemy_type
        self.loot = loot
        self.loot_amount = loot_amount
        self.enemy_options = enemy_options
        self.dead_enemies = 0
        self.key = key
        self.shop_ID = shop_ID
        self.shop_items = shop_items

    def has_shop(self):
        return self.shop_ID != 0

    def use_shop(self, player):
        if self.shop_ID == 0:
            return
        print(f"The shop stocks the following:")
        for item_name in self.shop_items['stock']:
            product = self.shop_items['stock'][item_name][item_name]
            print(f"   {tc.colour(product.item_colour)}{item_name}{tc.colour()} ({product.weight}kg each) x{self.shop_items['stock'][item_name]['stock']}")
            print(f"      Cost: {tc.colour('yellow')}{product.cost*self.shop_items['cost']}{tc.colour()}")
            if product.type in ('health', 'armour'):
                print(f"      Recovers {tc.colour(product.item_colour)}{product.health_recovery}{tc.colour()} hit points")
            print(f"      {product.description}")
        while True:
            print(f"Do you want to buy something?")
            choice = input("Yes or No: ")
            if choice.lower().startswith('y'):
                item_name = input("Enter the item name: ")
                item_number = int(input("How many do you want to buy?: "))
                # check total cost and if the player has that much money
                if item_name in self.shop_items['stock'].keys():
                    product = self.shop_items['stock'][item_name][item_name]
                    if item_number <= int(self.shop_items['stock'][item_name]['stock']):
                        total = (product.cost * self.shop_items['cost']) * item_number
                        if player.wallet_value() >= total:                            
                            self.sell_to_player(player, item_name, item_number)
                            break
                        else:
                            print(f"You have {player.wallet_value()}, you need {total} for this transaction")
                    else:
                        print(f"There are not enough {item_name} to buy")
                else:
                    print("Product not recognised, please try again.")        
                print("   ------")
            else:
                print(f"Do you want to Sell something?")
                choice = input("Yes or No: ")
                if choice.lower().startswith('y'):
                    self.buy_from_player(player)
                else:
                    break

    def buy_from_player(self, player):
        pass

    def sell_to_player(self, player, item_name, item_number):
        product = self.shop_items['stock'][item_name][item_name]
        total_cost = product.cost * item_number
        player.remove_money(total_cost)
        for _ in range(item_number):
            player.add_to_inventory(product)
        self.shop_items['stock'][item_name]['stock'] -= item_number
        if self.shop_items['stock'][item_name]['stock'] == 0:
            del self.shop_items['stock'][item_name]
        print(f"You bought {item_number} {item_name} for {total_cost}")


    def has_enemy(self):
        enemy_encounter = random.random() < self.enemy_chance
        return enemy_encounter

    def loot_location(self, player: Player):
        lootable = random.random() < self.loot_chance
        if not lootable or self.loot_amount<= 0:
            return False
        # Display the loot at the location
        self.loot.item_description()
        print(f"x{self.loot_amount}")
        
        action_loop = True
        # Present the player a chance to see their inventory
        # Present the player a chance to drop items from their inventory
        # Give the player the option to loot if they want.
        # Remove the loot from the location
        while action_loop:
            print(f"What do you want to do?")
            print(f"   1. Check inventory")
            print(f"   2. Pick up loot")
            print(f"   3. Leave loot")
            action = input("Enter choice: ")

            if action == "1":
                player.check_inventory()                  
            elif action == "2":
                amount_to_loot = 1
                if self.loot_amount > 1:
                    amount_to_loot = int(input(f"How many do you want to collect?: "))
                for _ in range(amount_to_loot):
                    if self.loot_amount >0:                        
                        picked_up = player.add_to_inventory(self.loot)
                        if not picked_up:
                            print(f"Unable to collect {self.loot.name}")
                            break
                        else:
                            self.loot_amount -= 1
                    else:
                        print(f"Loot depleted")
                        break
                action_loop = False
                return lootable
                
            elif action == "3":
                print(f"You didn't pick anything up, you can return later")
                action_loop = False
                return lootable
            else:
                print(f"{action} : not valid choice. Please use a number")                
        return lootable
    
    def enemy_killed(self):
        self.dead_enemies += 1