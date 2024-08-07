import os.path

from nomad.client import normalize_all, parse


def test_schema():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert (
        entry_archive.data.DOI_number == 'https://doi.org/10.1002/macp.1985.021860810'
    )
