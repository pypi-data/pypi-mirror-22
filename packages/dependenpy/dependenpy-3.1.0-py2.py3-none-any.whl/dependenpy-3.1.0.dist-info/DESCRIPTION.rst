==========
Dependenpy
==========



Dependenpy allows you to build a dependency matrix for a set of Python packages.
To do this, it reads and searches the source code for import statements.

License
=======

Software licensed under `ISC`_ license.

.. _ISC: https://www.isc.org/downloads/software-support-policy/isc-license/

Installation
============

::

    pip install dependenpy


Usage
=====

Version 3 introduces a command-line tool:

Example:

.. code:: bash

    dependenpy -h

Result:

.. code:: bash

    usage: dependenpy [-d DEPTH] [-f {csv,json,text}] [-g] [-h] [-i INDENT] [-l]
                      [-m] [-o OUTPUT] [-t] [-v]
                      PACKAGES [PACKAGES ...]

    Command line tool for dependenpy Python package.

    positional arguments:
      PACKAGES              The package list. Can be a comma-separated list. Each
                            package must be either a valid path or a package in
                            PYTHONPATH.

    optional arguments:
      -d DEPTH, --depth DEPTH
                            Specify matrix depth (only for -m option). Default:
                            best guess.
      -f {csv,json,text}, --format {csv,json,text}
                            Output format. Default: text.
      -g, --greedy          Explore subdirectories even if they do not contain an
                            __init__.py file. Can make execution slower. Default:
                            false.
      -h, --help            Show this help message and exit.
      -i INDENT, --indent INDENT
                            Specify output indentation (only for -l option). CSV
                            will not be indented. Text will always have new-lines,
                            but JSON can be minified with a negative value.
                            Default: best guess.
      -l, --show-dependencies-list
                            Show the dependencies list. Default: false.
      -m, --show-matrix     Show the matrix. Default: true unless -l or -t.
      -o OUTPUT, --output OUTPUT
                            Output to given file. Default: stdout.
      -t, --show-treemap    Show the treemap (work in progress). Default: false.
      -v, --version         Show the current version of the program and exit.

Example:

.. code:: bash

    dependenpy dependenpy
    dependenpy dependenpy --depth=2

Result:

.. code:: bash

                    Module | Id ||0|1|2|3|4|5|6|7|
     ----------------------+----++-+-+-+-+-+-+-+-+
       dependenpy.__init__ |  0 ||0|0|0|4|0|0|0|2|
       dependenpy.__main__ |  1 ||0|0|1|0|0|0|0|0|
            dependenpy.cli |  2 ||1|0|0|1|0|0|3|0|
            dependenpy.dsm |  3 ||0|0|0|0|2|3|1|0|
         dependenpy.finder |  4 ||0|0|0|0|0|0|0|0|
           dependenpy.node |  5 ||0|0|0|0|0|0|1|2|
        dependenpy.printer |  6 ||0|0|0|0|0|0|0|0|
     dependenpy.structures |  7 ||0|0|0|0|0|0|1|0|

You can also use dependenpy programmatically:

.. code:: python

    from dependenpy import DSM

    # create DSM
    dsm = DSM('django')

    # transform as matrix, dict of deps or treemap
    matrix = dsm.as_matrix(depth=2)
    deps = dsm.as_dict()
    treemap = dsm.as_treemap()  # soon

    # initialize with many packages
    dsm = DSM('django', 'meerkat', 'appsettings', 'dependenpy', 'archan')
    with open('output', 'w') as output:
        dsm.print(matrix=True, depth=1, dependencies=True, output=output)

    # access packages and modules
    meerkat = dsm['meerkat']  # or dsm.get('meerkat')
    finder = dsm['dependenpy.finder']  # or even dsm['dependenpy']['finder']

    # instances of DSM and Package all have print, as_matrix, etc. methods
    meerkat.print_matrix(depth=2)

This module was originally design to work in a Django project.
The Django package `django-meerkat`_ uses it to display the matrices with Highcharts.

.. _django-meerkat: https://github.com/Pawamoy/django-meerkat


Documentation
=============

`On ReadTheDocs`_

.. _`On ReadTheDocs`: http://dependenpy.readthedocs.io/

Development
===========

To run all the tests: ``tox``

=========
Changelog
=========

3.1.0 (2017-06-02)
==================

- Change ``-i, --enforce-init`` option to its contrary ``-g, --greedy``.
- Add ``-i, --indent`` option to specify indentation level.
- Options ``-l``, ``-m`` and ``-t`` are now mutually exclusive.
- Fix matrix build for depth 0.
- Print methods have been improved.
- Update documentation.

3.0.0 (2017-05-23)
==================

This version is a big refactoring. The code is way more object oriented,
cleaner, shorter, simpler, smarter, more user friendly- in short: better.

Additional features:

- command line entry point,
- runtime static imports are now caught (in functions or classes),
  as well as import statements (previously only from import).

2.0.3 (2017-04-20)
==================

- Fix occasional UnicodeEncode when reading UTF-8 file.
- Handle bad characters in files when parsing with ``ast``.

0.1.0 to 2.0.2 (2016-10-06)
===========================

- Development (alpha then beta version).

0.1.0 (2016-10-06)
==================

- Alpha release on PyPI.


