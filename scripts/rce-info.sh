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
CONSTRAINT="$(echo ${_CONDOR_ENTITLEMENTS}|grep kennedy >/dev/null 2>&1 && echo "${_CONSTRAINT}" || echo "${_CONSTRAINT} && ! regexp(\"ksg\", Machine) && ! regexp (\"edlabs\", Machine) ")"

# Main

case "$TYPE" in
    available)
${FIGLET} -f small 'RCE Cluster' 2> /dev/null|| echo "==== RCE Cluster ===="
cat <<EOF|fold -w 70 -s

This displays the amount of cpu(s) and memory in gigabytes available for use on each host in our cluster. If you're submitting an RCE powered job, make sure that the amount of memory and cpu(s) requested fall within available resources on at least one of the cluster hosts listed below. Otherwise, your job will remain in the queue until enough resources become available.

EOF
(echo CpusAvailable MemoryAvailable\(gb\) Machine; condor_status -constraint "regexp(\"^slot1@\",Name) && ${CONSTRAINT}" -format "%d " Cpus -format "%d " Memory/1024 -format "%s\n" "regexps(\"^slot1@(.*)\", Name, \"\\1\")" |sort -n -r)|column -t
    ;;
    used)
      ${FIGLET} -f small 'RCE Cluster' 2> /dev/null|| echo "==== RCE Cluster ===="
      /usr/bin/condor_q -global -currentrun -constraint '( JobStatus == 2)' -format '%s ' User -format '%d ' RequestCpus -format '%d \n' RequestMemory |perl -e 'while (<>) { @f = split(/\s+/, $_); $sum{$f[0]}{cpu} += $f[1]; $sum{$f[0]}{mem} += $f[2]; } printf( "%15s %4s %s\n", "USER", "CPUS", "MEM_GB" ); foreach $u ( sort(keys(%sum)) ) { $us = $u; $us =~ s/\@hmdc\.harvard\.edu//; printf( "%15s %4d %d\n", $us, $sum{$u}{cpu}, $sum{$u}{mem} / 1024 ); }'
    ;;
esac
