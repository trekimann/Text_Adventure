from TextColour import TC
from BaseClasses.Item import Item
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
    self.money = {}
    self.keys = {
      "default": {
        "key": Item("default", 0, 0, 0, "", "key", True, False),
        "count": max_moves,
      }
    }
      
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
      return False
    # Check if adding the item to the inventory would exceed the maximum weight
    if self.get_inventory_weight() + item.weight > self.max_inventory_weight:
        print("Cannot add item to inventory. Exceeds maximum weight.")
        return False

    # Check if its a key
    if item.type == "key":
      return self.collect_key(item)
    elif item.type == "weapon":
      self.equip_weapon(item)
    elif item.type == "money":
      return self.add_money(item)
      
    # Add item to inventory
    if item.name in self.inventory.keys():
      self.inventory[item.name]['count'] += 1
    else:
      self.inventory[item.name] = {'item':item,'count':1}
    
    print(f"You got a {tc.colour(item.item_colour)}{item.name}{tc.colour()}")
    return True
  
  def add_money(self, money):
      # Add item to inventory
    if money.name in self.money.keys():
      self.money[money.name]['count'] += 1
    else:
      self.money[money.name] = {'item':money,'count':1}
    return True

  def remove_money(self, amount):
    # Sort the money in the player's inventory by value in descending order
    sorted_money = sorted(self.money.items(), key=lambda x: x[1], reverse=True)
    
    # Initialize a counter for the total value of money removed
    total_removed = 0
    
    # Iterate through the sorted money
    for money_name, money_value in sorted_money:
      if money_value > amount:
        continue
      # Calculate the number of this type of money needed to reach the desired amount
      num_needed = (amount - total_removed) // money_value
      # If there are enough of this type of money, remove them all
      if num_needed <= self.money[money_name]:
          total_removed += num_needed * money_value
          self.money[money_name] -= num_needed
      # If there are not enough of this type of money, remove as many as possible
      else:
          total_removed += self.money[money_name] * money_value
          del self.money[money_name]
      # If the desired amount has been reached, break out of the loop
      if total_removed == amount:
          break    
    # Return the total value of money removed
    return total_removed

  def remove_from_inventory(self, item_name, count=1):
    if item_name not in self.inventory.keys():
        print("Item not in inventory.")
        return False
    if self.inventory[item_name]['count'] < int(count):
        print("Not enough of that item in inventory.")
        return False

    self.inventory[item_name]['count'] -= count
    if self.inventory[item_name]['count'] == 0:
        del self.inventory[item_name]
    print(f"{count} {item_name} removed from inventory.")
    return True

  def collect_key(self, key):
    # Check if the key is already there
    if key.name in self.keys.keys():
      self.keys[key.name]['count'] +=1
    else:
      self.keys[key.name]={"key": key, "count": 1}
    return True

  def get_inventory_weight(self):
    # Calculate total weight of items in inventory
    total_weight = 0
    for item in self.inventory:
      total_weight += self.inventory[item]['item'].weight
    for money in self.money:
      total_weight += self.money[money]['item'].weight

    return total_weight

  def display_inventory(self):
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
    print("Money:")
    money_value = 0
    for money_type in self.money:
      money = self.money[money_type]['item']
      print(f"   {tc.colour(money.item_colour)}{money_type}{tc.colour()} ({money.weight}kg each) x{self.money[money_type]['count']}")
      print("      "+money.description)
      money_value += money.value * self.money[money_type]['count']
    print(f"Money total value: {money_value}")
    print(f"Equipped weapon: {tc.colour(self.weapon.item_colour)}{self.weapon.name}{tc.colour()}")
    print(f"{self.name} inventory weight: {self.get_inventory_weight()}/{self.max_inventory_weight}")

  def check_inventory(self):
    self.display_inventory()
    print(f"Do you want to drop something?")
    choice = input("Yes or No: ")
    if choice.lower().startswith('y'):
        item_name = input("Enter the item name: ")
        item_number = input("How many do you want to drop?: ")
        decision = input(f"Are you sure you want to permanently discard {item_name} x{item_number}? Yes or No: ")
        if decision.lower().startswith('y'):
          self.remove_from_inventory(item_name, item_number)
    choice = input("Do ou want to use something? Yes or No: ")
    if choice.lower().startswith('y'):
      self.use_item()

  def wallet_value(self):
    money_value = 0
    for money_type in self.money:
      money = self.money[money_type]['item']
      money_value += money.value * self.money[money_type]['count']
    return money_value

  def use_item(self):
    fields = self.inventory.keys()
    print("What item do you want to use?")
    for field in fields:
      item = self.inventory[field]
      print(f"    {tc.colour(item['item'].item_colour)}{field}{tc.colour()} x{item['count']}")
    print("---------------")
    choice = input("Enter Selection: ")
    if choice in fields:
      item = self.inventory[choice]['item']
      if item.type == "weapon":
        self.equip_weapon(item)
      elif item.type == "health":
        self.use_health_item(item)
      elif item.type == "armour":
        self.use_armour_item(item)
      print("---------------")

  def use_armour_item(self, item):
    self.armour += item.health_recovery
    self.inventory[item.name]['count'] -= 1
    if self.inventory[item.name]['count'] == 0:
      print(f"All {tc.colour(item.item_colour)}{item.name}{tc.colour()} used")
      del self.inventory[item.name]
    print(f"{tc.colour(item.item_colour)}{item.name}{tc.colour()} used. Armour recovered by {item.health_recovery}.")

  def use_health_item(self, item):
    self.health += item.health_recovery
    self.inventory[item.name]['count'] -= 1
    if self.inventory[item.name]['count'] == 0:
      print(f"All {tc.colour(item.item_colour)}{item.name}{tc.colour()} used")
      del self.inventory[item.name]
    print(f"{tc.colour(item.item_colour)}{item.name}{tc.colour()} used. Health recovered by {item.health_recovery}.")

  def get_location(self):
    # return the current location of the player
    return self.current_location

  def move_location(self,x,y):
    # Move the player to a new map Square.
    self.current_location = x,y
    self.moves -= 1
    if self.moves < 0:
      self.health = 0

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