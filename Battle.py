import random

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def start(self):
    # Print a message to let the player know they are being attacked by an enemy
        print("---------------")
        print(f"You are being attacked by a {self.enemy.name}!")

        # Enter a loop to handle the combat
        while True:
            print("---------------")
            # Check if the player or enemy is dead
            if self.player.is_dead():
                print("You have been defeated!")
                return False
            elif self.enemy.is_dead():
                print(f"{self.enemy.name} has been defeated!")
                loot = self.enemy.drop_loot()
                self.player.add_to_inventory(loot)
                self.player.enemy_killed(self.enemy)
                return True

            # Display options for the player to choose from
            print("What do you want to do?")
            print("1. Attack")
            print("2. Use item")
            print("3. Flee")

            # Get the player's choice
            choice = input("Enter choice: ")
            print("---------------")
            # Handle the player's choice
            if choice == "1":
                self.combat()
            elif choice == "2":
                # Get a list of items in the player's inventory
                items = []
                for i, item in enumerate(self.player.inventory):
                    items.append(f"{i+1}. {item.name}")
                # Print the list of items
                print("Which item do you want to use?")
                for item in items:
                    print(item)
                # Get the player's choice
                choice = input("Enter choice: ")
                # Use the item
                self.player.use_item(self.player.inventory[int(choice)-1])
            elif choice == "3":
                # Roll a random number between 0 and 1
                if random.uniform(0, 1) < 0.5:
                    # Flee successful
                    print(f"You fled from the {self.enemy.name}!")
                    break
                else:
                    # Flee unsuccessful
                    print(f"You failed to flee from the {self.enemy.name}!")
                    self.player.take_damage(self.enemy.attack())
            else:
                print("Invalid choice.")

    def combat(self):
        # deal with the fight here
        damage_dealt_player = self.player.attack()
        self.enemy.take_damage(damage_dealt_player)
        if not self.enemy.is_dead():
            damage_dealt_enemy = self.enemy.attack()
            self.player.take_damage(damage_dealt_enemy)
                