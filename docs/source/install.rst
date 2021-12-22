Installation
============

Requirement
-----------

GMM-Demux requires python3 (>3.5).

Install
-------

GMM-Demux can be directly installed from PyPi. Or it can be built and installed locally.

Install GMM-Demux from PyPi
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

	pip3 install --user GMM_Demux

In some OS, the ``pip3`` is linked to ``pip`` by default. For these OS, the installation command is simply:

.. code-block:: bash

	pip install --user GMM_Demux

Check if ``pip3`` is linked to ``pip`` with ``pip -V``.

If one chooses to install GMM-Demux from PyPi, it is unnecessary to download GMM-Demux from github. However, we still recommend downloading the example dataset to try out GMM-Demux.

Install GMM-Demux locally using `setuptools <https://packaging.python.org/tutorials/installing-packages/>`_ and pip3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may choose to install GMM-Demux locally after cloning the github repository. However, **this is for advanced users only and support is not gauranteed**.

The command is provided below:

.. code-block:: bash

	cd <GMM-Demux dir>
	python3 setup.py sdist bdist_wheel
	pip3 install --user . 

Post installation processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If this is the first time you install a python3 software through pip, make sure you add the pip binary folder to your ``PATH`` variable.

Typically, the pip binary folder is located at ``~/.local/bin``.

The pip binary folder might locate at a different location if the user uses virtual enviroment. Pay attention to the pip installation output.

Here is an example installation output. The path of the pip binary folder is highlighted:

.. image:: https://raw.githubusercontent.com/CHPGenetics/GMM-Demux/master/path.png

To temporarily add the pip binary folder, run the following command:

.. code-block:: bash

	export PATH=~/.local/bin:$PATH

To permenantly add the pip library folder to your `PATH` variable, append the following line to your ``.bashrc`` file (assuming bash is the default shell).

.. code-block:: bash

	PATH=~/.local/bin:$PATH
