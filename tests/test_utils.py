import json
import os

import pytest

from nomad_polymerization_reactions.utils import (
    generate_monomer_archive_from_json,
    generate_pr_archive_from_json,
)


@pytest.mark.parametrize(
    'filepath',
    [
        'tests/data/jsons/polymerization_10.1002_actp.1983.010340208_1.json',
        'tests/data/jsons/polymerization_10.1002_actp.1983.010340208_2.json',
    ],
)
def test_generate_pr_archive_from_json(filepath):
    output = generate_pr_archive_from_json(filepath)
    
    # Basic validation: check that output has correct structure
    assert 'data' in output
    assert output['data']['m_def'] == 'nomad_polymerization_reactions.schema_packages.polymerization.PolymerizationReaction'
    assert 'monomers' in output['data']
    assert 'reaction_conditions' in output['data']
    
    # Check that polymerization_method is used (not method)
    if 'polymerization_method' in output['data'].get('reaction_conditions', {}):
        assert 'method' not in output['data']['reaction_conditions']
    
    # Check that calculation_method is used (not determination_method)
    if 'calculation_method' in output['data'].get('reaction_conditions', {}):
        assert 'determination_method' not in output['data']['reaction_conditions']
    
    # Check that solvent_logP is used (not logP at top level)
    if 'solvent_logP' in output['data'].get('reaction_conditions', {}):
        assert 'logP' not in output['data']
    
    # Archive file should be created in tests/data/archive_jsons/
    if 'tests/data/jsons/' in filepath:
        archive_dir = filepath.replace('tests/data/jsons/', 'tests/data/archive_jsons/')
        archive_dir = os.path.dirname(archive_dir)
        archive_filename = os.path.basename(filepath).replace('.json', '.archive.json')
        generated_file = os.path.join(archive_dir, archive_filename)
        # Verify the file was created
        assert os.path.exists(generated_file), f'Archive file should be created at {generated_file}'


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
    
    # Archive file should be created in tests/data/archive_jsons/
    if 'tests/data/jsons/' in filepath:
        archive_dir = filepath.replace('tests/data/jsons/', 'tests/data/archive_jsons/')
        archive_dir = os.path.dirname(archive_dir)
        archive_filename = os.path.basename(filepath).replace('.json', '.archive.json')
        generated_file = os.path.join(archive_dir, archive_filename)
        # Verify the file was created
        assert os.path.exists(generated_file), f'Archive file should be created at {generated_file}'
