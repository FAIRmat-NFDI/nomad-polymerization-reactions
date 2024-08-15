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
    nargs=-1,
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    '--same-dir-as-input',
    is_flag=True,
    default=False,
    help='Create the archive in the same directory as the input JSON file.',
)
def _create_archive(json_file_path, same_dir_as_input):
    try:
        for file_path in json_file_path:
            generate_archive_from_json(file_path, same_dir_as_input)
            click.echo('Archive created successfully.')
    except Exception as e:
        click.echo(f'Archive creation failed. Error: {e}')
