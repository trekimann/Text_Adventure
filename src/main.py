import sys
sys.path.append("../Text_Adventure")

import src

tc = src.TC()

class TextAdventureGame:
  def __init__(self):
    self.player = None
    self.current_map = None
    self.game_data = None
    self.print_break = "---------------------------------------" 
  def start_game(self):

    # Load game Data
    map_choice = input("Pick a map: ")
    game_json = "src/Maps/"+map_choice+".json"
    self.game_data = src.GameData()
    self.game_data.load_from_json(game_json)

    # Get player name and description
    name = input("Enter your name: ")
    description = input("Enter your description: ")
    
    # Create player object
    self.player = src.Player(name, description, self.game_data.player_data['starting_location'])
    # Give player default items
    if self.game_data.player_data['starting_weapon'] is None:
      self.player.add_to_inventory(src.Weapon(
      name = "Rusty Sword", 
      weight = 1,
      health_recovery = 0,
      value = 10,
      description = "A Rusty Sword, should be ok against many things",
      equipped = True,
      equippable = True,
      item_colour = "brown",
      type="weapon",
      damage_range=(0.1,1),
      damage_modifier=2))
    else:
      self.player.add_to_inventory(self.game_data.player_data['starting_weapon'])
    if self.game_data.player_data['starting_armour'] != None:
      self.player.armour = self.game_data.player_data['starting_armour']
    if self.game_data.player_data['starting_health'] != None:
      self.player.health = self.game_data.player_data['starting_health']
    if self.game_data.player_data['starting_carry_weight'] != None:
      self.player.carry_weight = self.game_data.player_data['starting_carry_weight']
    # Create map object
    self.current_map = src.Map(self.game_data.map_data, self.game_data.enemy_options)

  def play(self):
    # Display starting location and options
    self.display_location()
    self.display_options()
    self.current_map.print_map_description()
    
    # Main game loop

    while not self.player.is_dead():
      # Get player input
      action = input("Enter your action: ").lower()
      
      # Process player input
      if action == "north":
        self.player_move(action)
      elif action == "east":
        self.player_move(action)
      elif action == "south":
        self.player_move(action)
      elif action == "west":
        self.player_move(action)
      elif action == "location":
        self.display_location(True)
      elif action == "inventory":
        self.player.check_inventory()
      elif action == "stats":
        self.player.display_stats()
      elif action == "use":
        self.player.use_item()
      elif action == "map":
        self.current_map.read_map()
      elif action == "bestiary":
        self.player.read_bestiary()
      else:
        print("Invalid action")
        continue
        
      # Check if player is dead
      if self.player.is_dead():
        print("You have died.")
        break
        
      # Display location and options
      print(self.print_break)      
      self.display_location()
      self.display_options()
    
    print(self.print_break)
    print(f"{tc.colour('red')}GAME OVER{tc.colour()}")
    print(self.print_break)
    self.player.display_stats()
    print(self.print_break)

      
  def display_location(self, from_instructions = False):
    # Get current location data
    x, y = self.player.get_location()
    location: src.MapSquare = self.current_map.get_location(x, y)
    
    # Display location description
    print(f"Current Location: X:{x} Y:{y}")
    print(location.description)
    if location.has_shop() and from_instructions:
      print(f"There is a shop here. Do you want to use it?")
      choice = input("Yes or No?: ")
      if choice.lower().startswith('y'):
        location.use_shop(self.player)
    
  def display_options(self):
    print(f"Options:")
    print(f"  {tc.colour('red')}north")
    print(f"  east")
    print(f"  south")
    print(f"  west")
    print(f"  {tc.colour('green')}location")
    print(f"  inventory")
    print(f"  stats")
    print(f"  map")
    print(f"  bestiary{tc.colour()}")
    
  def player_move(self, direction):
    current_x, current_y = self.player.get_location()
    new_x, new_y = self.current_map.try_to_move(direction.lower(), current_x, current_y)
    if self.current_map.check_location(new_x, new_y, self.player.keys):
        self.player.move_location(new_x, new_y)
        self.current_map.check_encounters(new_x, new_y, self.player)


# Start the game
game = TextAdventureGame()
game.start_game()
game.play()
