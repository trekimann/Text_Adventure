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

    def loot_location(self, player: Player):
        lootable = random.random() < self.loot_chance
        if lootable:
            # Display the loot at the location
            self.loot.item_description()
            print(f"X{self.loot_amount}")
            
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
                    print(f"{player.name} inventory weight: {player.get_inventory_weight()}/{player.max_inventory_weight}")
                    print(f"Do you want to drop something?")
                    choice = input("Yes or No: ")
                    if choice.lower().startswith('y'):
                        item_name = input("Enter the item name: ")
                        item_number = input("How many do you want to drop?: ")
                        player.remove_from_inventory(item_name, item_number)                    
                elif action == "2":
                    amount_to_loot = 1
                    if self.loot_amount > 1:
                        amount_to_loot = int(input(f"How many do you want to collect?: "))
                    THIS NEEDS SORTING
                    for _ in range(amount_to_loot):                        
                        picked_up = player.add_to_inventory(self.loot)
                        if not picked_up:
                            print(f"Unable to collect {self.loot.name}")
                            break
                    action_loop = False
                    return lootable
                    
                elif action == "3":
                    action_loop = False
                    return lootable
                else:
                    print(f"{action} :not valid choice. Please use a number")
                

        return lootable
    
    def enemy_killed(self):
        self.dead_enemies += 1