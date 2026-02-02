import collections
import json
import os
from typing import Any

from ase.data import chemical_symbols
from nomad.units import ureg

from nomad_polymerization_reactions.models import (
    MonomerInput,
    PolymerizationReactionInput,
)


def generate_pr_archive_from_json(  # noqa: PLR0912, PLR0915
    filepath: str, same_dir_as_input: bool = False
) -> dict:
    """
    Generate an archive.json file for polymerization reactions from a JSON file.

    All of the following keys are supported and copied into the archive when present:
    monomer1, monomer2, monomer1_smiles, monomer2_smiles,
    r_values (constant_1, constant_2), conf_intervals (constant_conf_1, constant_conf_2),
    temperature, temperature_unit, solvent, polymerization_method, r-product, source,
    calculation_method (fallback to determination_method), polymerization_type, logP (fallback for solvent_logP),
    polytype_emb_1, polytype_emb_2, method_emb_1, method_emb_2,
    solvent_logP, solvent_TPSA, solvent_HBA, solvent_HBD, solvent_FractionCSP3,
    solvent_MolMR, solvent_LabuteASA, solvent_NumRotatableBonds, solvent_RingCount,
    solvent_HeavyAtomCount.

    Args:
        filepath (str): Path to the JSON file.
        same_dir_as_input (bool): If True, the output is created inside the same
        directory as the input JSON file.

    Returns:
        dict: The dict used to generate archive.json file.
    """

    with open(filepath, encoding='utf-8') as f:
        file_dict = json.load(f)

    # Validate input JSON (allow extra keys from full JSON format)
    _ = PolymerizationReactionInput.model_validate(file_dict)

    data_dict_ordered: collections.OrderedDict[str, Any] = collections.OrderedDict()

    reaction_conditions: dict[str, Any] = {}
    if file_dict.get('temperature', None) is not None:
        temperature = file_dict['temperature']
        temperature_unit_original = file_dict.get('temperature_unit')
        if temperature_unit_original is not None:
            temperature = (
                ureg.Quantity(temperature, temperature_unit_original)
                .to('K')
                .magnitude
            )
            # Store original temperature unit
            reaction_conditions['temperature_unit'] = temperature_unit_original
        reaction_conditions['temperature'] = temperature
    if file_dict.get('solvent', None) is not None:
        # solvent is always SMILES (e.g. "CN(C)C=O")
        reaction_conditions['solvent'] = {'smile': file_dict['solvent']}
    # Solvent descriptors as separate subsection
    solvent_descriptors: dict[str, Any] = {}
    solvent_logp = file_dict.get('solvent_logP') or file_dict.get('logP')
    if solvent_logp is not None:
        solvent_descriptors['logP'] = solvent_logp
    # Map solvent_* keys to descriptors (remove 'solvent_' prefix)
    for key in (
        'solvent_TPSA', 'solvent_HBA', 'solvent_HBD', 'solvent_FractionCSP3',
        'solvent_MolMR', 'solvent_LabuteASA', 'solvent_NumRotatableBonds',
        'solvent_RingCount', 'solvent_HeavyAtomCount',
    ):
        if file_dict.get(key) is not None:
            # Remove 'solvent_' prefix
            descriptor_key = key.replace('solvent_', '')
            solvent_descriptors[descriptor_key] = file_dict[key]
    if solvent_descriptors:
        reaction_conditions['solvent_descriptors'] = solvent_descriptors
    # polymerization_method with fallback to legacy key "method"
    polymerization_method = file_dict.get('polymerization_method') or file_dict.get(
        'method'
    )
    if polymerization_method is not None:
        reaction_conditions['polymerization_method'] = polymerization_method
    if file_dict.get('polymerization_type', None) is not None:
        reaction_conditions['polymerization_type'] = file_dict['polymerization_type']
    # calculation_method with fallback to determination_method (they are the same)
    calc_method = file_dict.get('calculation_method') or file_dict.get(
        'determination_method'
    )
    if calc_method is not None:
        reaction_conditions['calculation_method'] = calc_method
    # Reaction constants from r_values and conf_intervals
    r_values = file_dict.get('r_values') or {}
    conf_intervals = file_dict.get('conf_intervals') or {}
    reaction_constants = []
    for i in (1, 2):
        r_key = f'constant_{i}'
        c_key = f'constant_conf_{i}'
        r_val = r_values.get(r_key) if r_values else None
        c_val = conf_intervals.get(c_key) if conf_intervals else None
        if r_val is not None or c_val is not None:
            rc = {}
            if r_val is not None:
                rc['reaction_constant'] = r_val
            if c_val is not None:
                rc['reaction_constant_confi'] = c_val
            if rc:
                reaction_constants.append(rc)
    if reaction_constants:
        reaction_conditions['reaction_constants'] = reaction_constants
    # Embeddings to reaction_conditions
    for key in ('polytype_emb_1', 'polytype_emb_2', 'method_emb_1', 'method_emb_2'):
        if file_dict.get(key) is not None:
            reaction_conditions[key] = file_dict[key]

    monomers: list[dict[str, str]] = []
    iterator = 1
    while True:
        if file_dict.get(f'monomer{iterator}', None) is None:
            break

        monomer_dict: dict[str, str] = {}
        monomer_dict['name'] = file_dict[f'monomer{iterator}']
        smiles = file_dict.get(f'monomer{iterator}_smiles')
        if smiles is not None:
            monomer_dict['smiles'] = smiles
        monomers.append(monomer_dict)
        iterator += 1

    data_dict_ordered['m_def'] = (
        'nomad_polymerization_reactions.schema_packages.polymerization.PolymerizationReaction'
    )
    if file_dict.get('source', None) is not None:
        data_dict_ordered['publication_reference'] = dict(
            DOI_number=file_dict['source']
        )
    if file_dict.get('r-product', None) is not None:
        data_dict_ordered['r_product'] = file_dict['r-product']
    if monomers:
        data_dict_ordered['monomers'] = monomers
    if reaction_conditions:
        data_dict_ordered['reaction_conditions'] = reaction_conditions

    data_dict: dict[str, Any] = dict(data_dict_ordered)
    entry: dict[str, dict[str, Any]] = {'data': data_dict}
    if same_dir_as_input:
        archive_path = filepath.replace('.json', '.archive.json')
    else:
        # If input is from tests/data/jsons/, save to tests/data/archive_jsons/
        if 'tests/data/jsons/' in filepath:
            archive_dir = filepath.replace('tests/data/jsons/', 'tests/data/archive_jsons/')
            archive_dir = os.path.dirname(archive_dir)
            os.makedirs(archive_dir, exist_ok=True)
            archive_filename = os.path.basename(filepath).replace('.json', '.archive.json')
            archive_path = os.path.join(archive_dir, archive_filename)
        else:
            archive_path = filepath.split('/')[-1].replace('.json', '.archive.json')
    with open(archive_path, 'w', encoding='utf-8') as f:
        json.dump(entry, f, indent=4)

    print(f'Polymerization reaction archive created at: {archive_path}')

    return entry


