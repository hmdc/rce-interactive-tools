Architecture
============

Basic Overview
---------------
Submitting an interactive job to the RCE by issuing the following
command::

  rce_submit.py -r -a shell

performs the following tasks:

* Creates a ClassAd for the job and submits this classad to the central
  manager. A truncated version of a such a generated ClassAd is
  reproduced below.

::

  HMDCUseXpra = true
  Email = "evansarm@gmail.com"
  AccountingGroup = "group_interactive.esarmien"
  User = "esarmien@hmdc.harvard.edu"
  OnExitHold = false
  MyType = "Job"
  PeriodicHold = false
  PeriodicRemove = false
  Err =
  strcat("/nfs/home/E/esarmien/.HMDC/jobs/interactive","/","shell_2.31.3","_",ClusterId,"_","201510271445984022","/err.txt")
  ProcId = 0
  HMDCApplicationName = "shell"
  AcctGroupUser = "esarmien"
  JobUniverse = 5
  In = "/dev/null"
  HMDCApplicationVersion = "2.31.3"
  Requirements = true && TARGET.OPSYS == "LINUX" && TARGET.ARCH ==
  "X86_64" && TARGET.FileSystemDomain == MY.FileSystemDomain &&
  TARGET.Disk >= RequestDisk && TARGET.Memory >= RequestMemory
  LocalJobDir =
  strcat("/nfs/home/E/esarmien/.HMDC/jobs/interactive","/","shell_2.31.3","_",ClusterId,"_","201510271445984022")
  PublicClaimId = "<10.0.0.34:9619>#1442840844#313#..."
  WhenToTransferOutput = "ON_EXIT"
  Environment = "_='/usr/bin/rce_submit.py'
  XAUTHORITY='/nfs/home/E/esarmien/.Xauthority'
  MY_INTERACTIVE_JOB_DIR='/nfs/home/E/esarmien/.HMDC/jobs/interactive'
  LOCATE_PATH=':/nfs/tools/lib/locate/locate.db::/nfs/tools/lib/locate/locate.db::/nfs/tools/lib/locate/locate.db'
  KDE_IS_PRELINKED='1'
  HMDC_PROD_KEYS_PATH='/nfs/home/E/esarmien/.hmdc_prod_keys'
  rvm_version='1.26.11 (latest)' NX_ROOT='/nfs/home/E/esarmien/.nx'
  COLORTERM='gnome-terminal' LINES='43'
  rvm_path='/nfs/home/E/esarmien/.rvm' LESSOPEN='||/usr/bin/lesspipe.sh
  %s' RUBY_VERSION='ruby-2.2.1'
  _CONDOR_ENTITLEMENTS='\"admin,mail_manager_root,hmdcOpsview,rt,cvs,jabber,desktopadmin,jenkins,login_manager_rce,bomgar\"'
  LOGNAME='esarmien' USER='esarmien' HOME='/nfs/home/E/esarmien'
  PATH='/opt/bin:/usr/local/bin:/opt/bin:/usr/local/bin:/nfs/home/E/esarmien/.rvm/gems/ruby-2.2.1/bin:/nfs/home/E/esarmien/.rvm/gems/ruby-2.2.1@global/bin:/nfs/home/E/esarmien/.rvm/rubies/ruby-2.2.1/bin:/opt/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/bin:/usr/bin:/usr/X11R6/bin:/usr/local/HMDC/sbin:/usr/local/HMDC/bin:/nfs/home/E/esarmien/bin:/nfs/home/E/esarmien/.rvm/bin:/nfs/home/E/esarmien/.rvm/bin:/nfs/home/E/esarmien/.rvm/bin:/nfs/home/E/esarmien/bin:/usr/local/HMDC/sbin:/usr/local/HMDC/bin:/nfs/home/E/esarmien/bin:/usr/local/HMDC/sbin:/usr/local/HMDC/bin:/nfs/home/E/esarmien/bin:/nfs/home/E/esarmien/.rvm/bin:/nfs/home/E/esarmien/.rvm/bin:/nfs/home/E/esarmien/.rvm/bin'
  MFINPUTS=':/usr/share/texlive/texmf-dist/fonts/source/public/mathabx::/usr/share/texlive/texmf-dist/fonts/source/public/mathabx::/usr/share/texlive/texmf-dist/fonts/source/public/mathabx:'
  HMDC_DEV_KEYS_PATH='/nfs/home/E/esarmien/.hmdc_dev_keys'
  _CONDOR_EMAIL='\"esarmien@g.harvard.edu\"'
  LD_LIBRARY_PATH='/opt/lib64:/opt/lib:/nfs/home/E/esarmien/lib'
  SSH_AGENT_PID='17080' LANG='en_US.UTF-8' TERM='xterm' SHELL='/bin/bash'
  CVS_RSH='ssh'
  XDG_SESSION_COOKIE='eb5986295c70101fb32f63f90000001a-1445872821.791472-194473865'
  SESSION_MANAGER='local/unix:@/tmp/.ICE-unix/17079,unix/unix:/tmp/.ICE-unix/17079'
  SHLVL='2' _system_arch='x86_64' NXDIR='/usr/NX' G_BROKEN_FILENAMES='1'
  NX_CLIENT='/usr/NX/bin/nxclient' HISTSIZE='1000' WINDOWID='41943043'
  ORBIT_SOCKETDIR='/scratch/orbit-esarmien' XMODIFIERS='@im=none'
  IMSETTINGS_INTEGRATE_DESKTOP='yes' GIO_LAUNCHED_DESKTOP_FILE_PID='3453'
  NX_SYSTEM='/usr/NX'
  MY_BATCH_JOB_DIR='/nfs/home/E/esarmien/.HMDC/jobs/batch'
  GEM_PATH='/nfs/home/E/esarmien/.rvm/gems/ruby-2.2.1:/nfs/home/E/esarmien/.rvm/gems/ruby-2.2.1@global'
  rvm_bin_path='/nfs/home/E/esarmien/.rvm/bin' USERNAME='esarmien'
  IMSETTINGS_MODULE='none' GTK_IM_MODULE='gtk-im-context-simple'
  GIO_LAUNCHED_DESKTOP_FILE='/usr/share/applications/gnome-terminal.desktop'
  _system_version='6' rvm_prefix='/nfs/home/E/esarmien'
  HMDC_ADMIN_PATH='/nfs/home/E/esarmien/git/hmdc-admin' NX_TEMP='/tmp'
  T1FONTS=':/usr/share/texlive/texmf-dist/fonts/type1/public/mathabx-type1::/usr/share/texlive/texmf-dist/fonts/type1/public/mathabx-type1::/usr/share/texlive/texmf-dist/fonts/type1/public/mathabx-type1:'
  SSH_AUTH_SOCK='/scratch/keyring-11bgaB/socket.ssh'
  IRBRC='/nfs/home/E/esarmien/.rvm/rubies/ruby-2.2.1/.irbrc'
  _system_type='Linux'
  MY_RUBY_HOME='/nfs/home/E/esarmien/.rvm/rubies/ruby-2.2.1'
  ACRO_ENABLE_FONT_CONFIG='1' COLUMNS='166' SPSSTMPDIR='/scratch'
  _system_name='CentOS' NX_SESSION_ID='2FB0CB7AC10E341D8605AEC17D60E014'
  TMPDIR='/scratch'
  TEXINPUTS=':/usr/local/share/texlive/texmf:/usr/share/texlive/texmf-dist:/usr/share/texmf:/usr/local/share/texmf/hmdc/misc:/usr/share/texlive/texmf-dist/tex/latex/powerdot:/usr/local/share/texmf/hmdc/imsart:/usr/share/texlive/texmf-dist/tex/generic/mathabx::/usr/local/share/texlive/texmf:/usr/share/texlive/texmf-dist:/usr/share/texmf:/usr/local/share/texmf/hmdc/misc:/usr/share/texlive/texmf-dist/tex/latex/powerdot:/usr/local/share/texmf/hmdc/imsart:/usr/share/texlive/texmf-dist/tex/generic/mathabx::/usr/local/share/texlive/texmf:/usr/share/texlive/texmf-dist:/usr/share/texmf:/usr/local/share/texmf/hmdc/misc:/usr/share/texlive/texmf-dist/tex/latex/powerdot:/usr/local/share/texmf/hmdc/imsart:/usr/share/texlive/texmf-dist/tex/generic/mathabx::/usr/share/texmf/tex/latex/ppower4:/usr/lib/R/share/texmf:/usr/share/latex2html/texinputs::/usr/share/texmf/tex/latex/ppower4:/usr/lib/R/share/texmf:/usr/share/latex2html/texinputs::/usr/share/texmf/tex/latex/ppower4:/usr/lib/R/share/texmf:/usr/share/latex2html/texinputs:'
  CVSEDITOR='vi' KDEDIRS='/usr' JAVA_HOME='/usr/lib/jvm/java-1.8.0/jre'
  DISPLAY=':1004.0' NX_CUPS_BIN='/usr/bin'
  BIBINPUTS='.:/nfs/home/E/esarmien/gkbibtex:.:/nfs/home/E/esarmien/gkbibtex:.:/nfs/home/E/esarmien/gkbibtex::'
  OLDPWD='/nfs/home/E/esarmien/projects/rce-interactive-tools'
  HOSTNAME='dev-rce6-2.hmdc.harvard.edu'
  BSTINPUTS='.:/nfs/home/E/esarmien/gkbibtex:.:/nfs/home/E/esarmien/gkbibtex:.:/nfs/home/E/esarmien/gkbibtex::'
  TEXMFLOCAL=':/usr/share/texlive/texmf:/usr/share/texlive/texmf-dist:/usr/share/texmf:/usr/local/share/texmf::/usr/share/texlive/texmf:/usr/share/texlive/texmf-dist:/usr/share/texmf:/usr/local/share/texmf::/usr/share/texlive/texmf:/usr/share/texlive/texmf-dist:/usr/share/texmf:/usr/local/share/texmf:'
  HISTCONTROL='ignoredups' PWD='/nfs/home/E/esarmien' QT_IM_MODULE='xim'
  GTK_RC_FILES='/etc/gtk/gtkrc:/nfs/home/E/esarmien/.gtkrc-1.2-gnome2'
  MAIL='/var/spool/mail/esarmien'
  LS_COLORS='rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lz=01;31:*.xz=01;31:*.bz2=01;31:*.tbz=01;31:*.tbz2=01;31:*.bz=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:'
  GEM_HOME='/nfs/home/E/esarmien/.rvm/gems/ruby-2.2.1'
  TFMFONTS=':/usr/share/texlive/texmf-dist/fonts/tfm/public/mathabx::/usr/share/texlive/texmf-dist/fonts/tfm/public/mathabx::/usr/share/texlive/texmf-dist/fonts/tfm/public/mathabx:'"
  TargetType = "Machine"
  LeaveJobInQueue = false
  JobNotification = 1
  Owner = "esarmien"
  CondorPlatform = "$CondorPlatform: x86_64_RedHat6 $"
  JobLeaseDuration = 1200
  RecentBlockWriteKbytes = 0
  TransferIn = false
  ExitStatus = 0
  RootDir = "/"
  NumJobMatches = 1
  JobCurrentStartDate = 1445969625
  HMDCInteractive = true
  Args = false
  CondorVersion = "$CondorVersion: 8.2.9 Aug 13 2015 BuildID: 335839 $"
  Out =
  strcat("/nfs/home/E/esarmien/.HMDC/jobs/interactive","/","shell_2.31.3","_",ClusterId,"_","201510271445984022","/out.txt")
  ShouldTransferFiles = "NO"
  FileSystemDomain = "hmdc.harvard.edu"
  JobPrio = 0
  NumCkpts = 0
  DebugPrepareJobHook = true
  BufferBlockSize = 32768
  ImageSize = 325000
  StatsLifetimeStarter = 3286729
  Cmd = "/usr/bin/gnome-terminal"
  Iwd = "/nfs/home/E/esarmien"
  AcctGroup = "group_interactive"
  Entitlements = "admin mail_manager_root hmdcOpsview rt cvs jabber
  desktopadmin jenkins login_manager_rce bomgar"

