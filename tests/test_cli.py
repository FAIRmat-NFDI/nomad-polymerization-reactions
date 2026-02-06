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
    os.remove(filepath.split('/')[-1].replace('.json', '.archive.json'))


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
    os.remove(filepath.split('/')[-1].replace('.json', '.archive.json'))
