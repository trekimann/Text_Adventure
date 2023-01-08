import pytest
import src

tc = src.TC()

@pytest.fixture
def setup():
    my_wallet = src.Wallet()
    value_of_1 = src.Money('Pound', 0.1, 1, 'A pound coin')
    value_of_5 = src.Money('Five Pound Note', 0.1, 5, 'A 5 pound note')
    value_of_10 = src.Money('Ten Pound Note', 0.1, 10, 'A 10 pound note')
    my_wallet.add_money(value_of_1,10)
    my_wallet.add_money(value_of_5,10)
    my_wallet.add_money(value_of_10,10)

    return my_wallet, value_of_1, value_of_5, value_of_10

@pytest.mark.test
def test_pay_money_transfers_money_from_one_wallet_to_another(setup):
    my_wallet, value_of_1, value_of_5, value_of_10 = setup
    wallet_2 = src.Wallet()
    wallet_2.add_money(value_of_5,1)

    my_wallet.pay_money(5, wallet_2)

    assert my_wallet.money[value_of_10.name]['count'] == 10
    assert my_wallet.money[value_of_5.name]['count'] == 9
    assert my_wallet.money[value_of_1.name]['count'] == 10

    assert wallet_2.money[value_of_5.name]['count'] == 2
    assert len(wallet_2.money) == 2

@pytest.mark.test
def test_give_change_breaks_up_change_into_coins(setup):
    my_wallet, value_of_1, value_of_5, value_of_10 = setup
    wallet_2 = src.Wallet()
    wallet_2.add_money(value_of_5,1)

    my_wallet.give_change(value_of_5, wallet_2)

    assert my_wallet.money[value_of_10.name]['count'] == 10
    assert my_wallet.money[value_of_5.name]['count'] == 11
    assert my_wallet.money[value_of_1.name]['count'] == 5

    assert wallet_2.money[value_of_1.name]['count'] == 5
    assert len(wallet_2.money) == 1

@pytest.mark.test
def test_my_wallet_has_not_enough_small_denominations_so_pay_money_invokes_give_change(setup):
    my_wallet, value_of_1, value_of_5, value_of_10 = setup
    wallet_2 = src.Wallet()
    wallet_2.add_money(value_of_1,10)

    my_wallet.remove_money(value_of_1, 10)
    my_wallet.remove_money(value_of_5, 10)
    my_wallet.pay_money(5, wallet_2)

    assert my_wallet.money[value_of_10.name]['count'] == 9
    assert my_wallet.money[value_of_1.name]['count'] == 5

    assert wallet_2.money[value_of_10.name]['count'] == 1
    assert wallet_2.money[value_of_1.name]['count'] == 5
    assert len(wallet_2.money) == 2