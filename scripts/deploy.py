from brownie import network, config, accounts, ERC20

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

SUPPLY_TOKEN = 100
def deployToken(account):
    token = ERC20.deploy(SUPPLY_TOKEN, {"from": account})
    return token

def main():
    account = get_account()
    deployToken(account)