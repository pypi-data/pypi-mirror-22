Stoichiograph - The Elemental Speller
=====================================

Spell words with elemental symbols from the periodic table ("He", "Cu", etc).

.. figure:: https://cloud.githubusercontent.com/assets/5744114/21043177/7c3efe8c-bdaa-11e6-9c1a-22db4de6bb2f.png
    :alt: A list of four words and their elemental spellings

    Some words and their elemental spellings


Usage
-----

.. code-block::

    usage: stoichiograph [-h] [-b BATCH_FILE] [-c] [--debug] [--list-elements]
                         [--export-graph] [-o OUTPUT_FILE] [-s] [-t] [-v] [-V]
                         [words [words ...]]

    Spell words with elemental symbols from the periodic table.

    positional arguments:
      words                 word(s) for which to find elemental spellings

    optional arguments:
      -h, --help            show this help message and exit
      -b BATCH_FILE, --batch-file BATCH_FILE
                            text file containing one word per line
      -c, --clobber         overwrite output file if it exists
      --debug               print debug log
      --list-elements       print list of elemental symbols and exit
      --export-graph        export graph of first word as dot code
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            path of output json file
      -s, --sort            sort words by length
      -t, --tuples          display spellings as tuples
      -v, --verbose         print a detailed log
      -V, --version         print version info and exit


Graph Export
------------

Stoichiograph can builds a graph to find a word's elemental spellings. Use the
`--export-graph` option to output dot code that can be used to generate an
image of the graph. You will need `graphviz`_ installed.

.. code-block:: bash

    $ stoichiograph.py --export-graph cryptographer | dot -Tpng -o cryptographer.png


.. _Graphviz: http://www.graphviz.org/Home.php