* A number of these ClassAd elements are added by rce_submit.py and are
  have effects on job routing.

* Upon submission, rce_submit.py polls the central manager, every five
  seconds, to check whether the job has started yet, polling for a
  maximum of 90 seconds. The ``POLL_TIMEOUT`` is set in
  ``hmdccondor/HMDCCondor.py``.

* When the poller finds that the submitted ClassAd now has a ``JobStatus
  == 2``, ``rce_submit.py`` launches Xpra to connect to the running
  job's xpra server.

Server-side Operations
----------------------

Starting a job
^^^^^^^^^^^^^^

Most of the work is performed by HTCondor startd or execute nodes.

* When a job submitted using rce_submit.py starts running, the execute
  node runs ``HMDC_interactive_prepare_job``, as configured in
  ``hmdc-admin/templates/etc-condor-config.d/compute.config.erb``::

    HMDC_HOOK_UPDATE_JOB_INFO = $(PIP_BINDIR)/HMDC_periodic_job_is_idle.py
    HMDC_HOOK_PREPARE_JOB = $(PIP_BINDIR)/HMDC_interactive_prepare_job.py
    HMDC_HOOK_JOB_EXIT = $(PIP_BINDIR)/HMDC_clean_up.py
    STARTER_JOB_HOOK_KEYWORD = HMDC