def generate_monomer_archive_from_json(  # noqa: PLR0912, PLR0915
    filepath: str, same_dir_as_input: bool = False
) -> dict:
    """
    Generate an archive.json file for monomers from a JSON file of the following format:
    ```json
    {
        "smiles": "[C-]#[N+]c1ccccc1C",
        "best_conformer_coordinates": [
            [
                2.595315676604095,
                1.804171318905585,
                1.1580280763992141
            ],
            ...
        ],
        "best_conformer_elements": [
            6,
            ...
        ],
        "best_conformer_energy": -23.540149986321136,
        "ip": 13.857459727669687,
        "ip_corrected": 9.011459727669687,
        "ea": 4.107520078269179,
        "homo": -0.40488757161696765,
        "lumo": -0.2615756078541851,
        "charges": {
            "1": -0.15148198241215938,
            ...
        },
        "dipole": [
            -0.9483921486833882,
            -0.6794399286044924,
            -0.42974637129632703
        ],
        "global_electrophilicity": 0.877469468153074,
        "global_nucleophilicity": -9.011459727669687,
        "fukui_electrophilicity": {
            "1": 0.15958638228848104,
            ...
        },
        "fukui_nucleophilicity": {
            "1": 0.1358186791274193,
            ...
        },
        "fukui_radical": {
            "1": 0.14770253070795017,
            ...
        }
    }
    ```

    Args:
        filepath (str): Path to the JSON file.
        same_dir_as_input (bool): If True, the output is created inside the same
        directory as the input JSON file.

    Returns:
        dict: The dict used to generate archive.json file.
    """
    with open(filepath, encoding='utf-8') as f:
        file_dict = json.load(f)

    # Validate input JSON
    _ = MonomerInput(**file_dict)

    data_dict: dict[str, Any] = {}

    data_dict['m_def'] = (
        'nomad_polymerization_reactions.schema_packages.polymerization.Monomer'
    )
    if file_dict.get('name', None) is not None:
        data_dict['name'] = file_dict['name']
    if file_dict.get('smiles', None) is not None:
        data_dict['smiles'] = file_dict['smiles']
    if file_dict.get('description', None) is not None:
        data_dict['description'] = file_dict['description']
    xtb_features: dict[str, Any] = {}
    if file_dict.get('best_conformer_energy', None) is not None:
        xtb_features['energy'] = file_dict['best_conformer_energy']
    if file_dict.get('ip', None) is not None:
        xtb_features['ionization_potential'] = file_dict['ip']
    if file_dict.get('ip_corrected', None) is not None:
        xtb_features['ionization_potential_corrected'] = file_dict['ip_corrected']
    if file_dict.get('ea', None) is not None:
        xtb_features['electron_affinity'] = file_dict['ea']
    if file_dict.get('homo', None) is not None:
        xtb_features['homo_energy'] = file_dict['homo']
    if file_dict.get('lumo', None) is not None:
        xtb_features['lumo_energy'] = file_dict['lumo']
    if file_dict.get('global_electrophilicity', None) is not None:
        xtb_features['global_electrophilicity'] = file_dict['global_electrophilicity']
    if file_dict.get('global_nucleophilicity', None) is not None:
        xtb_features['global_nucleophilicity'] = file_dict['global_nucleophilicity']
    if file_dict.get('dipole', None) is not None:
        xtb_features['dipole_moment'] = file_dict['dipole']

    atomic_features: list[dict[str, Any]] = []
    for positions, element in zip(
        file_dict.get('best_conformer_coordinates', []),
        file_dict.get('best_conformer_elements', []),
    ):
        atomic_features.append(
            {'positions': positions, 'element': chemical_symbols[element]}
        )
    if file_dict.get('charges', None) is not None:
        charges = list(file_dict['charges'].values())
        for i, atomic_feature in enumerate(atomic_features):
            atomic_feature['charge'] = charges[i]
    if file_dict.get('fukui_electrophilicity', None) is not None:
        fukui_electrophilicity = list(file_dict['fukui_electrophilicity'].values())
        for i, atomic_feature in enumerate(atomic_features):
            atomic_feature['fukui_electrophilicity'] = fukui_electrophilicity[i]
    if file_dict.get('fukui_nucleophilicity', None) is not None:
        fukui_nucleophilicity = list(file_dict['fukui_nucleophilicity'].values())
        for i, atomic_feature in enumerate(atomic_features):
            atomic_feature['fukui_nucleophilicity'] = fukui_nucleophilicity[i]
    if file_dict.get('fukui_radical', None) is not None:
        fukui_radical = list(file_dict['fukui_radical'].values())
        for i, atomic_feature in enumerate(atomic_features):
            atomic_feature['fukui_radical'] = fukui_radical[i]
    if atomic_features:
        xtb_features['atomic_features'] = atomic_features
    if xtb_features:
        data_dict['xtb_features'] = xtb_features

    entry: dict[str, dict[str, Any]] = {'data': data_dict}
    if same_dir_as_input:
        archive_path = filepath.replace('.json', '.archive.json')
    else:
        # If input is from tests/data/jsons/, save to tests/data/archive_jsons/
        if 'tests/data/jsons/' in filepath:
            archive_dir = filepath.replace('tests/data/jsons/', 'tests/data/archive_jsons/')
            archive_dir = os.path.dirname(archive_dir)
            os.makedirs(archive_dir, exist_ok=True)
            archive_filename = os.path.basename(filepath).replace('.json', '.archive.json')
            archive_path = os.path.join(archive_dir, archive_filename)
        else:
            archive_path = filepath.split('/')[-1].replace('.json', '.archive.json')

    with open(archive_path, 'w', encoding='utf-8') as f:
        json.dump(entry, f, indent=4)

    print(f'Monomer archive created at: {archive_path}')

    return entry
