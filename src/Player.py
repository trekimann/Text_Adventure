import src

tc= src.TC()

class Player(src.Character):
  def __init__(self, name, description, current_location=(0,0), max_moves = 100):
    super().__init__(
      name=name,
      description=description,
      health = 10,
      armour = 10)

    self.inventory = {}
    self.max_inventory_weight = 25
    self.current_location = current_location
    self.kills = 0
    self.bestiary = {}
    self.moves = max_moves
    self.wallet = src.Wallet()
    self.keys = {
      "default": {
        "key": src.Item("default", 0, 0, 0, "", "key", True, False),
        "count": max_moves,
      }
    }

  def moves_remaining(self):
    print(f"You have {tc.colour('yellow')}{self.moves}{tc.colour()} moves remaining.")
    return self.moves
      
  def check_health(self):
    if self.health <= 0:
      print(f"{self.name} has died.")
    else:
      print(f"{self.name} has {tc.colour('green')}{self.health}{tc.colour()} hit points remaining.")
    return self.health

  def check_armour(self):
    if self.armour <= 0:
      print(f"{self.name} has no armour.")
    else:
      print(f"{self.name} armour has {tc.colour('blue')}{self.armour}{tc.colour()} hit points remaining.")
    return self.armour

  def display_stats(self):
    self.check_health()
    self.check_armour()
    self.moves_remaining()
    print(f"{self.name} has killed {self.kills} enemies")

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
    return self.wallet.add_money(money)

  def remove_from_inventory(self, item_name, count=1):
    count = int(count)
    if item_name not in self.inventory.keys():
        print("Item not in inventory.")
        return False
    if self.inventory[item_name]['count'] < int(count):
        print("Not enough of that item in inventory.")
        return False

    item = self.inventory[item_name]['item']
    if item.equipped:
      print(f"You cant remove an equipped item")
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
      total_weight += self.inventory[item]['item'].weight * self.inventory[item]['count']
    total_weight += self.wallet.wallet_weight()

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
    self.wallet.flash_cash()
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
    choice = input("Do you want to use something? Yes or No: ")
    if choice.lower().startswith('y'):
      self.use_item()

  def wallet_value(self):
    return self.wallet.wallet_value()

  def use_item(self):
    fields = self.inventory.keys()
    print("What item do you want to use?")
    for field in fields:
      item = self.inventory[field]
      print(f"    {tc.colour(item['item'].item_colour)}{field}{tc.colour()} x{item['count']}")
    print("---------------")
    choice = input("Enter Selection: ")
    amount = int(input("How many do you want to use?: "))
    if choice in fields:
      item = self.inventory[choice]['item']
      if self.inventory[choice]['count'] >= amount:
        for _ in range(amount):
          if item.type == "weapon":
            self.equip_weapon(item)
          elif item.type == "health":
            self.use_health_item(item)
          elif item.type == "armour":
            self.use_armour_item(item)
        print("---------------")
      else:
        print(f"You only have {self.inventory[choice]['count']} of {choice}")

  def use_armour_item(self, item):
    self.armour += item.health_recovery
    self.inventory[item.name]['count'] -= 1
    print(f"{tc.colour(item.item_colour)}{item.name}{tc.colour()} used. Armour recovered by {item.health_recovery}.")
    if self.inventory[item.name]['count'] == 0:
      print(f"All {tc.colour(item.item_colour)}{item.name}{tc.colour()} used")
      del self.inventory[item.name]

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
    self.moves_remaining()
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