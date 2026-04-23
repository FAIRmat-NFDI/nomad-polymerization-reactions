def test_importing_app():
    # this will raise an exception if pydantic model validation fails for the app
    from nomad_polymerization_reactions.apps.polymerization import polymerization_app  # noqa: F401, I001
