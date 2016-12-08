#!/bin/bash
# This is because XPRA is passing -p and -T which we aren't interested
# in. Hacky! Help! Temporary only!
/usr/bin/condor_ssh_to_job "${1}" "${2}" "${@:6}"
