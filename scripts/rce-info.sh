#!/bin/bash

# condor_status -format "%d\n" Cpus -constraint '(RemoteOwner =?= undefined && ! regexp("ksg", Machine))' -pool cod6-head.priv.hmdc.harvard.edu|sort -n|tail -1

# Description

printhelp() {
    cat <<EOF >&2
Usage: $0 [-v] -c <batch|interactive|all> -t <available|used>
       $0 -h

Displays RCE cluster resource utilization.
Queries either the Interactive or Batch cluster, or both.

Parameters:
      -c <batch|interactive|all>
           Query the Batch cluster, Interactive cluster, or both (default).
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
while getopts ":c:ht:v-" opt; do
    case $opt in
        c)
        CLUSTER="$OPTARG"         # cluster to query
        ;;
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
HMDC_INT_HEAD=$(${CONDOR_CONFIG_VAL} HMDC_INT_HEAD)
FIGLET=$(which figlet 2>/dev/null || echo /usr/bin/figlet)

# Only include ksg machines if user has kennedy entitlement
_CONSTRAINT='RemoteOwner =?= undefined'
CONSTRAINT="($(echo ${_CONDOR_ENTITLEMENTS}|grep kennedy >/dev/null 2>&1 && echo "${_CONSTRAINT}" || echo "${_CONSTRAINT} && ! regexp(\"ksg\", Machine)"))"

# Main

case "$TYPE" in
    available)
        if [ "$CLUSTER" == "batch" -o "$CLUSTER" == "all" ]; then
            cat <<EOF
$(${FIGLET} -f small 'Batch Cluster' 2> /dev/null || echo "==== Batch Cluster ====")
    Slots Available: $(condor_status -autoformat SlotId -constraint 'RemoteOwner =?= undefined'|wc -l)
    Max Memory Per Slot: $(condor_status -format "%d GB\n" Memory/1024 -constraint 'RemoteOwner =?= undefined'|sort -n|head -1)
    Max Cpus Per Slot: $(condor_status -format "%d\n" Cpus -constraint 'RemoteOwner =?= undefined'|sort -n|head -1)
EOF
        fi
        if [  "$CLUSTER" == "all" ]; then
            echo
        fi
        if [ "$CLUSTER" == "interactive" -o "$CLUSTER" == "all" ]; then
            cat <<EOF
$(${FIGLET} -f small 'Interactive Cluster' 2> /dev/null|| echo "==== Interactive Cluster ====")
    Largest Possible CPU Reservation: $(condor_status -autoformat Cpus -constraint "${CONSTRAINT}" -pool ${HMDC_INT_HEAD}|sort -n|tail -1)
    Largest Possible Memory Reservation: $(condor_status -format "%d GB\n" Memory/1024  -constraint "${CONSTRAINT}" -pool ${HMDC_INT_HEAD}|sort -n|tail -1)
EOF
        fi
    ;;
    used)
        if [ "$CLUSTER" == "batch" -o "$CLUSTER" == "all" ]; then
            ${FIGLET} -f small 'Batch Cluster' 2> /dev/null || echo "==== Batch Cluster ===="
            /usr/bin/condor_q -global -currentrun -pool batch6-head.priv.hmdc.harvard.edu -constraint '( JobStatus == 2)' -format '%s ' User -format '%d ' RequestCpus -format '%d \n' RequestMemory |perl -e 'while (<>) { @f = split(/\s+/, $_); $sum{$f[0]}{cpu} += $f[1]; $sum{$f[0]}{mem} += $f[2]; } printf( "%15s %4s %s\n", "USER", "CPUS", "MEM_GB" ); foreach $u ( sort(keys(%sum)) ) { $us = $u; $us =~ s/\@hmdc\.harvard\.edu//; printf( "%15s %4d %d\n", $us, $sum{$u}{cpu}, $sum{$u}{mem} / 1024 ); }'
        fi
        if [  "$CLUSTER" == "all" ]; then
            echo
        fi
        if [ "$CLUSTER" == "interactive" -o "$CLUSTER" == "all" ]; then
            ${FIGLET} -f small 'Interactive Cluster' 2> /dev/null|| echo "==== Interactive Cluster ===="
            /usr/bin/condor_q -global -currentrun -pool cod6-head.priv.hmdc.harvard.edu -constraint '( JobStatus == 2)' -format '%s ' User -format '%d ' RequestCpus -format '%d \n' RequestMemory |perl -e 'while (<>) { @f = split(/\s+/, $_); $sum{$f[0]}{cpu} += $f[1]; $sum{$f[0]}{mem} += $f[2]; } printf( "%15s %4s %s\n", "USER", "CPUS", "MEM_GB" ); foreach $u ( sort(keys(%sum)) ) { $us = $u; $us =~ s/\@hmdc\.harvard\.edu//; printf( "%15s %4d %d\n", $us, $sum{$u}{cpu}, $sum{$u}{mem} / 1024 ); }'
        fi
    ;;
esac