* ``HMDC_interactive_prepare_job`` performs the following tasks:

  * Creates a job directory under ``$HOME/.HMDC/jobs/interactive``,
    specified by the classad element ``LocalJobDir`` to
    house stdout, stderr, and console output from job. When the XPRA
    server is started, XPRA server output is written to this directory.

* After ``HMDC_interactive_prepare_job`` successfully completes,
  ``HMDC_job_wrapper.py`` executes the command specified in the job
  classad by:

  * Setting ulimits on the executing job based on the slot's memory and
    cpu allocation.
  * Executing an Xpra server which runs the command specified in the
    job classad.

Counting idle time
^^^^^^^^^^^^^^^^^^
* ``HMDC_periodic_job_is_idle.py`` is run periodically for each job
  running on an execute node, as configured in
  ``hmdc-admin/templates/etc-condor-config.d/compute.config.erb``.

* ``HMDC_periodic_job_is_idle.py`` performs the following functions:
  
  * Opens ``$TEMP/.idletime`` and reads the integer representing the
    total time a job was idle. Here, ``$TEMP`` is the job's execute
    directory under ``/tmp/condor/execute``
  * If the job is currently idle, ``HMDC_periodic_job_is_idle.py``
    subtracts the mtime of ``$TEMP/.idletime`` from the current time and
    adds this value to the idle time value stored in
    ``$TEMP/.idletime``.
  * If the job is currently active, ``HMDC_periodic_job_is_idle.py``
    writes 0 to ``$TEMP/.idletime``
  * If the job is currently idle and idle for two or more days,
    ``HMDC_periodic_job_is_idle.py`` sends a notification to the job
    owner of the job's impeding preemptibility.

