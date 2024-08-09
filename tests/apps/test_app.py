def test_importing_app():
    # this will raise an exception if pydantic model validation fails for th app
    from nomad_polymerization_reactions.apps import polymerization_reaction_app  # noqa: F401, I001
