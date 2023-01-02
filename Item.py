from TextColour import TC

tc = TC()

class Item:
    def __init__(self, name, weight, health_recovery, value, description,type,equipped = False,equippable = False, item_colour="green", cost=0,):
        self.name = name
        self.weight = weight
        self.health_recovery = health_recovery
        self.value = value
        self.description = description
        self.equipped = equipped
        self.equippable = equippable
        self.item_colour = item_colour
        self.type = type
        self.cost = cost

    def colour(self):
        return tc.colour(self.item_colour)