import random
from TextColour import TC
from Item import Item
from BaseClasses.Character import Character

tc= TC()

class Player(Character):
  def __init__(self, name, description, current_location=(0,0), max_moves = 100):
    super().__init__(
      name=name,
      description=description,
      health = 10,
      armour = 10)

    self.inventory = {}
    self.max_inventory_weight = 10
    self.current_location = current_location
    self.kills = 0
    self.bestiary = {}
    self.moves = max_moves

    default_key = Item("default",0,0,0,"","key",True,False)

    self.keys = {default_key.name:{"key":default_key,"count":max_moves}}
      
  def check_health(self):
    if self.health <= 0:
      print(f"{self.name} has died.")
    else:
      print(f"{self.name} has {tc.colour('green')}{self.health}{tc.colour()} hit points remaining.")

  def check_armour(self):
    if self.armour <= 0:
      print(f"{self.name} has no armour.")
    else:
      print(f"{self.name} armour has {tc.colour('blue')}{self.armour}{tc.colour()} hit points remaining.")

  def display_stats(self):
    self.check_health()
    self.check_armour()
    print("{} has killed {} enemies".format(self.name, self.kills))

  def add_to_inventory(self, item):
    if item is None:
      return
    # Check if adding the item to the inventory would exceed the maximum weight
    if self.get_inventory_weight() + item.weight > self.max_inventory_weight:
        print("Cannot add item to inventory. Exceeds maximum weight.")
        return
    # Check if its a key
    print(f"You got a {tc.colour(item.item_colour)}{item.name}{tc.colour()}")

    if item.type == "key":
      self.collect_key(item)
      return
    elif item.type == "weapon":
      self.equip_weapon(item)
    # Add item to inventory
    if item.name in self.inventory.keys():
      self.inventory[item.name]['count'] += 1
    else:
      self.inventory[item.name] = {'item':item,'count':1}

  def collect_key(self, key):
    # Check if the key is already there
    if key.name in self.keys.keys():
      self.keys[key.name]['count'] +=1
    else:
      self.keys[key.name]={"key": key, "count": 1}

  def get_inventory_weight(self):
    # Calculate total weight of items in inventory
    total_weight = 0
    for item in self.inventory:
        total_weight += self.inventory[item]['item'].weight
    return total_weight

  def check_inventory(self):
      print("Inventory:")
      for item_name in self.inventory:
          thing = self.inventory[item_name]['item']
          print(f"   {tc.colour(thing.item_colour)}{item_name}{tc.colour()} ({thing.weight}kg each) x{self.inventory[thing.name]['count']}")
          print(f"      "+thing.description)
      print("Keys:")
      for key_name in self.keys:
        if key_name != "default":
          key = self.keys[key_name]['key']
          print(f"   {tc.colour(key.item_colour)}{key_name}{tc.colour()} ({key.weight}kg each) x{self.keys[key.name]['count']}")
          print("      "+key.description)

  def use_item(self):
    fields = self.inventory.keys()
    print("What item do you want to use?")
    for field, in fields:
      print(f"    {field} x{self.inventory[field]['count']}")
    print("---------------")
    choice = input("Enter Selection: ")
    if choice in fields:
      print("---------------")

  def get_location(self):
    # return the current location of the player
    return self.current_location

  def move_location(self,x,y):
    # Move the player to a new map Square.
    self.current_location = x,y
    self.moves -= 1
    if self.moves < 0:
      self.health = 0

  # def attack(self):
  #     # Calculate the damage dealt to the player
  #     damage = round(random.uniform(1.8, 3.5),2)
  #     print(f"{self.name} attacks for {tc.colour('red')}{damage}{tc.colour()} points of damage.")
  #     return damage

  # def is_dead(self):
  #   if self.health <= 0:
  #     print("You Died")
  #   return self.health <= 0

  def enemy_killed(self, enemy):
    self.kills += 1
    if enemy.name not in self.bestiary:
      self.bestiary[enemy.name] = {'enemy': enemy, 'kill_count': 1}
    else:
      self.bestiary[enemy.name]['kill_count'] += 1

  def read_bestiary(self):
    if len(self.bestiary) == 0:
      print("You have not encountered any enemies yet")
    else:
      # have the dictionary looped through to find the names of all the enemies encountered
      # then let the user either exit or type in a specific creature to see its description and how many of them the player has killed.
      fields = self.bestiary.keys()
      print("What enemy are you reading about?")
      for field in fields:
        print(f"    {field}")
      print("---------------")
      choice = input("Enter Selection: ")
      if choice in fields:
        print("---------------")
        print(self.bestiary[choice]['enemy'].description)
        print("You have killed \033[1;32;40m{}\033[0;37;m {}'s".format(self.bestiary[choice]['kill_count'],self.bestiary[choice]['enemy'].name))
      else:
        print("Enemy not found")