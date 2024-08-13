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
    CompositeSystem,
    PubChemPureSubstanceSection,
    PublicationReference,
    PureSubstanceComponent,
)
from nomad.metainfo import Quantity, SchemaPackage, SubSection

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
    extracted_json_data = Quantity(
        type=str,
        description='Data file containing the extracted data.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity,
        ),
    )

    reaction_conditions = SubSection(section_def=ReactionConditions, repeats=True)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if self.monomers is not None:
            if self.polymer is None:
                self.polymer = CompositeSystem()
            self.polymer.components = self.monomers
        super().normalize(archive, logger)

        import json  # noqa: I001
        from nomad.units import ureg  # noqa: I001

        logger.info(
            'PolymerizationReaction.normalize', parameter=configuration.parameter
        )
        if self.extracted_json_data:
            with archive.m_context.raw_file(self.extracted_json_data) as file:
                file_dict = json.load(file)

            print(file_dict)
            self.DOI_number = file_dict.get('source')
            if 'reactions' in file_dict:
                for reaction in file_dict['reactions']:
                    self.monomers = reaction.get('monomers', [])

                    if 'reaction_conditions' in reaction:
                        for condition in reaction['reaction_conditions']:
                            reaction_condition = ReactionConditions(
                                polymerization_type=condition.get(
                                    'polymerization_type'
                                ),
                                solvent=condition.get('solvent'),
                                method=condition.get('method'),
                                temperature=np.float64(condition.get('temperature'))
                                * ureg(condition['temperature_unit']),
                                determination_method=condition.get(
                                    'determination_method'
                                ),
                            )

                            if (
                                'reaction_constants' in condition
                                and 'reaction_constant_conf' in condition
                            ):
                                constants = condition['reaction_constants']
                                confs = condition['reaction_constant_conf']

                                for const_key, const_value in constants.items():
                                    reaction_constant = ReactionConstant()
                                    reaction_constant.reaction_constant = const_value
                                    reaction_constant.reaction_constant_confi = (
                                        confs.get(f'constant_conf_{const_key[-1]}')
                                    )
                                    reaction_condition.reaction_constants.append(
                                        reaction_constant
                                    )

                            self.reaction_conditions.append(reaction_condition)
        super().normalize(archive, logger)


m_package.__init_metainfo__()
