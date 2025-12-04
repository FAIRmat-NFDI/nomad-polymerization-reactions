import json
import os

import pytest

from nomad_polymerization_reactions.utils import generate_pr_archive_from_json


@pytest.mark.parametrize(
    'params',
    [
        {
            'filepath': 'tests/data/processed_reactions/paper_0_reaction_1.json',
            'reference': (
                'tests/data/processed_reactions/paper_0_reaction_1.archive.json'
            ),
        },
        {
            'filepath': 'tests/data/processed_reactions/paper_5_reaction_1.json',
            'reference': (
                'tests/data/processed_reactions/paper_5_reaction_1.archive.json'
            ),
        },
        {
            'filepath': 'tests/data/processed_reactions/empty.json',
            'reference': ('tests/data/processed_reactions/empty.archive.json'),
        },
    ],
)
def test_generate_archive_from_llm_output(params):
    output = generate_pr_archive_from_json(params['filepath'])
    with open(params['reference'], encoding='utf-8') as f:
        reference = json.load(f)
    assert output == reference

    # remove the generated file
    generated_file = f'{params["filepath"].split("/")[-1].split(".")[0]}.archive.json'
    os.remove(generated_file)
