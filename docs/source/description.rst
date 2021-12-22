Introduction
============
GMM-Demux identifies Multi-Sample Multiplets (MSMs) in a sample barcoding dataset. Below shows an example distribution of MSMs in a PBMC scRNA-seq dataset. Orange dots in the scatter plot are MSMs.

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/GMM_simplified.png

Description
-----------
GMM-Demux removes Multi-Sample-Multiplets (MSMs) in a cell hashing dataset and estimates the percentages of Same-Sample-Multiplets (SSMs) and singlets in the remaining dataset.
GMM-Demux also verifies if a putative cell type exists, or is it merely an artifact induced by multiplets.

Multiplet-induced fake cell types are called "phony cell types".

Examples of phony cell types in a PBMC CITE-seq dataset is provided in the figure below:

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/phony.png

In the above figure, both the CD3+CD19+ and the CD4+CD8+ cell types are multiplet-induced fake cell types.

Phony type clusters have large percentages of MSMs, as above figure shows. Both phony type clusters have large MSM percentages.

Percentages of MSMs are used as key features by GMM-Demux to classify GEM clusters.

Terminology
-----------
* **Singlet**: A droplet that contains a single cell.

* **MSM**: Multi-Sample Multiplet. A MSM is a multiplet that contains cells from different samples in sample barcoding. MSMs can be identified by GMM-Demux.

* **SSM**: Same-Sample Multiplet. A SSM is a multiplet that contains cells from a single sample in sample barcoding. SSMs cannot be separated from singlets by sample barcoding.

* **SSD**: Same-Sample Droplet. SSD is a combined category of both SSMs and singlets.

* **Pure type**: a pure type cell type is a real cell type that exist in the tissue.

* **Phony type**: a phony type cell type is an artificial cell type that is an artifact produced by multiplets.

* **Mixture type**: a mixture type cell type is a cluster of droplets in which there exist a non-trivial fraction of phony type droplets.

An illustration of the above terminologies in a PBMC dataset is provided in the figure below:

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/term.png

Features
--------
* Remove cell-hashing-identifiable multiplets (i.e., MSMs) from the dataset.
* Estimate the fraction of cell-hashing-unidentifiable multiplets (SSMs) in the remaining dataset (the RSSM percentage).
* Test if a putative cell type is a pure (real) cell type or is it a phony (fake) cell type.

Example Dataset
---------------
* An example cell hashing dataset is provided in the *example_input* folder. It contains the per-drop HTO count matrix of a 4-sample cell hashing library prep. The input folder has the same file format with the CellRanger v3 output.