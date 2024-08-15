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


@cli.command(
    help='Create an archive from a JSON file containing polymerization reaction data.',
    name='create-archive',
)
@click.argument(
    'JSON_FILE_PATH',
    required=True,
    type=click.Path(exists=True),
)
def _create_archive(json_file_path):
    try:
        generate_archive_from_json(json_file_path)
        click.echo('Archive created successfully.')
    except Exception as e:
        click.echo(f'Archive creation failed. Error: {e}')
