import pytest
import brownie
from brownie import advStorage
from scripts.deploy import *
from brownie.test import given, strategy

account = get_account()
token = deployToken(account)
@given(
    to=strategy('address', exclude=account),
    value=strategy('uint256', max_value=10000),
)
def test_transfer_amount(token, to, value):
    balance = token.balanceOf(account)
    token.transfer(to, value, {'from': account})

    assert token.balanceOf(account) == balance - value
    assert token.balanceOf(to) == value


INITIAL_VALUE = 8
@pytest.fixture
def adv_storage_contract(advStorage, accounts):
    yield advStorage.deploy(INITIAL_VALUE, {'from': accounts[0]})

def test_failed_transactions(adv_storage_contract, accounts):
    with brownie.reverts("No negative values"):
        adv_storage_contract.set(-10, {"from": accounts[1]})
        adv_storage_contract.set(150, {"from": accounts[1]})
        with brownie.reverts("Storage is locked when 100 or more is stored"):
            adv_storage_contract.set(10, {"from": accounts[1]})
        adv_storage_contract.reset({"from": accounts[1]})
        adv_storage_contract.set(10, {"from": accounts[1]})
        assert adv_storage_contract.storedData() == 10