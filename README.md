# nomad-polymerization-reactions

![nomad-polymerization-reactions logo](logo.png)

A NOMAD plugin providing schemas, search apps, and data transformation
utilities for polymerization data extracted from publications.

## Availability

The plugin is available on the central NOMAD deployment. You can use the
Polymerization Reaction [search app][nomad-prod-polymerization-search] to
access polymerization entries from publically available datasets. These entries
are based on the [`PolymerizationReaction`][nomad-prod-metainfo-browser] schema
made available from this plugin.

## Installation

Install the package in your local environment with pip:

```bash
pip install nomad-polymerization-reactions
```

## Adding this plugin to NOMAD Oasis

The plugin can be added to a [NOMAD Oasis][nomad-oasis] instance in a few
steps, provided that you have access to the repository hosting the Oasis.

Read the [NOMAD plugin documentation][plugin-docs] for all details on how to
deploy the plugin on your NOMAD Oasis instance. If you want to get started with
a new Oasis, read the [installation guide][oasis-install].

## Using the CLI for data transformation

The package provides utility functions for transforming JSON files into NOMAD
entry archives. These archives have `archive.json` ending and are processed by
NOMAD once uploaded. The `m_def` key in the archives helps NOMAD to identify
which data schema to use.

Here's how you can convert a JSON file into an NOMAD entry archive that uses
`nomad_polymerization_reactions.schema_packages.polymerization.Monomer` schema:

```bash
nomad-polymerization archive monomer.json
```

If you want to create an archive that uses the `PolymerizationReaction`
schema, use the `polymerization` mode:

```bash
nomad-polymerization archive polymerization_reaction.json --mode polymerization
```

You can specify multiple filepaths in the same command or even use directory
paths. All the `.json` files in the directory will be transformed into archives:

```bash
nomad-polymerization archive /folder/polymerization/ --mode polymerization
```

By default, the command will create the archives in the same directory where it
runs. If you want to create them in the same directory as the JSON file, use
the flag `--same-dir`:

```bash
nomad-polymerization archive /folder/sub-folder/monomer.json --same-dir
# creates `monomer.archive.json` file in `/folder/sub-folder/`
```

The JSON files used for transformation should have a fixed format.
You can find the data models for JSON files in [models.py][models-py].

### License

Distributed under the terms of the `Apache Software License 2.0` license,
`nomad-polymerization-reactions` is free and open source software.

[nomad-prod-polymerization-search]: https://nomad-lab.eu/prod/v1/gui/search/polymerization
[nomad-prod-metainfo-browser]: https://nomad-lab.eu/prod/v1/gui/analyze/metainfo/nomad_polymerization_reactions/section_definitions@nomad_polymerization_reactions.schema_packages.polymerization.PolymerizationReaction
[copol-reactivity]: https://github.com/lamalab-org/copolymer-reactivity/tree/main
[nomad-oasis]: https://nomad-lab.eu/prod/v1/docs/reference/glossary.html#deployment-nomad-oasis
[plugin-docs]: https://nomad-lab.eu/prod/v1/docs/howto/oasis/configure.html#plugins
[oasis-install]: https://nomad-lab.eu/prod/v1/docs/howto/oasis/install.html#how-to-install-a-nomad-oasis
[models-py]: https://github.com/FAIRmat-NFDI/nomad-polymerization-reactions/blob/main/src/nomad_polymerization_reactions/models.py
