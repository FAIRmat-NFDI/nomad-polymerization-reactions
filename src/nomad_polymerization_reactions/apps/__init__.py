from nomad.config.models.plugins import AppEntryPoint

from nomad_polymerization_reactions.apps.polymerization_reaction_app import (
    polymerization_reaction_app,
)

myapp = AppEntryPoint(
    name='Polymerization Reactions',
    description='This app allows you to search **polymerization reactions** within NOMAD. The filter menu on the left and the shown default columns are specifically designed for polymerization reaction exploration. The dashboard directly shows useful interactive statistics about the data.',  # noqa: E501
    app=polymerization_reaction_app,
)
