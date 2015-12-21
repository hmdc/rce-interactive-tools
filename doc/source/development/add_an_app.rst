Adding an RCE Powered Application to the menu
=============================================

Changes
-------
As of 12/15, the following individual application modules were removed:

* modules/gauss
* modules/matlab 
* modules/mathematica
* modules/hmdc_rce_shell
* modules/rstudio
* modules/stata
* modules/stattransfer
* modules/jabref
* modules/gauss
* modules/octave
* modules/gephi
* modules/sas

Furthermore, modules ``modules/hmdc_emacs``, ``modules/hmdc_r`` were
stripped of their icon and desktop creating elements, leaving only our
HMDC customizations.

Instead, all RCE Powered Application desktop and icon creation has been
moved to ``modules/rceapp`` utilizing one single file in
``modules/hmdc_cluster_tools/files/rceapp.yml``

Adding an application with a pre-installed icon
-----------------------------------------------
Presume we want to add Firefox as an RCE Powered Application, adding it
to the RCE Powered Menu.

First, edit ``modules/hmdc_cluster_tools/files/rceapp.yml`` and add this
stanza::

	firefox:
	  global:
	    memory: 2048
	    cpu: 1
	    icon: /usr/share/icons/hicolor/48x48/apps/firefox.png
      install_icon: false
	    supports_memory_adjustable: true
	    supports_cpu_adjustable: true
	    supports_cli_mode: false
	    requires_wrapper: false
	  '38.4.0':
	    default: true
	    command: /usr/bin/firefox

Now, run a standard ``cap ROLES=cluster deploy puppet:apply`` in the DEV environment.

This will create the RCE Powered Application menu for Firefox.

Please note the following oddities:

* ``icon`` must be the FQDN of the ``48x48`` icon as installed by the
  Firefox package.
* Since the icon is installed by the RPM, ``install_icon`` must be
  false, otherwise rceapp will try to install the icon from
  ``modules/rceapp/files``
* Firefox does not require a wrapper ``/usr/local/bin/firefox`` as we
  allow users to run firefox from the RCE login nodes.

Adding an application without a pre-installed icon
--------------------------------------------------

Use the same example as above, except:

* Set ``install_icon`` to true
* Move ``firefox.png``, or whatever application icon you need, to
  ``modules/rceapp/files``


