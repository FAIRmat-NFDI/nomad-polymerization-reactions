import glob
import os

from click.testing import CliRunner
from nomad_polymerization_reactions.cli import cli


def invoke_cli(*args, **kwargs):
    return CliRunner().invoke(*args, **kwargs)


def test_cli_help():
    result = invoke_cli(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output
    assert 'This is the entry point to nomad-polymerization-reactions' in result.output


def test_create_archive_help():
    result = invoke_cli(cli, ['create-archive', '--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output
    assert 'Create an archive from a JSON file' in result.output


def test_create_archive_success():
    files = glob.glob('tests/data/processed_reactions/*.json')
    result = invoke_cli(cli, ['create-archive', *files])
    assert result.exit_code == 0
    assert (
        'Archive created successfully.\nArchive created successfully.\n'
        in result.output
    )
    for file in files:
        os.remove(file.split('/')[-1].replace('.json', '.archive.yaml'))
