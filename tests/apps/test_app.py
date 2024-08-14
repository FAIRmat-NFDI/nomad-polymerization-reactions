def test_importing_app():
    # this will raise an exception if pydantic model validation fails for the app
    from nomad_polymerization_reactions.apps.polymerization import app  # noqa: F401, I001
