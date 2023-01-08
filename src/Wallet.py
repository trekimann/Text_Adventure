import src

tc = src.TC()

class Wallet:
    def __init__(self):
        self.money = {}

    def wallet_value(self):
        money_value = 0
        for money_type in self.money:
            money = self.money[money_type]['item']
            money_value += money.value * self.money[money_type]['count']
        return money_value

    def wallet_weight(self):
        total_weight = 0
        if len(self.money) == 0:
            return total_weight
        for money in self.money:
            total_weight += (self.money[money]['item'].weight * self.money[money]['count'])
        return total_weight

    def flash_cash(self):
        money_value = 0
        for money_type in self.money:
            money:src.Money = self.money[money_type]['item']
            print(f"   {tc.colour(money.item_colour)}{money_type}{tc.colour()} ({money.weight}kg each) x{self.money[money_type]['count']}")
            print("      "+money.description)
            money_value += money.value * self.money[money_type]['count']
        print(f"Money total value: {money_value}")
        return money_value

    def add_money(self, money, count = 1):
        # Add item to inventory
        if money.name in self.money.keys():
            self.money[money.name]['count'] += count
        else:
            self.money[money.name] = {'item':money,'count':count}
        return True

    def remove_money(self, money, count = 1):
        if money.name in self.money.keys():
            self.money[money.name]['count'] -= count
            if self.money[money.name]['count'] <= 0:
                del self.money[money.name]
            return True
        else:
            return False
    
    def pay_money(self, amount, target_wallet):
    # Sort the money in the wallet by value in descending order
        sorted_money = sorted(self.money.items(), key=lambda x: x[1]['item'].value, reverse=True)

        # Initialize a counter for the total value of money paid
        total_paid = 0

        # Iterate through the sorted money
        for currency in sorted_money:
            money = currency[1]['item'].name
            money_value = self.money[money]['item'].value
            # Calculate the number of this type of money needed to reach the desired amount
            num_needed = (amount - total_paid) // money_value
            # If there are enough of this type of money, pay them all
            if num_needed <= self.money[money]['count']:
                total_paid += num_needed * money_value
                target_wallet.add_money(self.money[money]['item'], num_needed)
                self.money[money]['count'] -= num_needed
            # If there are not enough of this type of money, pay as many as possible
            else:
                total_paid += self.money[money]['count'] * money_value
                target_wallet.add_money(self.money[money]['item'], self.money[money]['count'])
                # del self.money[money]
            # If the desired amount has been reached, break out of the loop
            if total_paid == amount:
                break
        if total_paid != amount:
            #get the smallest denomination which would cover the remaining amount and get change for it from the other wallet, then pay the rest of the amount
            remaining_amount = amount - total_paid
            for currency in sorted_money:
                money = currency[1]['item']
                money_value = self.money[money.name]['item'].value
                if money_value >= remaining_amount:
                    target_wallet.give_change(money, self)
                    self.pay_money(remaining_amount, target_wallet)
                    break

    def give_change(self, money_to_break, target_wallet):
        # This method takes in a money object then breaks it down into the smallest possible denominations that the wallet holds and returns them to the target wallet

        # Sort the money in the wallet by value in descending order
        sorted_money = sorted(self.money.items(), key=lambda x: x[1]['item'].value, reverse=False)

        # Initialize a counter for the total value of money paid
        total_paid = 0

        # get the money to break downs value
        amount = money_to_break.value

        # Iterate through the sorted money
        for currency in sorted_money:
            money = currency[1]['item'].name
            money_value = self.money[money]['item'].value
            # Calculate the number of this type of money needed to reach the desired amount
            num_needed = (amount - total_paid) // money_value
            # If there are enough of this type of money, pay them all
            if num_needed <= self.money[money]['count']:
                total_paid += num_needed * money_value
                target_wallet.add_money(self.money[money]['item'], num_needed)
                self.money[money]['count'] -= num_needed
            # If there are not enough of this type of money, pay as many as possible
            else:
                total_paid += self.money[money]['count'] * money_value
                target_wallet.add_money(self.money[money]['item'], self.money[money]['count'])
                # del self.money[money]
            # If the desired amount has been reached, break out of the loop
            if total_paid == amount:
                self.add_money(money_to_break)
                target_wallet.remove_money(money_to_break)
                break
       