* ``HMDC_periodic_job_is_idle.py`` calculates idletime for a job, but, a
  different script actually propagates this value to the HTCondor
  collector.

* Every five minutes, cron runs
  ``/usr/bin/HMDC_startd_cron_idle_generator.py``

* ``/usr/bin/HMDC_startd_cron_idle_generator.py`` performs the following
  tasks:

  * For every running job, opens and reads the value in
    ``$TMP/.idletime``
  * If idletime is greater than zero, generates a string composed of all
    Job IDs and idle times and writes this as a script to
    ``/usr/bin/HMDC_startd_cron_idle.sh``, for example::

      [root@dev-cod6-1 bin]# /usr/bin/HMDC_startd_cron_idle.sh 
      HMDCIdleJobs = "110.0,3702664 113.0,3637730 114.0,0 187.0,105483
      192.0,105480 198.0,105484"

* Every ten seconds, HTCondor executes
  ``/usr/bin/HMDC_startd_cron_idle.sh``, which publishes the
  ``HMDCIdleJobs`` machine classad to the collector, as configured in::

    STARTD_CRON_IDLEJOBS_AUTOPUBLISH = If_Changed
    STARTD_CRON_IDLEJOBS_EXECUTABLE = /usr/bin/HMDC_startd_cron_idle.sh
    STARTD_CRON_IDLEJOBS_MODE = Periodic
    STARTD_CRON_IDLEJOBS_PERIOD = 10s
    STARTD_CRON_JOBLIST =  idlejobs

