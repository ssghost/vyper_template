import pytest
from brownie import Oracle
import ape_vyper as ape

@pytest.fixture(scope='session')
def oracle(project, deployer, signer):
    return deployer.deploy(project.Oracle, signer)

@pytest.fixture(scope='session')
def signer(accounts):
    return accounts[2]

def test_publish(chain, oracle, reader, deployer, encode_message):
    time, price = chain.pending_timestamp, int(1500e6)
    sig = signer.sign_message(encode_message(time, price))
    oracle.set_price(time, price, sig.v, sig.r, sig.s, sender = deployer)
    assert oracle.price == int(1500e6)

    price = int(2000e6)
    sig = signer.sign_message(encode_message(time, price))
    with ape.reverts():
        oracle.set_price(time, price, sig.v, sig.r, sig.s, sender = deployer)
    chain.pending_timestamp += 5 * 60
    time = chain.pending_timestamp
    sig = signer.sign_message(encode_message(time, price))
    oracle.set_price(time, price, sig.v, sig.r, sig.s, sender = deployer)
    assert oracle.price == int(2000e6) 

