import src

class TemporaryEffectItem(src.Item):
    def __init__(self, name, weight, health_recovery, value, description, effect_duration, item_type, equipped = False, equippable = True, item_colour="green", cost=0):
        super().__init__(name=name, weight=weight, health_recovery=health_recovery, value=value, description=description, equippable=equippable, equipped=equipped, item_colour=item_colour, cost=cost, type=item_type)
        self.effect_duration = effect_duration
        self.current_duration = effect_duration

    def use(self, player: src.Player):
        # Apply the effect on the player
        player.health += self.health_recovery

        # Check if the effect brings the player's health above the maximum
        if player.health > player.max_health:
            player.health = player.max_health

        # Reset the current duration
        self.current_duration = self.effect_duration

    def update(self, player: src.Player):
        # Reduce the current duration by 1
        self.current_duration -= 1

        # Check if the effect has expired
        if self.current_duration <= 0:

            if player.health > player.max_health:
                player.health = player.max_health
