Mackinac: A bridge between ModelSEED and COBRApy
================================================

Mackinac combines the ability of `ModelSEED <http://modelseed.org>`_ to automatically
reconstruct metabolic models with the advanced analysis capabilities in
`cobrapy <https://github.com/opencobra/cobrapy>`_ to bridge the differences between
the two frameworks. Mackinac provides support for using the ModelSEED
web service to create draft genome-scale models from genomes available in the
`Pathosystems Resource Integration Center <https://www.patricbrc.org/portal/portal/patric/Home>`_
(PATRIC) and creates a COBRA model from a ModelSEED model. If you are not a
`registered PATRIC user <http://enews.patricbrc.org/faqs/workspace-faqs/registration-faqs/>`_,
you must complete a `new user registration <https://user.patricbrc.org/register/>`_
to work with the ModelSEED web service.
 
If you already have models available in ModelSEED, you can simply import and
create a COBRA model with the ``create_cobra_model_from_modelseed_model()``
function. You can then use all of the features in cobrapy to analyze,
inspect, explore, and draw conclusions from the model.

You can also reconstruct and gap fill models using the ModelSEED
service for any organism with a genome available in PATRIC. Additional functions
are available for working with ModelSEED models, managing workspace objects,
getting information about PATRIC genomes, and calculating reaction likelihoods.

Please use the `cobrapy Google
Group <http://groups.google.com/group/cobra-pie>`_ for help.
Alternatively, you can use
`gitter.im <https://gitter.im/opencobra/cobrapy>`_ for quick questions
and discussions (faster response times).

More information about opencobra is available at the
`website <http://opencobra.github.io/>`_.

Installation
------------

Use pip to install Mackinac from
`PyPI <https://pypi.python.org/pypi/mackinac>`_ (we recommend doing this
inside a `virtual environment
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_)::

    pip install mackinac

Web service URLs
----------------

Mackinac uses web services provided by other organizations which can be offline,
the interface can change, or the URL can change. Mackinac uses these default URLs:

* ModelSEED web service at http://p3c.theseed.org/dev1/services/ProbModelSEED
* Workspace web service at https://p3.theseed.org/services/Workspace
* PATRIC web service at https://www.patricbrc.org/api/

Alternate URLs include the following:

* Former production ModelSEED web service at https://p3.theseed.org/services/ProbModelSEED

You can change the URL used to connect to a web service as shown below:

    >>> import mackinac
    >>> mackinac.modelseed.ms_client.url = 'http://p3c.theseed.org/dev1/services/ProbModelSEED'
    >>> mackinac.workspace.ws_client.url = 'https://p3.theseed.org/services/Workspace'
    >>> mackinac.genome.patric_url = 'https://www.patricbrc.org/api/'

Direct installation in virtual environment
------------------------------------------

1. If virtualenvwrapper is not installed, `follow the directions <https://virtualenvwrapper.readthedocs.io/en/stable/>`__
   to install virtualenvwrapper. You should also `update your shell startup file
   <http://virtualenvwrapper.readthedocs.io/en/stable/install.html#shell-startup-file>`_.

2. Clone the `git repository <https://github.com/mmundy42/mackinac>`_ to your
   computer with this command::

    $ git clone https://github.com/mmundy42/mackinac.git

3. Create a virtualenv for Mackinac with these commands::

    $ cd mackinac
    $ mkvirtualenv mackinac

   Use the ``--python`` option to select a specific version of Python for the
   virtualenv. For example, ``python=python3`` to select the current python3
   installed on the system.

   Note on macOS, matplotlib requires Python be installed as a framework but
   virtualenv creates a non-framework build of Python. See the
   `matplotlib FAQ <http://matplotlib.org/1.5.3/faq/virtualenv_faq.html>`__
   for details on a workaround.

4. Upgrade pip and setuptools to the latest versions with these commands::

    (mackinac)$ pip install --upgrade pip setuptools

5. Install all of the Mackinac dependencies with this command::

    (mackinac)$ pip install -r requirements.txt

   This command can take a few minutes while numpy, pandas, and libsbml are
   built in the virtualenv.

6. Install the latest version of Mackinac with this command::

    (mackinac)$ python setup.py install

7. Install the pytest package with this command::

    (mackinac)$ pip install pytest

8. You need to provide a username and password for the tests to obtain an
   authentication token. Substitute your PATRIC username and password and run
   the tests with this command::

    (mackinac)$ TEST_USERNAME=<username> TEST_PASSWORD=<password> pytest mackinac/test -v

Run examples in a notebook
^^^^^^^^^^^^^^^^^^^^^^^^^^

An example of how to use Mackinac is provided in a notebook. Here's how to start Jupyter and run
the notebook from the virtualenv.

1. Install Jupyter with this command::

    (mackinac)$ pip install jupyter

2. Install a kernel that uses the virtualenv installation with this command::

    (mackinac)$ ipython kernel install --name "Mackinac_Python27" --user

3. Start the Jupyter notebook server with this command::

    (mackinac)$ jupyter notebook

   Jupyter opens a web page in your default browser with a file browser.

4. Navigate to the "documentation_builder" folder and click on the "modelseed.ipynb"
   notebook.

5. After the notebook opens, from the "Kernel" menu, select "Change kernel" and
   click on "Mackinac_Python27".

6. Now you can run the cells in the notebook.

Release Notes
-------------

Version 0.8.2 (May 5, 2017)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Removed dependency on a specific version of six package
* Updated directions for virtual environment installation
* Switched default ModelSEED service URL to current active server

Version 0.8.1 (March 15, 2017)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Version corresponding to published paper

How to cite Mackinac
--------------------

If you use Mackinac for an analysis, please cite this paper:
`Mackinac: a bridge between ModelSEED and COBRApy to generate and analyze genome-scale
metabolic models <https://dx.doi.org/doi:10.1093/bioinformatics/btx185>`_


References
----------

1. `COBRApy: COnstraints-Based Reconstruction and Analysis for Python <http://dx.doi.org/doi:10.1186/1752-0509-7-74>`_
2. `High-throughput generation, optimization and analysis of genome-scale metabolic models <http://dx.doi.org/doi:10.1038/nbt.1672>`_ (ModelSEED)
3. `PATRIC, the bacterial bioinformatics database and analysis resource <http://dx.doi.org/doi:10.1093/nar/gkt1099>`_

Mackinac Bridge
^^^^^^^^^^^^^^^

The `Mackinac Bridge <http://www.mackinacbridge.org>`_ is one of the longest
suspension bridges in the United States and spans the Straits of Mackinac to
connect the Upper and Lower Peninsulas of Michigan.
