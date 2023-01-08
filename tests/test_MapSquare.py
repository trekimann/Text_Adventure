import pytest
import mock

import src

@pytest.fixture
def setup():
    # Create a player and a MapSquare with loot
    player = src.Player('God', 'The creator of the universe', (0,0))
    player.max_inventory_weight = 2
    loot = src.Item("Gold Coins", 1, 10, "A pile of gold coins", "treasure")
    map_square = src.MapSquare("A room with loot", 0, 1, "None", [], loot)
    return player, loot, map_square

@pytest.mark.test
def test_loot_location_with_empty_inventory(setup):
    player, loot, map_square = setup
    # Test looting with an empty inventory
    with mock.patch('builtins.input', side_effect=['2','1']):
        lootable = map_square.loot_location(player)
    assert lootable == True
    assert len(player.inventory) == 1
    assert player.inventory[loot.name]['item'] == loot
    assert map_square.loot_amount == 0

@pytest.mark.test
def test_loot_location_with_full_inventory(setup):
    player, loot, map_square = setup
    # Test looting with a full inventory
    for _ in range(player.max_inventory_weight):
        player.add_to_inventory(loot)
    with mock.patch('builtins.input', side_effect=['2','1']):
        lootable = map_square.loot_location(player)
    assert lootable == True
    assert player.get_inventory_weight() == player.max_inventory_weight
    assert map_square.loot_amount == 1

@pytest.mark.test
def test_loot_location_with_partial_inventory(setup):
    player, loot, map_square = setup
    # Test looting with a partially full inventory
    start_weight = player.max_inventory_weight - 1
    for _ in range(start_weight):
        player.add_to_inventory(loot)
    with mock.patch('builtins.input', side_effect=['2','1']):
        lootable = map_square.loot_location(player)
    assert lootable == True
    assert player.get_inventory_weight() == start_weight +1
    assert map_square.loot_amount == 0

@pytest.mark.test
def test_loot_location_with_no_loot(setup):
    player, loot, map_square = setup
    # Test looting a location with no loot
    map_square.loot_amount = 0
    lootable = map_square.loot_location(player)
    assert lootable == False
    assert len(player.inventory) == 0

@pytest.mark.test
def test_loot_location_with_no_loot_chance(setup):
    player, loot, map_square = setup
    # Test looting a location with no loot chance
    map_square.loot_chance = 0
    lootable = map_square.loot_location(player)
    assert lootable == False
    assert len(player.inventory) == 0

@pytest.mark.test
def test_loot_location_with_no_loot_amount(setup):
    player, loot, map_square = setup
    # Test looting a location with no loot amount
    map_square.loot_amount = 0
    lootable = map_square.loot_location(player)
    assert lootable == False
    assert len(player.inventory) == 0

@pytest.mark.test
def test_loot_location_player_leaves_loot(setup):
    player, loot, map_square = setup
    # Test player leaving loot
    with mock.patch('builtins.input', side_effect=['3']):
        lootable = map_square.loot_location(player)
    assert lootable == True
    assert len(player.inventory) == 0
    assert map_square.loot_amount == 1

@pytest.mark.test
def test_loot_location_player_tried_to_take_more_than_available(setup, capsys):
    player, loot, map_square = setup
    map_square.loot_amount = 2
    # Test player trying to take more than available
    with mock.patch('builtins.input', side_effect=['2','3']):
        lootable = map_square.loot_location(player)
    assert lootable == True
    assert len(player.inventory) == 1
    assert player.inventory[loot.name]['count'] == 2
    assert map_square.loot_amount == 0
    captured = capsys.readouterr()
    assert  "Loot depleted" in captured.out

@pytest.mark.test
def test_player_selects_invalid_option(setup, capsys):
    player, loot, map_square = setup
    incorrect_input = 'God'
    expected_output = f"{incorrect_input} : not valid choice. Please use a number"
    # Test player selecting an invalid option
    with mock.patch('builtins.input', side_effect=[incorrect_input,'3']):
        lootable = map_square.loot_location(player)
    assert lootable == True
    assert len(player.inventory) == 0
    assert map_square.loot_amount == 1
    captured = capsys.readouterr().out
    assert  expected_output in captured