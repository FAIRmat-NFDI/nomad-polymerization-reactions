from typing import (
    TYPE_CHECKING,
)
from urllib.parse import quote

import numpy as np
from ase import Atoms
from ase.data import chemical_symbols
from nomad.datamodel.data import ArchiveSection, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    Activity,
    CompositeSystem,
    PubChemPureSubstanceSection,
    PublicationReference,
)
from nomad.datamodel.metainfo.basesections.v1 import PureSubstance, SectionReference
from nomad.datamodel.results import System
from nomad.metainfo import MEnum, Quantity, SchemaPackage, SubSection
from nomad.metainfo.metainfo import Section
from nomad.normalizing.common import nomad_atoms_from_ase_atoms
from nomad.normalizing.topology import add_system, add_system_info

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

m_package = SchemaPackage()


class ReactionConstant(ArchiveSection):
    reaction_constant = Quantity(
        type=float,
        description=(
            'Reaction constant (e.g. reactivity ratio) for the polymerization '
            'reaction, indicating the relative reactivity of the monomers.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    reaction_constant_confi = Quantity(
        type=float,
        description=(
            'Confidence interval or standard error associated with the reaction '
            'constant, providing a measure of uncertainty in its estimation.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )


class SolventDescriptors(ArchiveSection):
    """Molecular descriptors for the solvent."""

    log_P = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Partition coefficient (logP), a measure of lipophilicity '
            "representing the ratio of a compound's solubility in octanol "
            'versus water.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    TPSA = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Topological Polar Surface Area (TPSA), the sum of surface areas '
            'of polar atoms in the molecule, used to predict drug transport '
            'properties.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    HBA = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Number of Hydrogen Bond Acceptors (HBA), atoms that can accept '
            'hydrogen bonds (typically N, O, F).'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    HBD = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Number of Hydrogen Bond Donors (HBD), atoms that can donate '
            'hydrogen bonds (typically N-H, O-H groups).'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    fraction_CSP3 = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Fraction of sp3 hybridized carbon atoms relative to total carbon '
            'atoms, indicating molecular saturation.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    mol_MR = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Molar Refractivity (MolMR), a measure of the volume occupied by '
            'a molecule, calculated from the refractive index.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    labute_ASA = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Labute Approximate Surface Area (ASA), an approximation of the '
            'molecular surface area using a simplified method.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    num_rotatable_bonds = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Number of rotatable bonds, single bonds that can rotate freely '
            '(excluding terminal bonds and bonds in rings).'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    ring_count = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Number of rings in the molecule, counting all independent ring systems.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    heavy_atom_count = Quantity(
        type=np.dtype(np.float64),
        description='Number of heavy (non-hydrogen) atoms in the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )


class ReactionConditions(ArchiveSection):
    polymerization_type = Quantity(
        type=str,
        description=(
            'Type of polymerization reaction, e.g. "free radical", "anionic", '
            '"cationic", "ring-opening", "condensation", etc.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )
    polymerization_method = Quantity(
        type=str,
        description=(
            'Method of polymerization reaction, e.g. "bulk", "solution", etc.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )
    temperature = Quantity(
        type=np.dtype(np.float64),
        description='Temperature at which the polymerization reaction was conducted.',
        unit='K',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    calculation_method = Quantity(
        type=str,
        description=(
            'Method used to calculate the reaction constants, e.g. "nonlinear least-'
            'squares", "Mayo-Lewis method", "Fineman-Ross", etc.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )
    # Embeddings
    polytype_emb_1 = Quantity(
        type=np.dtype(np.float64),
        description='Polymerization type embedding dimension 1.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    polytype_emb_2 = Quantity(
        type=np.dtype(np.float64),
        description='Polymerization type embedding dimension 2.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    method_emb_1 = Quantity(
        type=np.dtype(np.float64),
        description='Method embedding dimension 1.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    method_emb_2 = Quantity(
        type=np.dtype(np.float64),
        description='Method embedding dimension 2.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    reaction_constants = SubSection(section_def=ReactionConstant, repeats=True)
    solvent = SubSection(section_def=PubChemPureSubstanceSection)
    solvent_descriptors = SubSection(section_def=SolventDescriptors)


class AtomicFeatures(ArchiveSection):
    element = Quantity(
        type=MEnum(chemical_symbols[1:]),
        description="""
        The symbol of the element, e.g. 'Pb'.
        """,
        a_eln=dict(component='AutocompleteEditQuantity'),
    )
    positions = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        unit='angstrom',
        description='Atomic positions.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    charge = Quantity(
        type=np.dtype(np.float64),
        unit='eV',
        description='Atomic charge.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    fukui_electrophilicity = Quantity(
        type=np.dtype(np.float64),
        description='Fukui electrophilicity index of the atom.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    fukui_nucleophilicity = Quantity(
        type=np.dtype(np.float64),
        description='Fukui nucleophilicity index of the atom.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    fukui_radical = Quantity(
        type=np.dtype(np.float64),
        description='Fukui radical index of the atom.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )


class XTBFeatures(ArchiveSection):
    m_def = Section(
        description='xTB calculated features of the best conformer of the molecule.',
    )
    energy = Quantity(
        type=np.dtype(np.float64),
        unit='eV',
        description='Energy of the best conformer of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    ionization_potential = Quantity(
        type=np.dtype(np.float64),
        unit='eV',
        description='Ionization potential of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    ionization_potential_corrected = Quantity(
        type=np.dtype(np.float64),
        unit='eV',
        description='Corrected ionization potential based on ???.',
        # TODO: based on what?
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    electron_affinity = Quantity(
        type=np.dtype(np.float64),
        unit='eV',
        description='Electron affinity of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    homo_energy = Quantity(
        type=np.dtype(np.float64),
        unit='eV',
        description='HOMO energy of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    lumo_energy = Quantity(
        type=np.dtype(np.float64),
        unit='eV',
        description='LUMO energy of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    global_electrophilicity = Quantity(
        type=np.dtype(np.float64),
        description='Global electrophilicity index of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    global_nucleophilicity = Quantity(
        type=np.dtype(np.float64),
        description='Global nucleophilicity index of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    dipole_moment = Quantity(
        type=np.dtype(np.float64),
        shape=[3],
        unit='debye',
        description='Dipole moment of the molecule.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    atomic_features = SubSection(
        description='Atomic features of the best conformer of the molecule.',
        section_def=AtomicFeatures,
        repeats=True,
    )


class Monomer(PureSubstance, Schema):
    """
    Schema for monomer data in polymerization reactions.
    """

    smiles = Quantity(
        type=str,
        description='SMILES representation of the monomer.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        description="""
        A field for adding additional information about the monomer that is not
        captured by the other quantities and subsections.
        """,
        a_eln=ELNAnnotation(
            component='RichTextEditQuantity',
            label='detailed monomer description',
            props=dict(height=200),
        ),
    )
    xtb_features = SubSection(
        description='xTB calculated features of the monomer.',
        section_def=XTBFeatures,
    )

    def populate_topology(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        Populates the `archive.results.material` section with elements and topology
        using the atomic positions from xTB features.
        """
        if not self.xtb_features or not self.xtb_features.atomic_features:
            return

        elements = []
        positions = []
        for atom in self.xtb_features.atomic_features:
            if atom.element is None or atom.positions is None:
                continue
            elements.append(atom.element)
            positions.append(atom.positions.to('angstrom').magnitude)

        if not positions:
            return None

        atoms = Atoms(symbols=elements, positions=positions)

        topology = {}
        system = System(
            atoms=nomad_atoms_from_ase_atoms(atoms),
            label=atoms.get_chemical_formula(),
            description='Structure based on xTB features of the best conformer of the '
            'molecule.',
            structural_type='monomer',
            dimensionality='3D',
        )
        add_system_info(system, topology)
        add_system(system, topology)

        archive.results.material.elements = list(elements)
        archive.results.material.topology = list(topology.values())

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        Populates the `pure_substance` section with data from PubChem based on the
        `smiles` quantity.

        Resets the `archive.results.material` section based on `pure_substance` and
        `xtb_features`. Populating `archive.results.material.topology` creates a
        visualization of the monomer in the material card.
        """

        # reset `archive.results.material` section to be repopulated from
        # `PureSubstance` normalization
        if archive.results and archive.results.material:
            archive.results.material = None
        archive.m_setdefault('results.material')

        self.elemental_composition = []
        if self.smiles:
            # Use URL-encoded SMILES to handle special characters properly when
            # fetching from PubChem. Can be removed once `PubChemPureSubstanceSection`
            # implements URL encoding.
            pure_substance = PubChemPureSubstanceSection(
                smile=quote(self.smiles, safe='')
            )
            pure_substance.normalize(archive, logger)
            pure_substance.smile = self.smiles

            self.pure_substance = pure_substance
            if self.pure_substance.name:
                archive.results.material.material_name = self.pure_substance.name
                if not self.name:
                    self.name = self.pure_substance.name

        self.populate_topology(archive, logger)

        super().normalize(archive, logger)


class MonomerReference(SectionReference):
    """
    A reference to a Monomer entry section.
    """

    reference = Quantity(
        type=Monomer,
        description='A reference to a Monomer entry section.',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
            label='monomer reference',
        ),
    )
    smiles = Quantity(
        type=str,
        description='SMILES representation of the referenced monomer.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )


class PolymerizationReaction(Activity, Schema):
    """
    Schema for polymerization reaction data.
    """

    monomers = SubSection(
        description='Reference to the monomers used in the polymerization reaction.',
        section_def=MonomerReference,
        repeats=True,
    )
    polymer = SubSection(
        description='Polymer formed in the polymerization reaction.',
        section_def=CompositeSystem,
    )
    publication_reference = SubSection(
        description='Reference to the publication containing the data.',
        section_def=PublicationReference,
    )
    reaction_conditions = SubSection(section_def=ReactionConditions)
    r_product = Quantity(
        type=np.dtype(np.float64),
        description=(
            'Product of reactivity ratios (r1 × r2), indicating the copolymerization '
            'behavior and monomer reactivity. If two reaction constants are provided, '
            'this field is automatically calculated as their product.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    def get_monomer_reference(
        self, smiles: str, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> str | None:
        """
        Looks for an existing monomer entry with the given SMILES and returns its
        proxy value.
        If found, it returns a reference to the entry.
        If no entry is found, logs a warning and returns None.
        If multiple entries are found, logs a warning and returns the first one.
        """
        from nomad.datamodel.context import ClientContext

        if isinstance(archive.m_context, ClientContext):
            return None

        from nomad.search import search

        search_result = search(
            owner='visible',
            query={
                'data.smiles#nomad_polymerization_reactions.schema_packages.'
                'polymerization.Monomer': smiles,
                'upload_id': archive.metadata.upload_id,  # limit search to same upload
            },
            user_id=archive.metadata.main_author.user_id,
        ).data

        if not search_result:
            logger.info(
                f'No monomer entry with the SMILES "{smiles}" found in current upload. '
                'Will search in published entries.'
            )
            search_result = search(
                owner='public',
                query={
                    'data.smiles#nomad_polymerization_reactions.schema_packages.'
                    'polymerization.Monomer': smiles,
                },
                user_id=archive.metadata.main_author.user_id,
            ).data

        if not search_result:
            logger.info(
                f'No monomer entry with the SMILES "{smiles}" found in published '
                'entries.'
            )
            return None

        if len(search_result) > 1:
            logger.warning(
                f'Multiple monomers found with the SMILES "{smiles}". Using the '
                f'first one with entry_id "{search_result[0]["entry_id"]}".'
            )

        upload_id = search_result[0]['upload_id']
        entry_id = search_result[0]['entry_id']
        m_proxy_value = f'../uploads/{upload_id}/archive/{entry_id}#/data'

        return m_proxy_value

    def create_monomer_entry(
        self,
        archive_name: str,
        monomer: Monomer,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
    ) -> str | None:
        """
        Create a new monomer entry in the current Upload and return its proxy value.
        """
        from nomad.datamodel.context import ServerContext
        from nomad.utils import hash as m_hash

        if not isinstance(archive.m_context, ServerContext):
            logger.warning(
                f'Cannot create monomer entries in "{type(archive.m_context)}" '
                'context. Returning None.'
            )
            return None

        # TODO: unique name for the monomer entry archive

        with archive.m_context.update_entry(
            archive_name, write=True, process=True
        ) as entry:
            entry['data'] = monomer.m_to_dict(with_root_def=True)

        entry_id = m_hash(archive.metadata.upload_id, archive_name)
        m_proxy_value = (
            f'../uploads/{archive.metadata.upload_id}/archive/{entry_id}#/data'
        )
        return m_proxy_value

    def normalize_monomers(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        """
        For each monomer in the reaction, check if it exists in the database.
        If it exists, create a reference to it.
        If it does not exist, create a new monomer entry and create a reference to it.
        """
        for monomer in self.monomers:
            monomer: MonomerReference
            if not monomer.smiles:
                logger.warning('Monomer data does not contain SMILES. Skipping.')
                continue

            monomer_m_proxy = self.get_monomer_reference(
                monomer.smiles, archive, logger
            )
            if monomer_m_proxy is None:
                logger.info(
                    f'Creating new monomer entry for SMILES "{monomer.smiles}".'
                )
                new_monomer = Monomer(name=monomer.name, smiles=monomer.smiles)
                archive_name = (
                    'monomer_'
                    + (
                        new_monomer.name.replace(' ', '_').lower()
                        if new_monomer.name
                        else new_monomer.smiles
                    )
                    + '.archive.json'
                )
                monomer_m_proxy = self.create_monomer_entry(
                    archive_name,
                    new_monomer,
                    archive,
                    logger,
                )
            if monomer_m_proxy is not None:
                monomer.reference = monomer_m_proxy
                monomer.normalize(archive, logger)

    def set_copolymerization_rproduct(self) -> None:
        """
        If the reaction conditions contain two reaction constants, calculate the
        product of reactivity ratios (r_product) as their product.
        """
        if self.reaction_conditions and self.reaction_conditions.reaction_constants:
            constants = [
                rc.reaction_constant
                for rc in self.reaction_conditions.reaction_constants
                if rc.reaction_constant is not None
            ]
            num_constants_for_product = 2  # r1 and r2 for copolymerization
            if len(constants) == num_constants_for_product:
                self.r_product = constants[0] * constants[1]

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if not self.name:
            self.name = 'Polymerization Reaction'
        self.normalize_monomers(archive, logger)

        self.set_copolymerization_rproduct()

        super().normalize(archive, logger)


m_package.__init_metainfo__()
