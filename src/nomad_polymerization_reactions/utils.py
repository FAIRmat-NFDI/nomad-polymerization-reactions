import collections
import json
from typing import TYPE_CHECKING

import yaml
from nomad.units import ureg

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger


def generate_archive_from_json(
    filepath: str, same_dir_as_input: bool = False, logger: 'BoundLogger' = None
):  # noqa: PLR0912
    """
    Generate an archive.yaml file from a JSON file coming from the LLM output.
    Function expects a JSON of the following format:
    ```json
    {
        "file": "paper_0.json",
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
        logger (BoundLogger): A structlog logger.

    Returns:
        dict: The dict used to generate archive.yaml file.
    """

    class OrderedDumper(yaml.Dumper):
        def represent_dict(self, data):
            return self.represent_mapping('tag:yaml.org,2002:map', data.items())

    OrderedDumper.add_representer(collections.OrderedDict, OrderedDumper.represent_dict)

    with open(filepath) as f:
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
        monomer_dict['substance_name'] = file_dict[f'monomer{iterator}']
        if file_dict.get(f'monomer{iterator}_s', None) is not None:
            monomer_dict['smiles'] = file_dict[f'monomer{iterator}_s']
        monomers.append(monomer_dict)
        iterator += 1

    data_dict_ordered['m_def'] = (
        'nomad_polymerization_reactions.schema_packages.polymerization.PolymerizationReaction'
    )
    if file_dict.get('file', None) is not None:
        data_dict_ordered['data_file_name'] = file_dict.get('file', None)
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
        archive_path = filepath.replace('.json', '.archive.yaml')
    else:
        archive_path = filepath.split('/')[-1].replace('.json', '.archive.yaml')
    with open(archive_path, 'w') as f:
        yaml.dump(entry, f, Dumper=OrderedDumper, default_flow_style=False)

    return entry
