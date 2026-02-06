import json
import os

import pytest

from nomad_polymerization_reactions.utils import (
    generate_monomer_archive_from_json,
    generate_pr_archive_from_json,
)


@pytest.mark.parametrize(
    'filepath,reference',
    [
        (
            'tests/data/jsons/polymerization_10.1002_actp.1983.010340208_1.json',
            'tests/data/archive_jsons/polymerization_10.1002_actp.1983.010340208_1.archive.json',
        ),
        (
            'tests/data/jsons/polymerization_10.1002_actp.1983.010340208_2.json',
            'tests/data/archive_jsons/polymerization_10.1002_actp.1983.010340208_2.archive.json',
        ),
    ],
)
def test_generate_pr_archive_from_json(filepath, reference):
    output = generate_pr_archive_from_json(filepath)
    with open(reference, encoding='utf-8') as f:
        reference_data = json.load(f)
    assert output == reference_data

    # remove the generated file
    generated_file = f'{filepath.split("/")[-1].split(".")[0]}.archive.json'
    os.remove(generated_file)


@pytest.mark.parametrize(
    'filepath,reference',
    [
        (
            'tests/data/jsons/monomer_1.json',
            'tests/data/archive_jsons/monomer_1.archive.json',
        ),
    ],
)
def test_generate_monomer_archive_from_json(filepath, reference):
    output = generate_monomer_archive_from_json(filepath)
    with open(reference, encoding='utf-8') as f:
        reference_data = json.load(f)
    assert output == reference_data

    # remove the generated file
    generated_file = f'{filepath.split("/")[-1].split(".")[0]}.archive.json'
    os.remove(generated_file)
