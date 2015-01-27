#!/bin/sh

# Author: Evan Sarmiento <esarmien@g.harvard.edu>
# How This Works
# ===============
# Why? When you run
#
# --> xpra attach dev-cod6-1.priv:5, where 5 is the X11 display
#
# The xpra client ssh to dev-cod6-1 and runs 
#
# --> xpra initenv || echo "Warning..." >/dev/null 2>&1; ~/.xpra/run-xpra.sh
#
# We want to make sure that only administrative users can SSH directly
# to the cod nodes, but that all other users are at least able to run
# the XPRA command such that they can access their XPRA sessions.
# The ${SSH_ORIGINAL_COMMAND} expands to the command listed above.
# If you, for example, run:
#
# --> ssh dev-cod6-1.priv ls -all /
#
# ${SSH_ORIGINAL_COMMAND} would evaluate to 'ls -all /'
# Therefore, this script checks SSH_ORIGINAL_COMMAND to determine if
# this is an XPRA client attempting to connect. If it is,
# this script evaluates the original ${SSH_ORIGINAL_COMMAND}.
# Otherwise this script returns an error.
# How is this script run?
# /etc/ssh/sshd_config uses 'ForceCommand' to run this script
# instead of the user's shell for users in non-administrative groups.
# 
# Caveats, FIXME.
# ===============
# A better way to do this would be to use condor_ssh_to_job in order
# to set up the xpra environment. However, condor_ssh_to_job 
# uses the default COLLECTOR, which is the batch collector, and
# is unable to connect to cod jobs. We can probably figure out
# how to use this in the future, so we can get rid of this wrapper.

echo ${SSH_ORIGINAL_COMMAND}|egrep -o 'xpra initenv \|\| echo \"Warning: xpra server does not support initenv\"' >/dev/null 2>&1 && eval ${SSH_ORIGINAL_COMMAND} || cat <<EOF ; exit 1
#############################################
# NOTICE                                    #
#############################################
`hostname` is not accessible via SSH. Please
use the RCE Powered Menu to launch a job.
EOF
