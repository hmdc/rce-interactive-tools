Using the RCE submit command line client (for advanced users)
=============================================================

Accessing the terminal
----------------------
If you're working within a NoMachine NX session, open the terminal by
selecting Applications |rarr| System Tools |rarr| Terminal.

You can also SSH to ``rce.hmdc.harvard.edu`` if you prefer to launch
interactive jobs outside of a NoMachine NX4 session, but, you will still
need an X server running client-side. If you're currently running any
variant of the Linux operating system, using ``ssh -X`` should suffice,
otherwise, follow these links to download X servers for your operating
system:

* Windows: `Xming <http://www.straightrunning.com/xmingnotes/>`_
* OS X: `Xquartz <http://www.xquartz.org/>`_

.. warning::

   HMDC does not support locally installed X servers, only NoMachine
   NX4. However, if you feel comfortable operating a locally installed X
   server, feel free to give it a whirl!

Listing available applications
------------------------------
While GUI RCE submit tools only supports Matlab for the rest of the 2015
calendar year, the RCE submit tools command line client supports all
applications in the RCE. You can list which applications are supported
by running the following command::

  rce_submit.py -list

which will output a list of supported applications and versions::

  ** denotes default
  Application    Version(s)
  -------------  ------------
  gauss          14 **
                 8
  mathematica    10.2.0
                 10.1.0
                 10.3.0 **
  matlab         R2015a **
                 R2012a
                 R2013a
                 R2014b
                 R2014a
                 R2010b
  octave         3.4.3 **
  python         3.3
                 2.7 **
  R              3.2 **
  rstudio        0.98 **
  SAS            9.3
                 9.4 **
  shell          2.31.3 **
  StatTransfer   12 **
  xstata-mp      13.1
                 14.0 **
  xstata-se      13.1
                 14.0 **

Running an application
----------------------
You can run the default version of the application ``python``, by
executing::

  rce_submit.py -r -a python

You can run ``python 3.3`` by executing::

  rce_submit.py -r -a python -v 3.3

Listing running applications
----------------------------
You can list which RCE interactive applications you are currently
running, whether attached or detached, by executing::

  rce_submit.py --jobs

which produces the following output::

    Job Id  Application    Version    Requested Cpus    Requested Memory
  --------  -------------  ---------  ----------------  ------------------
       174  xstata-mp      14.0       4                 6144
       183  matlab         R2015a     1                 12288
       113  shell          2.31.3     1                 2048
       110  shell          2.31.3     1                 2048

(Re)attaching an application
----------------------------
If you've disconnected your application from yoiur desktop, you can
re-attach it using the command line tools by first running
``rce_submit.py --jobs``, noting the Job Id of the job you want to
re-attach and then executing::

  rce_submit.py -attach 174

In the above example, I reattached xstata-mp.

Creating a custom application launcher
--------------------------------------
You may have installed an application locally to your home directory
which has GUI capabilities and want to run this application in our
HTCondor cluster. RCE cluster tools uses a configuration file format
called ``rceapp.yml`` to manage application settings.

First, you should copy the existing ``rceapp.yml`` into your home
directory to get an idea of how this file is structured::

  cp /etc/rceapp.yml $HOME

Here is a simple stanza from rceapp.yml describing the gnome-terminal::

  shell:
    global:
      memory: 2048
      cpu: 1
      icon: /usr/share/icons/gnome/32x32/apps/gnome-terminal.png
      supports_memory_adjustable: true
      supports_cpu_adjustable: true
      supports_cli_mode: true
    '2.31.3':
      default: true 
      command: /usr/bin/gnome-terminal
      command_nogui: $ENV(SHELL)

Presume that I want to run firefox as an interactive job in the RCE
cluster. I would first edit my local rceapp.yml at ``$HOME/rceapp.yml``
and add the following stanza::

  firefox:
    global:
      memory: 2048
      cpu: 1
      icon: /usr/share/icons/gnome/32x32/apps/gnome-terminal.png
      supports_memory_adjustable: true
      supports_cpu_adjustable: true
      supports_cli_mode: true
    '10.0':
      default: true 
      command: /usr/bin/firefox

Then, I could run firefox by running the following command, which would
create a firefox job that consumes 1 CPU and 2048 MiB of memory::

  rce_submit.py -f $HOME/rceapp.yml -r -a firefox

The ``-f`` switch designates that you're using a custom ``rceapp.yml``
rather than the system-wide ``rceapp.yml`` in ``/etc``

Getting help
------------
Running the following command will print out inline help for
rce_submit.py::

  rce_submit.py -help


.. |rarr| unicode:: U+2192 .. right arrow symbol
