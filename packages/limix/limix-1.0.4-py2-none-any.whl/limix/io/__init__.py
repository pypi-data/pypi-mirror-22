r"""
**********
I/O module
**********

- :func:`.read_plink`
- :class:`.h5data_fetcher`
- :func:`.read_csv`
- :func:`.read_gen`

Public interface
^^^^^^^^^^^^^^^^
"""

from . import examples
from ._csv import read_csv
from .gen import read_gen
from .hdf5 import h5data_fetcher
from .plink import read_plink


def genotype_reader(*args, **kwargs):
    from limix_legacy.io import genotype_reader
    return genotype_reader(*args, **kwargs)


def phenotype_reader(*args, **kwargs):
    from limix_legacy.io import phenotype_reader
    return phenotype_reader(*args, **kwargs)


def data(*args, **kwargs):
    from limix_legacy.io import data
    return data(*args, **kwargs)


__all__ = [
    'read_plink', 'h5data_fetcher', 'read_csv', 'read_gen', 'examples',
    'genotype_reader', 'phenotype_reader', 'data'
]
