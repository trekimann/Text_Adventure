from TextColour import TC
from Player import Player

tc = TC()

class Shop:
    def __init__(self, shop_items, cost_multiplier, shop_ID, currency_options):
        self.shop_items = shop_items
        self.cost_multiplier = cost_multiplier
        self.shop_ID = shop_ID
        self.currency_options = currency_options
    
    def use_shop(self, player: Player):
        if self.shop_ID == 0:
            return
        print(f"The shop stocks the following:")
        for item_name in self.shop_items.keys():
            product = self.shop_items[item_name][item_name]
            print(f"   {tc.colour(product.item_colour)}{item_name}{tc.colour()} ({product.weight}kg each) x{self.shop_items[item_name]['stock']}")
            print(f"      Cost: {tc.colour('yellow')}{product.cost*self.cost_multiplier}{tc.colour()}")
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
                if item_name in self.shop_items.keys():
                    product = self.shop_items[item_name][item_name]
                    if item_number <= int(self.shop_items[item_name]['stock']):
                        total = (product.cost * self.cost_multiplier) * item_number
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

    def buy_from_player(self, player: Player):
        player.display_inventory()
        while True:
            item_name = input("Enter the item name: ")
            item_number = int(input("How many do you want to sell?: "))
            if item_name in player.inventory.keys():
                product = player.inventory[item_name]['item']
                if int(player.inventory[item_name]['count']) <= item_number:
                    # add item to the shops stock
                    self.add_to_stock(product)
                    # remove the item from the players inventory
                    player.remove_from_inventory(product.name)
                    # give the player some money
                    for _ in range(product.value):
                        THIS NEEDS SORTING TO CALCULATE HOW MUCH OF MAXIMUM MONY TO GIVE TO THE PLAYER player.add_money(self.base_money_option)
                    break                    
                else:
                    print(f"You dont have {item_number} {tc.colour(product.item_colour)}{item_name}{tc.colour()} to sell")
            else:
                print("Product not recognised, please try again.")        
            print("   ------")

    def add_to_stock(self, product):
        if product.name in self.shop_items.keys():
            self.shop_items[product.name]['stock'] += 1
        else:
            self.shop_items[product.name] = {product.name: product, 'stock': 1}   

    def sell_to_player(self, player, item_name, item_number):
        product = self.shop_items[item_name][item_name]
        total_cost = (product.cost * self.cost_multiplier) * item_number
        player.remove_money(total_cost)
        for _ in range(item_number):
            player.add_to_inventory(product)
        self.shop_items[item_name]['stock'] -= item_number
        if self.shop_items[item_name]['stock'] == 0:
            del self.shop_items[item_name]
        print(f"You bought {item_number} {item_name} for {total_cost}")