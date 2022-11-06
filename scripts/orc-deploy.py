import click
import os
from ape_vyper import project
from ape_vyper.cli import NetworkBoundCommand, account_option

@click.command(cls=NetworkBoundCommand)
@account_option
@click.option(
    "--signer",
    default = os.getenv('COINBASE_SIGNER'),
)
def cli(account, signer):
    account.deploy(project.Oracle, signer)