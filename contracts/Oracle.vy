# @version ^0.3.3

MAX_UPDATE_DELAY: constant(uint256) = 5*60

price: public(uint256)
oracle: public(address)
last_update: public(uint256)

@external
def __init__(oracle: address):
    self.oracle = oracle
    self.last_update = 0
    self.price = 0

@external
def set_price(time: uint256, price: uint256, r: uint256, s: uint256, v: uint256):
    assert block.timestamp - time <= MAX_UPDATE_DELAY
    assert block.timestamp >= self.last_update + MAX_UPDATE_DELAY 
    msg_abi: bytes32 = keccak256(_abi_encode(b"prices", time, b"ETH", price))
    msg_hash: bytes32 = keccak256(concat(b"\x19Ethereum Signed Message:\n32", msg_abi))
    signer: address = ecrecover(msg_hash, v, r, s)
    assert signer == self.oracle
    self.price = price
    self.last_update = time
