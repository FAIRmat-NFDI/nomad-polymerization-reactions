import os

import pytest
from click.testing import CliRunner

from nomad_polymerization_reactions.cli import cli


def invoke_cli(*args, **kwargs):
    return CliRunner().invoke(*args, **kwargs)


def test_cli_help():
    result = invoke_cli(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output
    assert 'This is the entry point to nomad-polymerization-reactions' in result.output


def test_archive_help():
    result = invoke_cli(cli, ['archive', '--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output
    assert (
        'Generate an archive or archives from the specified JSON files or directories.'
        in result.output
    )


@pytest.mark.parametrize(
    'filepath',
    [
        'tests/data/jsons/monomer_1.json',
    ],
)
def test_archive_monomer(filepath):
    result = invoke_cli(cli, ['archive', filepath])
    assert result.exit_code == 0
    assert 'Monomer archive created at:' in result.output
    # Verify the file was created (now in tests/data/archive_jsons/)
    if 'tests/data/jsons/' in filepath:
        archive_dir = filepath.replace('tests/data/jsons/', 'tests/data/archive_jsons/')
        archive_dir = os.path.dirname(archive_dir)
        archive_filename = os.path.basename(filepath).replace('.json', '.archive.json')
        generated_file = os.path.join(archive_dir, archive_filename)
        assert os.path.exists(generated_file), f'Archive file should be created at {generated_file}'


@pytest.mark.parametrize(
    'filepath',
    [
        'tests/data/jsons/polymerization_10.1002_actp.1983.010340208_1.json',
        'tests/data/jsons/polymerization_10.1002_actp.1983.010340208_2.json',
    ],
)
def test_archive_polymerization_reactions(filepath):
    result = invoke_cli(cli, ['archive', filepath, '--mode', 'polymerization'])
    assert result.exit_code == 0
    assert 'Polymerization reaction archive created at:' in result.output
    # Verify the file was created (now in tests/data/archive_jsons/)
    if 'tests/data/jsons/' in filepath:
        archive_dir = filepath.replace('tests/data/jsons/', 'tests/data/archive_jsons/')
        archive_dir = os.path.dirname(archive_dir)
        archive_filename = os.path.basename(filepath).replace('.json', '.archive.json')
        generated_file = os.path.join(archive_dir, archive_filename)
        assert os.path.exists(generated_file), f'Archive file should be created at {generated_file}'
