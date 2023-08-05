nCephes
=======

|PyPI-License| |PyPI-Version| |Anaconda-Version| |Anaconda-Downloads
Badge| |Documentation Status|

This package provides a python interface for the
`Cephes <http://www.netlib.org/cephes/>`__ library. It also supports
`Numba <http://numba.pydata.org>`__ and its ``nopython`` mode.

Usage
-----

.. code:: python

    from ncephes import cprob
    print(cprob.incbet(1., 3., 0.3))

prints ``0.657``.

You can also call them inside a numba function

.. code:: python

    from ncephes import cprob
    from numba import jit

    @jit
    def numba_incbet(a, b, x):
        return cprob.incbet(a, b, x)

    print(numba_incbet(1., 3., 0.3))

and with nopython mode and nogil enabled

.. code:: python

    from ncephes import cprob
    from numba import jit

    incbet = cprob.incbet

    @jit(nogil=True, nopython=True)
    def numba_incbet(a, b, x):
        return incbet(a, b, x)

    print(numba_incbet(1., 3., 0.3))

One can also statically link the compiled Cephes libraries ``ncprob``
and ``ncellf``. Please, have a peek at the ``examples/prj_name`` for a
minimalistic example.

Install
-------

The recommended way of installing it is via
`conda <http://conda.pydata.org/docs/index.html>`__

.. code:: bash

    conda install -c conda-forge ncephes

An alternative way would be via pip

.. code:: bash

    pip install ncephes

Running the tests
-----------------

After installation, you can test it

::

    python -c "import ncephes; ncephes.test()"

as long as you have `pytest <http://docs.pytest.org/en/latest/>`__.

Authors
-------

-  **Danilo Horta** - https://github.com/Horta

License
-------

This project is licensed under the MIT License - see the
`LICENSE <LICENSE>`__ file for details

.. |PyPI-License| image:: https://img.shields.io/pypi/l/ncephes.svg?style=flat-square
   :target: https://pypi.python.org/pypi/ncephes/
.. |PyPI-Version| image:: https://img.shields.io/pypi/v/ncephes.svg?style=flat-square
   :target: https://pypi.python.org/pypi/ncephes/
.. |Anaconda-Version| image:: https://anaconda.org/conda-forge/ncephes/badges/version.svg
   :target: https://anaconda.org/conda-forge/ncephes
.. |Anaconda-Downloads Badge| image:: https://anaconda.org/conda-forge/ncephes/badges/downloads.svg
   :target: https://anaconda.org/conda-forge/ncephes
.. |Documentation Status| image:: https://readthedocs.org/projects/ncephes/badge/?style=flat-square&version=latest
   :target: https://ncephes.readthedocs.io/


