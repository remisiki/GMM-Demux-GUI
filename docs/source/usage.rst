Usage
=====

The source code of GMM-Demux is supplied in the ``GMM_Demux`` folder.

An example cell hashing dataset is also provided, located in the ``example_input/outs/filtered_feature_bc_matrix`` folder.

An example set of hand-curated putative cell types of the above dataset are provided in the ``example_cell_types`` folder. Cell types are annotated through manual gating using surface marker expression data.

An example csv format of the above cell hashing dataset is provided as the ``example_hto.csv`` file.

Command Line Tools
------------------

.. function:: GMM-demux [-h] [-k SKIP] [-x EXTRACT] [-o OUTPUT] [-f FULL] [-c] [-t THRESHOLD] [-s SIMPLIFIED] [-u SUMMARY] [-r REPORT] [-e EXAMINE] [-a AMBIGUOUS] [input_path ...] [hto_array ...]

	:arg str input_path: The input path of mtx files from cellRanger pipeline.
	:arg str hto_array: Names of the HTO tags, separated by ``,``.
	:arg -h: Show help information.
	:type -h: optional
	:arg -k: Load a full classification report and skip the mtx folder. Requires a path argument to the full report folder. When specified, the user no longer needs to provide the mtx folder.
	:type -k: str, optional
	:arg -x: Names of the HTO tag(s) to extract, separated by ``,``. Joint HTO samples are combined with ``+``, such as ``HTO_1+HTO_2``.
	:type -x: str, optional
	:arg -o: The path for storing the Same-Sample-Droplets (SSDs). SSDs are stored in mtx format. Requires a path argument.
	:type -o: str, optional
	:arg -f: Generate the full classification report. Requires a path argument. Defaults to ``SSD_mtx``.
	:type -f: str, optional
	:arg -c: Take input in csv format, instead of mmx format.
	:arg -t: Provide the confidence threshold value. Requires a float in (0,1). Defaults to ``0.8``.
	:type -t: float, optional
	:arg -s: Generate the simplified classification report. Requires a path argument.
	:type -s: str, optional
	:arg -u: Generate the statstic summary of the dataset. Including MSM, SSM rates. Requires an estimated total number of cells in the assay as input.
	:type -u: int, optional
	:arg -r: Store the data summary report. Requires a file argument. Only executes if ``-u`` is set.
	:type -r: str, optional
	:arg -e: Provide the cell list. Requires a file argument. Only executes if ``-u`` is set.
	:type -e: str, optional
	:arg -a: The estimated chance of having a phony GEM getting included in a pure type GEM cluster by the clustering algorithm. Requires a float in (0, 1). Only executes if ``-e`` executes. Defaults to ``0.05``.
	:type -a: float, optional

Examples
--------

Case 1: Basic Usage, Remove MSMs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once installed, GMM-Demux is directly accessible with the ``GMM-demux`` command.

.. code-block:: bash

	GMM-demux <cell_hashing_path> <HTO_names>

``<HTO_names>`` is a list of sample tags (HTOs) separated by ',' without whitespace.

For example, there are four sample barcoding tags in the example cell hashing dataset.
They are **HTO_1**, **HTO_2**, **HTO_3**, **HTO_4**. The ``<HTO_names>`` variable therefore is ``HTO_1,HTO_2,_HTO_3,HTO_4``.

The non-MSM droplets (SSDs) of the dataset are stored in the ``GMM_Demux_mtx`` folder under the current directory by default.

The output path can also be specified through the ``-o`` flag.

Example Command 
^^^^^^^^^^^^^^^

An example cell hashing data is provided in the ``example_input`` folder. ``<HTO_names>`` can be obtained from the ``features.tsv`` file.

.. code-block:: bash

	GMM-demux example_input/outs/filtered_feature_bc_matrix HTO_1,HTO_2,HTO_3,HTO_4

``<HTO_names>`` are included in the ``features.tsv`` file. The content of the ``feature.tsv`` file is shown below.

.. figure:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/features.png
	:figwidth: 40%

Output
^^^^^^

The default content in the output folder are the non-MSM droplets (SSDs), stored in MTX format. The output shares the same format with CellRanger 3.0. By default, the output is stored in ``SSD_mtx`` folder. The output location can be overwritten with the ``-o`` flag.

