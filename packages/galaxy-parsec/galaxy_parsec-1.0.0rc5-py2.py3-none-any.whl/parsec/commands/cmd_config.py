import click
from parsec.commands.config.get_config import cli as func0

@click.group()
def cli():
	pass

cli.add_command(func0)
