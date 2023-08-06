.. highlight:: shell

============
Installation
============

Dependencies
------------

PyIM requires Python 3.4 and has been tested on macOS and Linux.

The following external dependencies are also required for full functionality:

- Bowtie2
- Cutadapt
- CIMPL (R package, via rpy2)

These external tools should be available in ``$PATH``. CIMPL, which is an R
package, should be loadable in the default R installation.

Using pip
---------

From sources
~~~~~~~~~~~~

The sources for PyIM can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/jrderuiter/pyim

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/jrderuiter/pyim/tarball/develop

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/jrderuiter/pyim
.. _tarball: https://github.com/jrderuiter/pyim/tarball/master

Using bioconda
--------------

Coming soon!
