import click

from nomad_polymerization_reactions.utils import generate_archive_from_json


@click.group(
    help="""
    This is the entry point to nomad-polymerization-reactions's command line interface
    CLI. This CLI provides a set of commands to interact with the utility functions
    of the package.
    """,
)
def cli():
    pass
