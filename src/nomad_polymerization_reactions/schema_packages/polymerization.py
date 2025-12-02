from typing import (
    TYPE_CHECKING,
)
from nomad.datamodel.metainfo.basesections.v1 import PureSubstance

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

import numpy as np
from nomad.config import config
from nomad.datamodel.data import ArchiveSection, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    Activity,
    CompositeSystem,
    PubChemPureSubstanceSection,
    PublicationReference,
)
from nomad.metainfo import Quantity, SchemaPackage, SubSection

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

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        self.components = []
        self.elemental_composition = []
        pure_substance = None
        if self.smiles:
            pure_substance = PubChemPureSubstanceSection(smile=self.smiles)
            pure_substance.normalize(archive, logger)
        if pure_substance:
            self.pure_substance = pure_substance
        super().normalize(archive, logger)


class PolymerizationReaction(Activity, Schema):
    monomers = SubSection(
        description='Monomers used in the polymerization reaction.',
        section_def=Monomer,
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
    data_file_name = Quantity(
        type=str,
        description='Data file containing the extracted data.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    reaction_conditions = SubSection(section_def=ReactionConditions)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        logger.info(
            'PolymerizationReaction.normalize', parameter=configuration.parameter
        )
        if self.monomers is not None:
            if self.polymer is None:
                self.polymer = CompositeSystem()
            self.polymer.components = self.monomers
            self.polymer.elemental_composition = []
            self.polymer.normalize(archive, logger)
        super().normalize(archive, logger)


m_package.__init_metainfo__()
