import os.path

from nomad.client import normalize_all, parse


def test_schema():
    test_file = os.path.join(
        'tests', 'data', 'test_polymerization_reaction.archive.yaml'
    )
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert (
        entry_archive.data.publication_reference.DOI_number
        == 'https://doi.org/10.1002/macp.1985.021860810'
    )
    assert (
        entry_archive.data.publication_reference.publication_title
        == 'Synthesis and characterization of a rubber incorporated polyamideimide'
    )
    assert entry_archive.data.monomers[0].pure_substance.name == 'Methacrylic acid'
