import collections
import json

from ase.data import chemical_symbols
from nomad.units import ureg


def generate_pr_archive_from_json(  # noqa: PLR0912, PLR0915
    filepath: str, same_dir_as_input: bool = False
):
    """
    Generate an archive.json file for polymerization reactions from a JSON file of the
    following format:
    ```json
    {
        "monomer1_s": "C=C",
        "monomer2_s": "C=O",
        "monomer1": "ethylene",
        "monomer2": "carbon monoxide",
        "r_values": {
            "constant_1": 22.0,
            "constant_2": 0.0
        },
        "conf_intervals": {
            "constant_conf_1": null,
            "constant_conf_2": null
        },
        "temperature": 20.0,
        "temperature_unit": "\u00b0C",
        "solvent": null,
        "method": "bulk",
        "r-product": null,
        "source": "https://doi.org/10.1002/pol.1963.110010415"
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

    data_dict_ordered = collections.OrderedDict()

    reaction_conditions = dict()
    if file_dict.get('temperature', None) is not None:
        temperature = file_dict['temperature']
        if file_dict.get('temperature_unit', None) is not None:
            temperature = (
                ureg.Quantity(temperature, file_dict['temperature_unit'])
                .to('K')
                .magnitude
            )
        reaction_conditions['temperature'] = temperature
    if file_dict.get('solvent', None) is not None:
        reaction_conditions['solvent'] = dict(name=file_dict['solvent'])
    if file_dict.get('method', None) is not None:
        reaction_conditions['method'] = file_dict['method']
    if file_dict.get('polymerization_type', None) is not None:
        reaction_conditions['polymerization_type'] = file_dict['polymerization_type']
    if file_dict.get('determination_method', None) is not None:
        reaction_conditions['determination_method'] = file_dict['determination_method']

    monomers = []
    iterator = 1
    while True:
        if file_dict.get(f'monomer{iterator}', None) is None:
            break

        monomer_dict = dict()
        monomer_dict['name'] = file_dict[f'monomer{iterator}']
        if file_dict.get(f'monomer{iterator}_s', None) is not None:
            monomer_dict['smiles'] = file_dict[f'monomer{iterator}_s']
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
    if file_dict.get('logP', None) is not None:
        data_dict_ordered['logP'] = file_dict['logP']
    if monomers:
        data_dict_ordered['monomers'] = monomers
    if reaction_conditions:
        data_dict_ordered['reaction_conditions'] = reaction_conditions

    data_dict = dict(data_dict_ordered)
    entry = dict(data=data_dict)
    if same_dir_as_input:
        archive_path = filepath.replace('.json', '.archive.json')
    else:
        archive_path = filepath.split('/')[-1].replace('.json', '.archive.json')
    with open(archive_path, 'w', encoding='utf-8') as f:
        json.dump(entry, f, indent=4)

    print(f'Polymerization reaction archive created at: {archive_path}')

    return entry


def generate_monomer_archive_from_json(filepath: str, same_dir_as_input: bool = False):  # noqa: PLR0912, PLR0915
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

    data_dict = {}

    data_dict['m_def'] = (
        'nomad_polymerization_reactions.schema_packages.polymerization.Monomer'
    )
    if file_dict.get('name', None) is not None:
        data_dict['name'] = file_dict['name']
    if file_dict.get('smiles', None) is not None:
        data_dict['smiles'] = file_dict['smiles']
    if file_dict.get('description', None) is not None:
        data_dict['description'] = file_dict['description']
    xtb_features = {}
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

    atomic_features = []
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

    entry = dict(data=data_dict)
    if same_dir_as_input:
        archive_path = filepath.replace('.json', '.archive.json')
    else:
        archive_path = filepath.split('/')[-1].replace('.json', '.archive.json')

    with open(archive_path, 'w', encoding='utf-8') as f:
        json.dump(entry, f, indent=4)

    print(f'Monomer archive created at: {archive_path}')

    return entry
