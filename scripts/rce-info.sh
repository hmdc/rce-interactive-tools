#!/bin/bash

# condor_status -format "%d\n" Cpus -constraint '(RemoteOwner =?= undefined && ! regexp("ksg", Machine))' -pool cod6-head.priv.hmdc.harvard.edu|sort -n|tail -1

# Description

printhelp() {
    cat <<EOF >&2
Usage: $0 [-v] -t <available|used>
       $0 -h

Displays RCE cluster resource utilization.

Parameters:
      -h 
           Print this help text and exit.
      -t <available|used>
           Print available resources (default), or used resources.
      -v 
           Verbose
      
EOF
}

# Parameters

TYPE="available"
CLUSTER="all"
unset VERBOSE
while getopts ":ht:v-" opt; do
    case $opt in
        h)
        printhelp                 # print help
        exit 0
        ;;
        t)
        TYPE="$OPTARG"            # type of query
        ;;
        v)
        VERBOSE="1"               # print more detail
        ;;
        -)
        break                     # end argument parsing
        ;;
    esac
done
shift $(($OPTIND - 1))

# Constants

CONDOR_CONFIG_VAL=$(which condor_config_val)
FIGLET=$(which figlet 2>/dev/null || echo /usr/bin/figlet)

# Only include ksg machines if user has kennedy entitlement
_CONSTRAINT='RemoteOwner =?= undefined'
CONSTRAINT="($(echo ${_CONDOR_ENTITLEMENTS}|grep kennedy >/dev/null 2>&1 && echo "${_CONSTRAINT}" || echo "${_CONSTRAINT} && ! regexp(\"ksg\", Machine) && ! regexp (\"edlabs\", Machine) "))"

# Main

case "$TYPE" in
    available)
      cat <<EOF
$(${FIGLET} -f small 'RCE Cluster' 2> /dev/null|| echo "==== RCE Cluster ====")
    Largest Possible CPU Reservation: $(condor_status -autoformat Cpus -constraint "${CONSTRAINT}"|sort -n|tail -1)
    Largest Possible Memory Reservation: $(condor_status -format "%d GB\n" Memory/1024  -constraint "${CONSTRAINT}"|sort -n|tail -1)
EOF
    ;;
    used)
      ${FIGLET} -f small 'RCE Cluster' 2> /dev/null|| echo "==== RCE Cluster ===="
      /usr/bin/condor_q -global -currentrun -constraint '( JobStatus == 2)' -format '%s ' User -format '%d ' RequestCpus -format '%d \n' RequestMemory |perl -e 'while (<>) { @f = split(/\s+/, $_); $sum{$f[0]}{cpu} += $f[1]; $sum{$f[0]}{mem} += $f[2]; } printf( "%15s %4s %s\n", "USER", "CPUS", "MEM_GB" ); foreach $u ( sort(keys(%sum)) ) { $us = $u; $us =~ s/\@hmdc\.harvard\.edu//; printf( "%15s %4d %d\n", $us, $sum{$u}{cpu}, $sum{$u}{mem} / 1024 ); }'
    ;;
esac

