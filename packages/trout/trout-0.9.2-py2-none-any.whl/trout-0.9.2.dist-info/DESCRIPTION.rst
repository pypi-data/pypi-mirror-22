Trout
=====

``trout`` is a bioinformatics software package that uses suffix trees to
compute the distances between genomes.

Setup
-----

Build from source
~~~~~~~~~~~~~~~~~

::

    wget https://bitbucket.org/NDBL/trout/get/trout-0.9.tar.gz
    tar -xvzf trout-0.9.tar.gz
    mv NDBL-trout-<commit> trout-0.9
    cd trout-0.9
    make

Requirements
------------

-  ``/usr/bin/make``
-  ``/usr/bin/g++``
-  ``/usr/bin/python``

Usage
-----

``trout-suffix`` builds a suffix tree from a *fastq* and searches that
tree for kmers to generate a binary sketch (*.trout.sketch*)

::

    usage:    trout-suffix <input_fastq> <kmer_markers> <output_sketch>

``trout-matrix`` generates a distance matrix from the binary sketches
(*.trout.sketch*) produced by ``trout-suffix``

::

    usage:    trout-matrix <sketch_dir>

``trout-compare`` computes the difference between two distance matrices

::

    usage:    trout-compare <distance_matrix> <distance_matrix>

``trout-match`` computes the number of matches of the kmer-markers
across binary sketches (*.trout.sketch*)

::

    usage:    trout-match <sketch_dir>

Example Usage
-------------

For an example usage with sample data:

::

    make sample

To remove generated files when finished:

::

    make sample-clean

Contact
-------

| `Notre Dame Bioinformatics
  Lab <http://www.cse.nd.edu/~biocmp/index.html>`__
| Will Markley: `wmarkley@nd.edu <mailto:%20wmarkley@nd.edu>`__


