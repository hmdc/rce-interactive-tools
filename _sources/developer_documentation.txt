Operations/Development Documentation
====================================

.. toctree::
   :maxdepth: 2
   :hidden:

   development/modules
   development/logs
   development/architecture
   development/add_an_app

Getting the source code
-----------------------
``git clone git@github.com:hmdc/rce-interactive-tools.git``

Upgrading application to latest master
--------------------------------------
For development environment, run from ``hmdc-admin`` checkout::

  cap condor:upgrade_hmdc_cluster_tools

For production environment, run from ``hmdc-admin`` checkout::

  cap production condor:upgrade_hmdc_cluster_tools

Building the documentation
--------------------------
From the RCE, run::

  git clone git@github.com:hmdc/rce-interactive-tools.git
  pip install sphinx --user --force-reinstall --upgrade
  pip install sphinx_rtd_theme --user --force-reinstall --upgrade
  cd rce-interactive-tools/doc
  PATH=~/.local/bin:$PATH PYTHONPATH=../:$PYTHONPATH make html

Once you've installed the  ``sphinx`` and ``sphinx_rtd_theme``
pre-requisites, you can rebuild documentation by running::

  cd rce-interactive-tools/doc
  PATH=~/.local/bin:$PATH PYTHONPATH=../:$PYTHONPATH make html

HTML output is placed in ``rce-interactive-tools/doc/build/html`` which
you can view via any web browser.

.. note::

  Sphinx and sphinx_rtd_theme are already installed on NFS in
  ``/nfs/tools/lib/python/2.6/current``. However, the Python 2.6
  virtualenv executable is unable to locate htcondor appropriately. In
  the meantime, I simply force reinstall these modules to my home
  directory in order to build the documentation. Although someone should
  look into this.

.. note::

   This entire process could be done automatically via Jenkins git
   hooks.

Editing the documentation
-------------------------
Documentation is written with sphinx and ReST. Here are some helpful
resources:

* `Restructed Text (reST) and Sphinx Cheat Sheet
  <http://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_
* `Documenting Your Project Using Sphinx
  <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_

Publishing documentation to GitHub pages
----------------------------------------
From the RCE, run::

  cd rce-interactive-tools/doc
  PATH=~/.local/bin:$PATH PYTHONPATH=../:$PYTHONPATH make html ghpages
