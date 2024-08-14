from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class MySchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_polymerization_reactions.schema_packages.polymerization import (
            m_package,
        )

        return m_package


polymerization = MySchemaPackageEntryPoint(
    name='Polymerization',
    description='Schema package defining FAIR datamodels for polymerization reactions.',
)
