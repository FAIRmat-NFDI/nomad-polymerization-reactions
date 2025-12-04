import os

import click

from nomad_polymerization_reactions.utils import (
    generate_monomer_archive_from_json,
    generate_pr_archive_from_json,
)


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
    name='archive',
    help="""
    Generate an archive or archives from the specified JSON files or directories.

        PATHS: Path to the JSON files or directories containing JSON files.
    """,
)
@click.argument(
    'PATHS',
    nargs=-1,
    required=True,
    type=click.Path(exists=True),
    # help='Path to the JSON file or directory containing JSON files.',
)
@click.option(
    '--mode',
    type=click.Choice(['monomer', 'polymerization'], case_sensitive=False),
    default='monomer',
    help='Specify the mode for archive creation. Choose "monomer" for monomer data '
    'and "polymerization" for polymerization reaction data.',
)
@click.option(
    '--same-dir',
    is_flag=True,
    default=False,
    help='Create the archive in the same directory as the input JSON file.',
)
def _create_monomer_archive(paths, mode, same_dir):
    try:
        if mode == 'polymerization':
            click.echo('Generating polymerization reaction archive(s)...')
            archive_generator = generate_pr_archive_from_json
        else:
            click.echo('Generating monomer archive(s)...')
            archive_generator = generate_monomer_archive_from_json
        all_json_paths = []
        for path in paths:
            if os.path.isdir(path):
                # if the argument is a directory, get all json files in it
                all_json_paths.extend(
                    [
                        os.path.join(path, f)
                        for f in os.listdir(path)
                        if f.endswith('.json')
                    ]
                )
            else:
                all_json_paths.append(path)
        for json_path in all_json_paths:
            archive_generator(json_path, same_dir_as_input=same_dir)
    except Exception as e:
        click.echo(f'Archive creation failed. Error: {e}')
