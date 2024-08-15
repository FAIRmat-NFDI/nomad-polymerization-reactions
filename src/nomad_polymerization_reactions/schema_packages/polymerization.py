from typing import (
    TYPE_CHECKING,
)

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
    BaseSection,
    CompositeSystem,
    PubChemPureSubstanceSection,
    PublicationReference,
    PureSubstanceComponent,
    SectionReference,
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


class Monomer(PureSubstanceComponent):
    # TODO: use Topology class to visualize the smiles
    smiles = Quantity(
        type=str,
        description='SMILES representation of the monomer.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    pure_substance = SubSection(
        section_def=PubChemPureSubstanceSection,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if self.substance_name and self.pure_substance is None:
            self.pure_substance = PubChemPureSubstanceSection(name=self.substance_name)
            self.pure_substance.normalize(archive, logger)
        if not self.smiles:
            self.smiles = self.pure_substance.smile
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
        super().normalize(archive, logger)


class PolymerizationReactionReference(SectionReference):
    reference = SubSection(
        section_def=PolymerizationReaction,
        description='Reference to the polymerization reaction.',
    )


class AddPolymerizationReactions(BaseSection, Schema):
    """
    A section to add polymerization reaction entries in the current upload.
    Each entry is also referenced in this section.
    """

    zip_file = Quantity(
        type=str,
        description="""
        Zip file containing data files in JSON format. Each file contains data for
        one polymerization reaction.
        """,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity,
        ),
    )
    polymerization_reactions = SubSection(
        section_def=PolymerizationReactionReference,
        repeats=True,
        description='References to polymerization reaction entries.',
    )
    reprocess = Quantity(
        type=bool,
        description='Reprocess the zip file to generate entries.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
        default=True,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        logger.info(
            'AddPolymerizationReactions.normalize', parameter=configuration.parameter
        )
        super().normalize(archive, logger)
        if self.zip_file and self.reprocess:
            ## create entry archives with overwriting
            ## use generate archive from json
            ## add the entry to the polymerization_reactions reference list
            self.reprocess = False


m_package.__init_metainfo__()