.. note::

  Unfortunately, a system cron job and an HTCondor cron job are
  required, but, not desired. The ``.idletime`` file created by
  ``HMDC_periodic_job_is_idle.py`` is owned by the executing user,
  whereas scripts executed by ``STARTD_CRON`` run as user ``daemon`` and
  are unable to read ``.idletime`` files. Therefore, a root system
  cronjob reads these files such that the `STARTD_CRON`` job can access
  them.


ClassAd Elements
----------------

+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ClassAd Element        | Accepted values                                                 | Description                                                              | Effect                                                                                                                                                                                                                                                                                                       |
+========================+=================================================================+==========================================================================+==============================================================================================================================================================================================================================================================================================================+
| HMDCUseXpra            | True, False                                                     | Determines whether a job should use XPRA                                 | If True, execute node treats this job as an XPRA-enabled interactive job, launching an XPRA server to execute the job's command.                                                                                                                                                                             |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| AccountingGroup        | group_interactive.$(Owner) or group_batch.$(Owner)              | Places a job into an accounting group                                    | If set to group_interactive.$(Owner), user's job is limited by group_interactive's quota. If set to group_batch.$(Owner), user's job is l imited by group_batch's quota. In January 2016, quotas will be disabled in favor of multi-slot pre-emption and this ClassAd element will become deprecated.        |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Err                    | Fully qualified path to stderr output                           | Location of stderr output file.                                          | The running job's stderr output will be redirected to this file.                                                                                                                                                                                                                                             |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| HMDCApplicationName    | A human readable string denoting the running job's application  | A human readable string denoting the running job's application           | No effect, useful for statistics                                                                                                                                                                                                                                                                             |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| HMDCApplicationVersion | A string denoting the running job's version                     | A string denoting the running job's version                              | No effect, useful for statistics                                                                                                                                                                                                                                                                             |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| LocalJobDir            | Fully qualified path of a directory                             | This directory will store stdout and stderr output from the running job. | LocalJobDir will be created by the HTCondor execute node and stderr and stdout output friom the job will be stored in this directory.                                                                                                                                                                        |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Environment            | A string of x=y pairs separated by spaces the job's environment | The job's environment                                                    | This is a standard HTCondor ClassAd element populated by rce_submit.py with the user's shell environment, subtracting GNOME and DBUS environment variables.                                                                                                                                                  |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| HMDCInteractive        | True, False                                                     | Determines whether a job should be treated as an interactive job         | HMDCInteractive, when set to True, influences a number of HTCondor policy decisions:                                                                                                                                                                                                                         |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Entitlements           | A string of entitlements separated by spaces                    | The user's eduPersonEntitlements                                         | Entitlements is populated by rce_submit.py by querying LDAP, or, when using condor_submit, through the environment varaible ``$_CONDOR_ENTITLEMENTS ``created by ``/etc/profile.d/Condor_group.sh`` or ``/etc/profile.d/Condor_group.csh``                                                                   |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Out                    | Fully qualified path to stdout output                           | Location of stdout output file                                           | The running job's stdout output will be redirected to this file.                                                                                                                                                                                                                                             |
+------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
