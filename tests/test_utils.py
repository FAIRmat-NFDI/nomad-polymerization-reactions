import os

import pytest
import yaml
from nomad_polymerization_reactions.utils import generate_archive_from_json


@pytest.mark.parametrize(
    'params',
    [
        {
            'filepath': 'tests/data/processed_reactions/paper_0_reaction_1.json',
            'reference': (
                'tests/data/processed_reactions/paper_0_reaction_1.archive.yaml'
            ),
        },
        {
            'filepath': 'tests/data/processed_reactions/paper_5_reaction_1.json',
            'reference': (
                'tests/data/processed_reactions/paper_5_reaction_1.archive.yaml'
            ),
        },
        {
            'filepath': 'tests/data/processed_reactions/empty.json',
            'reference': ('tests/data/processed_reactions/empty.archive.yaml'),
        },
    ],
)
def test_generate_archive_from_llm_output(params):
    output = generate_archive_from_json(params['filepath'])
    with open(params['reference']) as f:
        reference = yaml.load(f, Loader=yaml.FullLoader)
    assert output == reference

    # remove the generated file
    generated_file = f'{params["filepath"].split("/")[-1].split(".")[0]}.archive.yaml'
    os.remove(generated_file)
