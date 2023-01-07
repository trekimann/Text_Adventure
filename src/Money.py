from BaseClasses.Item import Item

class Money(Item):
    def __init__(self, name, weight, value, description, item_colour="yellow"):
        super().__init__(name=name, weight=weight, value=value, description=description, item_colour=item_colour, type="money", cost=value)
