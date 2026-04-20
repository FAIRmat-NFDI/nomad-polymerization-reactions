from typing import (
    TYPE_CHECKING,
)

import numpy as np
import plotly.graph_objects as go
from ase import Atoms
from ase.data import chemical_symbols, covalent_radii
from ase.data.colors import jmol_colors
from ase.neighborlist import NeighborList, natural_cutoffs
from nomad.datamodel.data import ArchiveSection, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    Activity,
    CompositeSystem,
    PubChemPureSubstanceSection,
    PublicationReference,
)
from nomad.datamodel.metainfo.basesections.v1 import PureSubstance, SectionReference
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import MEnum, Quantity, SchemaPackage, SubSection
from nomad.metainfo.metainfo import Section

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
        type=float, a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity)
    )

    reaction_constant_confi = Quantity(
        type=float, a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity)
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
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )
    solvent = SubSection(section_def=PubChemPureSubstanceSection)
    solvent_descriptors = SubSection(section_def=SolventDescriptors)
    polymerization_method = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    temperature = Quantity(
        type=np.dtype(np.float64),
        unit='K',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    calculation_method = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    reaction_constants = SubSection(section_def=ReactionConstant, repeats=True)
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


class Monomer(PureSubstance, Schema, PlotSection):
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
        a_eln=dict(
            component='RichTextEditQuantity',
            label='detailed monomer description',
            props=dict(height=200),
        ),
    )
    xtb_features = SubSection(
        description='xTB calculated features of the monomer.',
        section_def=XTBFeatures,
    )

    def generate_visualization(self) -> PlotlyFigure | None:
        """
        Generate a 3D visualization of the monomer from its atomic positions.

        Uses ASE for atom data and bond detection (via natural cutoff neighbor
        list). Renders a Plotly 3D scatter with Jmol colors and sizes based on covalent
        radii.
        """

        if not self.xtb_features or not self.xtb_features.atomic_features:
            return None

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
        pos = atoms.get_positions()
        x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]

        # Colors from ASE's Jmol palette, sizes from covalent radii
        # Override white (H) to light grey for visibility
        def atom_color(atomic_number: int) -> str:
            grey_cutoff = 0.95
            r, g, b = jmol_colors[atomic_number]
            if r > grey_cutoff and g > grey_cutoff and b > grey_cutoff:
                return 'rgb(200, 200, 200)'
            return f'rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})'

        colors = [atom_color(a.number) for a in atoms]
        sizes = [max(6, covalent_radii[a.number] * 18) for a in atoms]

        # Atom trace
        atom_trace = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers+text',
            marker=dict(
                size=sizes,
                color=colors,
                line=dict(width=1, color='#333333'),
            ),
            text=elements,
            textposition='top center',
            textfont=dict(size=9),
            hovertext=[
                f'{s} ({xi:.3f}, {yi:.3f}, {zi:.3f})'
                for s, xi, yi, zi in zip(elements, x, y, z)
            ],
            hoverinfo='text',
            name='atoms',
        )

        # Bond detection using ASE neighbor list
        cutoffs = natural_cutoffs(atoms)
        nl = NeighborList(cutoffs, self_interaction=False, bothways=False)
        nl.update(atoms)

        bond_x, bond_y, bond_z = [], [], []
        for i in range(len(atoms)):
            indices, _ = nl.get_neighbors(i)
            for j in indices:
                bond_x.extend([x[i], x[j], None])
                bond_y.extend([y[i], y[j], None])
                bond_z.extend([z[i], z[j], None])

        bond_trace = go.Scatter3d(
            x=bond_x,
            y=bond_y,
            z=bond_z,
            mode='lines',
            line=dict(color='#555555', width=4),
            hoverinfo='none',
            name='bonds',
        )

        fig = go.Figure(data=[bond_trace, atom_trace])
        fig.update_layout(
            scene=dict(
                xaxis_title='x (Å)',
                yaxis_title='y (Å)',
                zaxis_title='z (Å)',
                aspectmode='data',
            ),
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0),
        )

        return PlotlyFigure(
            label='Best conformer visualization generated from xTB features.',
            figure=fig.to_plotly_json(),
        )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if not self.name:
            self.name = 'Monomer'
        # TODO: more descriptive name?
        self.components = []
        self.elemental_composition = []
        pure_substance = None
        if self.smiles:
            pure_substance = PubChemPureSubstanceSection(smile=self.smiles)
            pure_substance.normalize(archive, logger)
        if pure_substance:
            self.pure_substance = pure_substance
        fig = self.generate_visualization()
        self.figures = [fig] if fig else []
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
            'Product of reactivity ratios (r1 × r2), indicating the '
            'copolymerization behavior and monomer reactivity.'
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
                'polymerization.Monomer': smiles
            },
            user_id=archive.metadata.main_author.user_id,
        ).data

        if not search_result:
            logger.warning(f'No monomer found with the SMILES "{smiles}".')
            return None

        if len(search_result) > 1:
            logger.warning(
                f'Multiple monomers found with the SMILES "{smiles}". Using the '
                'first one.'
            )
            # TODO: better handling in case of multiple entries?
            # Limit to the same upload?

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

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if not self.name:
            self.name = 'Polymerization Reaction'
            # TODO: more descriptive name?
        self.normalize_monomers(archive, logger)
        super().normalize(archive, logger)


m_package.__init_metainfo__()
