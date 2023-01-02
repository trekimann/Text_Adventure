from Battle import Battle
from TextColour import TC

tc = TC()

class Map:
    def __init__(self, map_data, enemy_options):
        if map_data['map_size'] is None:
          self.size = (0, 0)
        else:
          self.size = map_data['map_size']

        self.map_squares = map_data['map_squares']
        self.enemy_options = enemy_options

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
        battle = Battle(player = player, enemy = enemy)
        if battle.start():
          location.enemy_killed()
      else:
        print("Nothing to fight")

      if location.has_loot():
        # trigger looting option
        print("Something to pick up")
        location.loot_location(player)
      else:
        print("Nothing to pick up")

    def try_to_move(self, direction, x, y):
      # try to move the player in this direction.
      if direction == "north":
        x = x + 1
      elif direction == "east":
        y = y + 1
      elif direction == "south":
        x = x - 1
      elif direction == "west":
        y = y - 1
      else:
        print(direction + "is not valid for moving")
      return x,y

    def read_map(self):
      print("Enter grid reference to see its description")
      x = int(input("Enter X reference: "))
      y = int(input("Enter Y reference: "))
      print("---------------")
      if self.viable_grid(x,y):
        # show the description of the grid
        print(self.get_location(x,y).description)
      else:
        print("That is not a valid grid")
