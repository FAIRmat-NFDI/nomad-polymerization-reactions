import os.path

from nomad.client import normalize_all, parse


def test_polymerization_reaction():
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
    assert entry_archive.data.monomers[0].name == 'Methacrylic acid'

def test_monomer():
    test_file = os.path.join(
        'tests', 'data', 'test_monomer.archive.yaml'
    )
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.pure_substance.smile == 'C=CC#N'
    assert entry_archive.data.pure_substance.pub_chem_cid == 7855
    assert entry_archive.data.name == 'Acrylonitrile'
