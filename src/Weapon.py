from BaseClasses.Item import Item

class Weapon(Item):
    def __init__(self, name, weight, health_recovery, value, description,type,equipped = False,equippable = False, item_colour="green", cost=0, damage_modifier = 1, damage_range = (0.1, 1)):
        super().__init__(name=name, weight=weight,health_recovery=health_recovery,value=value,description=description,equippable=equippable, equipped=equipped, item_colour=item_colour,cost=cost, type=type)
        self.damage_modifier = damage_modifier
        self.damage_range = damage_range