import h5py
import dask.array as da
import dask.dataframe as dd
import pandas as pd

from numpy.testing import assert_allclose, assert_equal


class h5data_fetcher(object):
    r"""
    Fetch datasets from HDF5 files.

    Parameters
    ----------
    filename : str
        Filename to an HDF5 file.

    Examples
    --------
    .. doctest::

        >>> from limix.io import h5data_fetcher
        >>> from limix.io.examples import hdf5_file_example
        >>> with h5data_fetcher(hdf5_file_example()) as df:
        ...     X = df.fetch('/group/dataset')
        ...     print('%.4f' % X[0, 0].compute())
        -0.0453
    """

    def __init__(self, filename):
        self._filename = filename

    def __enter__(self):
        self._f = h5py.File(self._filename, 'r')
        return self

    def fetch(self, data_path):
        r"""
        Fetch a HDF5 dataset.

        Parameters
        ----------
        data_path : str
            Path to a dataset.

        Returns
        -------
        X : dask array
        """
        data = self._f[data_path]
        if data.chunks is None:
            chunks = data.shape
        else:
            chunks = data.chunks
        return da.from_array(data, chunks=chunks)

    def __exit__(self, *exc):
        self._f.close()
