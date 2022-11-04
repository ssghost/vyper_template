import click
import dotenv
from ape_vyper import project
from ape_vyper.cli import NetworkBoundCommand, account_option

@click.command(cls=NetworkBoundCommand)
@account_option
@click.option(
    "--signer",
    default = dotenv.COINBASE_SIGNER,
)
def cli(account, signer):
    account.deploy(project.Oracle, signer)