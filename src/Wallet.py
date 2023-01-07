from Money import Money
from TextColour import TC

tc = TC()

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
            money:Money = self.money[money_type]['item']
            print(f"   {tc.colour(money.item_colour)}{money_type}{tc.colour()} ({money.weight}kg each) x{self.money[money_type]['count']}")
            print("      "+money.description)
            money_value += money.value * self.money[money_type]['count']
        print(f"Money total value: {money_value}")

    def add_money(self, money, count = 1):
        # Add item to inventory
        if money.name in self.money.keys():
            self.money[money.name]['count'] += count
        else:
            self.money[money.name] = {'item':money,'count':count}
        return True
    
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
                total_paid += self.money[money] * money_value
                target_wallet.add_money(self.money[money]['item'], self.money[money]['count'])
                del self.money[money]
            # If the desired amount has been reached, break out of the loop
            if total_paid == amount:
                break
