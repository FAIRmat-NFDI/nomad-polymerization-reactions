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
    result = invoke_cli(
        cli,
        ['create-archive', 'tests/data/processed_reactions/paper_0_reaction_1.json'],
    )
    assert result.exit_code == 0
    assert 'Archive created successfully.' in result.output
    os.remove('paper_0_reaction_1.archive.yaml')
