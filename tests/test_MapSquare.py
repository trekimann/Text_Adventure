import unittest

from src.MapSquare import MapSquare
from src.BaseClasses.Item import Item
from src.Player import Player

class TestMapSquare(unittest.TestCase):
    def setUp(self):
        # Create a player and a MapSquare with loot
        self.player = Player()
        self.loot = Item("Gold Coins", 0.01, 10, "A pile of gold coins", "money")
        self.map_square = MapSquare("A room with loot", 0, 1, "None", [], self.loot)

    def test_loot_location_with_empty_inventory(self):
        # Test looting with an empty inventory
        lootable = self.map_square.loot_location(self.player)
        self.assertTrue(lootable)
        self.assertEqual(len(self.player.inventory), 1)
        self.assertEqual(self.player.inventory[0], self.loot)
        self.assertEqual(self.map_square.loot_amount, 0)

    def test_loot_location_with_full_inventory(self):
        # Test looting with a full inventory
        self.player.inventory = [self.loot] * self.player.inventory_size
        lootable = self.map_square.loot_location(self.player)
        self.assertTrue(lootable)
        self.assertEqual(len(self.player.inventory), self.player.inventory_size)
        self.assertEqual(self.map_square.loot_amount, 1)

    def test_loot_location_with_partial_inventory(self):
        # Test looting with a partially full inventory
        self.player.inventory = [self.loot] * (self.player.inventory_size - 1)
        lootable = self.map_square.loot_location(self.player)
        self.assertTrue(lootable)
        self.assertEqual(len(self.player.inventory), self.player.inventory_size)
        self.assertEqual(self.map_square.loot_amount, 0)

    def test_loot_location_with_no_loot(self):
        # Test looting a location with no loot
        self.map_square.loot_amount = 0
        lootable = self.map_square.loot_location(self.player)
        self.assertFalse(lootable)
        self.assertEqual(len(self.player.inventory), 0)

if __name__ == '__main__':
    unittest.main()
