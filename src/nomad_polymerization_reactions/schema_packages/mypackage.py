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

from nomad.config import config
from nomad.datamodel.data import Schema, ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import Quantity, SchemaPackage, SubSection, MEnum
from nomad.datamodel.metainfo.basesections import PublicationReference

configuration = config.get_plugin_entry_point(
    'nomad_polymerization_reactions.schema_packages:mypackage'
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
        type=MEnum(
            'free radical',
            'Cationic',
            'Coordination',
            'Ring-opening',
            'Step-growth',
            'Chain-growth',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    solvent = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    method = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    temperature = Quantity(
        type=float,
        unit='K',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    determination_method = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    reaction_constants = SubSection(section_def=ReactionConstant, repeats=True)


class PolymerizationReaction(PublicationReference, Schema):
    monomers = Quantity(
        type=str,
        shape=['*'],
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    extracted_json_data = Quantity(
        type=str,
        description='Data file containing the extracted data.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity,
        ),
    )

    reaction_conditions = SubSection(section_def=ReactionConditions, repeats=True)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        logger.info(
            'PolymerizationReaction.normalize', parameter=configuration.parameter
        )
        # if self.extracted_json_data:
        #     with open(self.extracted_json_data, 'r') as f:
        #         extracted_json_data = f.read()

        #     self.DOI_number = extracted_json_data.get('source')


m_package.__init_metainfo__()
