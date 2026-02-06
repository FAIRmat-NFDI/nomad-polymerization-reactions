from pydantic import BaseModel, Field, conlist


class RValuesModel(BaseModel):
    constant_1: float | None = Field(
        None, description='First reactivity constant value.'
    )
    constant_2: float | None = Field(
        None, description='Second reactivity constant value.'
    )


class ConfIntervalsModel(BaseModel):
    constant_conf_1: float | None = Field(
        None, description='Confidence interval for first reactivity constant.'
    )
    constant_conf_2: float | None = Field(
        None, description='Confidence interval for second reactivity constant.'
    )


class PolymerizationReactionInput(BaseModel):
    file: str | None = Field(None, description='Source filename (e.g. paper_0.json).')

    monomer1_smiles: str | None = Field(
        None, description='SMILES string for monomer 1.'
    )
    monomer2_smiles: str | None = Field(
        None, description='SMILES string for monomer 2.'
    )
    monomer1: str | None = Field(None, description='Name of monomer 1.')
    monomer2: str | None = Field(None, description='Name of monomer 2.')
    # TODO: there can be more than 2 monomers in a reaction. How to handle this?
    r_values: RValuesModel | None = Field(
        None, description='Reactivity constants for the reaction.'
    )
    conf_intervals: ConfIntervalsModel | None = Field(
        None, description='Confidence intervals for reactivity constants.'
    )
    temperature: float | None = Field(None, description='Reaction temperature value.')
    temperature_unit: str | None = Field(
        None, description="Unit for reaction temperature (e.g., 'K', '°C')."
    )
    solvent: str | None = Field(None, description='Solvent used in the reaction.')
    polymerization_method: str | None = Field(
        None, description="Polymerization method (e.g., 'bulk', 'solution')."
    )
    method: str | None = Field(
        None,
        description='Deprecated: fallback for polymerization_method if not provided.',
    )
    r_product: float | None = Field(
        None, alias='r-product', description='Product reactivity ratio.'
    )
    source: str | None = Field(None, description='Source or DOI for the reaction data.')
    calculation_method: str | None = Field(
        None,
        description='Method used to determine reactivity constants (e.g. Kelen-Tudos).',
    )
    polymerization_type: str | None = Field(
        None, description="Type of polymerization (e.g., 'free radical')."
    )
    determination_method: str | None = Field(
        None,
        description=(
            'Method used to determine reactivity constants '
            '(fallback for calculation_method if not provided).'
        ),
    )
    logP: float | None = Field(
        None, description='LogP value (fallback for solvent_logP if not provided).'
    )
    polytype_emb_1: float | None = Field(
        None, description='Polymerization type embedding dimension 1.'
    )
    polytype_emb_2: float | None = Field(
        None, description='Polymerization type embedding dimension 2.'
    )
    method_emb_1: float | None = Field(
        None, description='Method embedding dimension 1.'
    )
    method_emb_2: float | None = Field(
        None, description='Method embedding dimension 2.'
    )
    solvent_logP: float | None = Field(None, description='Solvent logP descriptor.')
    solvent_TPSA: float | None = Field(None, description='Solvent TPSA descriptor.')
    solvent_HBA: float | None = Field(None, description='Solvent HBA descriptor.')
    solvent_HBD: float | None = Field(None, description='Solvent HBD descriptor.')
    solvent_FractionCSP3: float | None = Field(
        None, description='Solvent FractionCSP3 descriptor.'
    )
    solvent_MolMR: float | None = Field(None, description='Solvent MolMR descriptor.')
    solvent_LabuteASA: float | None = Field(
        None, description='Solvent LabuteASA descriptor.'
    )
    solvent_NumRotatableBonds: float | None = Field(
        None, description='Solvent NumRotatableBonds descriptor.'
    )
    solvent_RingCount: float | None = Field(
        None, description='Solvent RingCount descriptor.'
    )
    solvent_HeavyAtomCount: float | None = Field(
        None, description='Solvent HeavyAtomCount descriptor.'
    )


class MonomerInput(BaseModel):
    name: str = Field(..., description='Name of the monomer.')
    smiles: str = Field(..., description='SMILES string for the monomer.')
    description: str | None = Field(None, description='Description of the monomer.')
    best_conformer_coordinates: (
        list[conlist(float, min_length=3, max_length=3)] | None
    ) = Field(
        None,
        description='3D coordinates of each atom of the best conformer.',
    )
    # TODO: how to limit the length of inner list to 3?
    best_conformer_elements: list[int] | None = Field(
        None, description='Atomic numbers of each atom in the best conformer.'
    )
    best_conformer_energy: float | None = Field(
        None, description='Energy of the best conformer.'
    )
    ip: float | None = Field(None, description='Ionization potential.')
    ip_corrected: float | None = Field(
        None, description='Corrected ionization potential.'
    )
    ea: float | None = Field(None, description='Electron affinity.')
    homo: float | None = Field(
        None, description='Highest occupied molecular orbital energy.'
    )
    lumo: float | None = Field(
        None, description='Lowest unoccupied molecular orbital energy.'
    )
    charges: dict[str, float] | None = Field(None, description='Atomic charges.')
    dipole: list[float] | None = Field(None, description='Dipole moment vector.')
    global_electrophilicity: float | None = Field(
        None, description='Global electrophilicity index.'
    )
    global_nucleophilicity: float | None = Field(
        None, description='Global nucleophilicity index.'
    )
    fukui_electrophilicity: dict[str, float] | None = Field(
        None,
        description='Fukui electrophilicity values per atom. Dict key is atom index, '
        'value is Fukui electrophilicity.',
    )
    fukui_nucleophilicity: dict[str, float] | None = Field(
        None,
        description='Fukui nucleophilicity values per atom. Dict key is atom index, '
        'value is Fukui nucleophilicity.',
    )
    fukui_radical: dict[str, float] | None = Field(
        None,
        description='Fukui radical values per atom. Dict key is atom index, value is '
        'Fukui radical.',
    )