Case 2: Compute the MSM and SSM rates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To compute the MSM and SSM rates, GMM-Demux requires the ``-u`` flag:

* ``-u SUMMARY, --summary SUMMARY``  Generate the statstic summary of the dataset. Requires an estimated total number of cells in the assay as input.
 
The ``-u`` flag requires an additional ``<NUM_OF_CELL>`` argument, which is the estimated total count of cells in the single cell assay.

Example Command
^^^^^^^^^^^^^^^

.. code-block:: bash

	GMM-demux example_input/outs/filtered_feature_bc_matrix HTO_1,HTO_2,HTO_3,HTO_4 -u 35685

Output
^^^^^^

Below is an example report:

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/summary.png

* RSSM denotes the percentage of SSMs among the remaining SSDs (after removing all MSMs). RSSM **measures the quality of the final cell hashing dataset after removing MSMs**.

Case 3: Verify if a cell type exists 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GMM-Demux verifies if a putative cell type exists with the ``-e`` flag:

* ``-e EXAMINE, --examine``  EXAMINE Provide the cell list. Requires a file argument. Only executes if -u is set.

The ``-e`` flag requires a file name, which stores the list of droplet barcodes of the putative cell type.

Example Command
^^^^^^^^^^^^^^^

.. code-block:: bash

	GMM-demux example_input/outs/filtered_feature_bc_matrix HTO_1,HTO_2,HTO_3,HTO_4 -u 35685 -e example_cell_types/CD19+.txt
	GMM-demux example_input/outs/filtered_feature_bc_matrix HTO_1,HTO_2,HTO_3,HTO_4 -u 35685 -e example_cell_types/Doublets/CD3+CD4+CD19+.txt

Output
^^^^^^

An example output of a pure cell type:

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/pure_type.png

An example output of a phony cell type:

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/phony_type.png

Case 4: Use the csv file format as input, instead of the mtx format 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example Command
^^^^^^^^^^^^^^^

.. code-block:: bash

	GMM-demux -c example_hto.csv HTO_1,HTO_2,HTO_3,HTO_4 -u 35685

Case 5: Extract droplets that are labeled by a combination of sample tags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract droplets that are labeled by multiple sample barcoding tags, with the ``-x`` flag:

* ``-x EXTRACT, --extract`` EXTRACT  Names of the sample barcoding tag(s) to extract, separated by ``,``.  Joint tags are linked with ``+``.

**When** ``-x`` **is set, other functions of GMM-Demux will be turned off.**

*Case 5a: Extract a single HTO sample*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example Command
+++++++++++++++

.. code-block:: bash

	GMM-demux example_input/outs/filtered_feature_bc_matrix HTO_1,HTO_2,HTO_3,HTO_4 -x HTO_1

*Case 5b: Extract a single HTO sample that are jointly defined by multiple HTO tags*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``+`` to specify the joint HTO tags.

Example Command
+++++++++++++++

.. code-block:: bash

	GMM-demux example_input/outs/filtered_feature_bc_matrix HTO_1,HTO_2,HTO_3,HTO_4 -x HTO_1+HTO_2

*Case 5c: Extract multiple HTO samples*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``,`` to separate sample tags. Single tag samples can be merged with joint-tag samples.

Example Command
+++++++++++++++

.. code-block:: bash

	GMM-demux example_input/outs/filtered_feature_bc_matrix HTO_1,HTO_2,HTO_3,HTO_4 -x HTO3,HTO_1+HTO_2,HTO_1+HTO_4+HTO_2

Parsing the Classification Output
---------------------------------

There are two files in a classification output folder. A config file (ending with .config) and a classification file (ending with .csv).

The classification file contains the label of each droplet as well as the probability of the classification. The classification is represented with numbers which are explained in the config file.

Below shows the classification output of the example data:

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/class_output.png
 
Online Cell Hashing Experiment Planner
--------------------------------------

A GMM-Demux based online cell hashing experiment planner is publically accessible at `here <https://www.pitt.edu/~wec47/gmmdemux.html>`_.

.. figure:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/planner.png
	:figwidth: 60%
	:target: https://www.pitt.edu/~wec47/gmmdemux.html