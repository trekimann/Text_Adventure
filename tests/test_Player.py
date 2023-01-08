import pytest
import mock
import src

tc = src.TC()

@pytest.fixture
def setup():
    player = src.Player("God", "The creator of the universe", (0,0))
    loot = src.Item("Gold Coins", 1, 10, "A pile of gold coins", "treasure")
    return player, loot

@pytest.mark.test
def test_check_health_death(setup, capsys):
    player, loot = setup
    # Test that the player dies when their health is 0 or below
    player.health = 0
    player.check_health()
    captured = capsys.readouterr()
    assert f"{player.name} has died." in captured.out

@pytest.mark.test
def test_check_health_alive(setup, capsys):
    player, loot = setup
    # Test that the player's health is displayed when they are alive
    player.health = 5
    player.check_health()
    captured = capsys.readouterr().out
    assert f"{player.name} has {tc.colour('green')}5{tc.colour()} hit points remaining." in captured

@pytest.mark.test
def test_check_armour_more_than_0(setup, capsys):
    player, loot = setup
    # Test that the player's armour is displayed when it is more than 0
    player.armour = 5
    player.check_armour()
    captured = capsys.readouterr().out
    assert f"{player.name} armour has {tc.colour('blue')}{player.armour}{tc.colour()} hit points remaining." in captured


@pytest.mark.test
def test_check_armour_0(setup, capsys):
    player, loot = setup
    # Test that the player's armour is displayed when it is 0
    player.armour = 0
    player.check_armour()
    captured = capsys.readouterr().out
    assert f"{player.name} has no armour." in captured

@pytest.mark.test
def test_when_player_displays_stats_they_are_shown_the_kills(setup, capsys):
    player, loot = setup
    # Test that the player's kills are displayed when they are alive
    player.kills = 5
    player.display_stats()
    captured = capsys.readouterr().out
    assert f"{player.name} has killed {player.kills} enemies" in captured

@pytest.mark.test
def test_when_player_adds_to_inventory_and_item_is_None_then_return_False(setup):
    player, loot = setup
    # Test that the player's inventory is not updated when the item is None
    assert player.add_to_inventory(None) == False

@pytest.mark.test
def test_when_player_adds_to_inventory_and_item_is_not_None_then_return_True(setup):
    player, loot = setup
    # Test that the player's inventory is updated when the item is not None
    assert player.add_to_inventory(loot) == True

@pytest.mark.test
def test_when_player_adds_to_inventory_and_item_is_not_None_then_item_is_added_to_inventory(setup):
    player, loot = setup
    # Test that the player's inventory is updated when the item is not None
    player.add_to_inventory(loot)
    assert loot.name in player.inventory.keys()

@pytest.mark.test
def test_when_player_adds_to_inventory_and_item_is_type_key_then_collect_key_is_called(setup):
    player, loot = setup
    loot.type = "key"
    # Test that the player's collect_key method is called when the item is a key
    with mock.patch.object(player, 'collect_key') as mock_collect_key:
        player.add_to_inventory(loot)
        mock_collect_key.assert_called_once()

@pytest.mark.test
def test_when_player_adds_to_inventory_and_item_is_type_weapon_then_equip_weapon_is_called(setup):
    player, loot = setup
    loot.type = "weapon"
    # Test that the player's equip_weapon method is called when the item is a weapon
    with mock.patch.object(player, 'equip_weapon') as mock_equip_weapon:
        player.add_to_inventory(loot)
        mock_equip_weapon.assert_called_once()

@pytest.mark.test
def test_when_player_adds_to_inventory_and_item_is_type_money_then_add_money_is_called(setup):
    player, loot = setup
    loot.type = "money"
    # Test that the player's add_money method is called when the item is money
    with mock.patch.object(player, 'add_money') as mock_add_money:
        player.add_to_inventory(loot)
        mock_add_money.assert_called_once()

@pytest.mark.test
def test_when_player_adds_item_to_inventory_which_was_already_there_the_count_increases_by_one(setup):
    player, loot = setup
    # Test that the player's inventory is updated when the item is not None
    player.add_to_inventory(loot)
    player.add_to_inventory(loot)
    assert player.inventory[loot.name]['count'] == 2

@pytest.mark.test
def test_when_player_collects_key_then_key_is_added_to_keys(setup):
    player, loot = setup
    loot.type = "key"
    # Test that the player's keys are updated when they collect a key
    player.collect_key(loot)
    assert loot.name in player.keys