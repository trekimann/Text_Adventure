import src

tc = src.TC()

class Map:
    def __init__(self, map_data, enemy_options):
        if map_data['map_size'] is None:
          self.size = (0, 0)
        else:
          self.size = map_data['map_size']

        self.map_squares = map_data['map_squares']
        self.enemy_options = enemy_options
        self.map_description = map_data['map_description']

    def print_map_description(self):
      print(f"{self.map_description}")

    def get_location(self, x, y):
      if self.viable_grid(x, y):
        return self.map_squares[(x, y)]
      else:
        return None

    def viable_grid(self,x,y):
      if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
        return False
      else:
        return True

    def check_location(self, x, y, keys):
    # Check if the coordinates are within the bounds of the map
      if self.viable_grid(x,y):
        # Get the map square at the given coordinates
        map_square = self.map_squares[(x,y)]
        
        # Check if the player has a key
        if map_square.key in keys.keys():
          if map_square.key != "default":
            key= keys[map_square.key]['key']
            print(f"You have the required {tc.colour(key.item_colour)}{map_square.key}{tc.colour()}")  
          return True
        else:
          print(f"You do not have the {tc.colour('yellow')}{map_square.key}{tc.colour()} needed to go here")
          return False

    def check_encounters(self, x,y, player):
      # check the contents of the map square
      location = self.map_squares[(x, y)]
      print(f"{location.description}")
      if location.has_enemy():
        # trigger fight
        enemy = self.enemy_options[location.enemy_type]
        enemy.reset()
        battle = src.Battle(player = player, enemy = enemy)
        if battle.start():
          location.enemy_killed()
      location.loot_location(player)

      if location.has_shop():
        print(f"There is a shop here. Do you want to use it?")
        choice = input("Yes or No?: ")
        if choice.lower().startswith('y'):
          location.use_shop(player)
      
    def try_to_move(self, direction, x, y):
      # try to move the player in this direction.
      # get the map square that the player is currently on
      map_square = self.map_squares[(x,y)]
      # check if the player can move in this direction
      if direction in map_square.available_directions:
        if direction == "north":
          y = y + 1
        elif direction == "east":
          x = x + 1
        elif direction == "south":
          y = y - 1
        elif direction == "west":
          x = x - 1
        else:
          print(direction + "is not valid for moving")
      else:
        print(f"You cannot move in that direction. You can move in the following directions: {map_square.available_directions}")
      return x,y

    def read_map(self):
      self.print_map_description()
      print("Enter a grid reference to see its description")
      x = int(input("Enter X reference: "))
      y = int(input("Enter Y reference: "))
      print("---------------")
      if self.viable_grid(x,y):
        # show the description of the grid
        mapSquare = self.get_location(x,y)
        print(mapSquare.description)
        if mapSquare.shop_ID != 0:
          print(f"There is a {tc.colour('bright blue')}shop{tc.colour()} here.")
      else:
        print("That is not a valid grid")
