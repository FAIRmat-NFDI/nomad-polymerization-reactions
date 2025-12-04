import json
import os
import re
from typing import (
    TYPE_CHECKING,
)

import numpy as np
from ase.data import chemical_symbols
from nomad.config import config
from nomad.datamodel.data import ArchiveSection, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    Activity,
    CompositeSystem,
    PubChemPureSubstanceSection,
    PublicationReference,
)
from nomad.datamodel.metainfo.basesections.v1 import PureSubstance, SectionReference
from nomad.metainfo import MEnum, Quantity, SchemaPackage, SubSection
from nomad.metainfo.metainfo import Section

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )
configuration = config.get_plugin_entry_point(
    'nomad_polymerization_reactions.schema_packages:polymerization'
)

m_package = SchemaPackage()


class ReactionConstant(ArchiveSection):
    reaction_constant = Quantity(
        type=float, a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity)
    )

    reaction_constant_confi = Quantity(
        type=float, a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity)
    )


class ReactionConditions(ArchiveSection):
    polymerization_type = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )
    solvent = SubSection(section_def=PubChemPureSubstanceSection)
    method = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    temperature = Quantity(
        type=np.dtype(np.float64),
        unit='K',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    determination_method = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    reaction_constants = SubSection(section_def=ReactionConstant, repeats=True)


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

    def generate_visualization(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        """
        Generate visualization for the monomer based on its calculated atomic features
        of the best conformer.
        """
        # TODO: implement visualization generation
        pass

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        self.components = []
        self.elemental_composition = []
        pure_substance = None
        if self.smiles:
            pure_substance = PubChemPureSubstanceSection(smile=self.smiles)
            pure_substance.normalize(archive, logger)
        if pure_substance:
            self.pure_substance = pure_substance
        self.generate_visualization(archive, logger)
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
                'search_quantities': {
                    'id': (
                        'data.smiles#nomad_polymerization_reactions.schema_packages'
                        '.polymerization.Monomer'
                    ),
                    'str_value': f'{smiles}',
                }
            },
            user_id=archive.metadata.main_author.user_id,
        ).data

        if not search_result:
            logger.warning(f'No monomer found with the SMILES "{smiles}".')
            return None

        if len(search_result) > 1:
            logger.warning(
                f'Multiple monomers found with the SMILES "{smiles}". Using the first '
                'one.'
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
                new_monomer = Monomer()
                new_monomer.name = monomer.name
                new_monomer.smiles = monomer.smiles
                monomer_m_proxy = self.create_monomer_entry(
                    f'{monomer.smiles}.archive.json',
                    # TODO: use monomer name for archive name?
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
