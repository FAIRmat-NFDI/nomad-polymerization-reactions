from nomad.config.models.plugins import AppEntryPoint

from nomad_polymerization_reactions.apps.polymerization import polymerization_app

polymerization = AppEntryPoint(
    name='Polymerization Reactions',
    description='Search app for polymerization reactions entries.',
    app=polymerization_app,
)
