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

# Only include ksg/edlabs/nsaph machines if user has matching entitlement
#  (HMDC profile sets _CONDOR_ENTITLEMENTS at login)
CONDOR_ENTITLEMENTS=`echo ${_CONDOR_ENTITLEMENTS} |sed -e 's/[,"]/ /g'`
_CONSTRAINT='regexp("^slot1@",Name) && Start == true && RemoteOwner =?= undefined'
_NOKSG=' && ! regexp("ksg", Machine)'
_NOEDLABS=' && ! regexp ("edlabs", Machine)'
_NONSAPH=' && ! regexp ("nsaph", Machine)'
for title in ${CONDOR_ENTITLEMENTS}; do
    case "$title" in
        kennedy)
            _NOKSG=''
        ;;
        edlabs)
            _NOEDLABS=''
        ;;
        nsaph)
            _NONSAPH=''
        ;;
    esac
done
CONSTRAINT="${_CONSTRAINT} ${_NOKSG} ${_NOEDLABS} ${_NONSAPH}"

# Main

case "$TYPE" in
    available)
${FIGLET} -f small 'RCE Cluster' 2> /dev/null|| echo "==== RCE Cluster ===="
cat <<EOF|fold -w 70 -s

This displays the amount of cpu(s) and memory in gigabytes available for use on each host in our cluster. If you're submitting an RCE powered job, make sure that the amount of memory and cpu(s) requested fall within available resources on at least one of the cluster hosts listed below. Otherwise, your job will remain in the queue until enough resources become available.

EOF
(echo CpusAvailable MemoryAvailable\(gb\) Machine; condor_status -constraint "${CONSTRAINT}" -format "%d " Cpus -format "%d " Memory/1024 -format "%s\n" "regexps(\"^slot1@(.*)\", Name, \"\\1\")" |sort -n -r)|column -t
    ;;
    used)
      ${FIGLET} -f small 'RCE Cluster' 2> /dev/null|| echo "==== RCE Cluster ===="
      #/usr/bin/condor_q -global -currentrun -constraint '( JobStatus == 2)' -format '%s ' User -format '%d ' RequestCpus -format '%d ' RequestMemory -format '%d ' MemoryUsage -format '\n' none|\
      /usr/bin/condor_q -global -currentrun -constraint '( JobStatus == 2)' -format '%s ' User -format '%d ' RequestCpus -format '%d ' RequestMemory -format '%d ' ResidentSetSize_RAW -format '\n' none|\
	perl -e 'while (<>) { 
	  @f = split(/\s+/, $_); 
	  $us = $f[0]; 
	  $us =~ s/\@hmdc\.harvard\.edu//;  
	  $sum{$us}{cpu} += $f[1]; 
	  $sum{$us}{requestmem} += $f[2]; 
	  $sum{$us}{usedmem} += ( $f[3] / 1024 ); 
	} 
 
	foreach $u ( keys(%sum) ) {
	  $sum{$u}{deltamem} = ($sum{$u}{requestmem} - $sum{$u}{usedmem} )
	}
	printf( "%45s\n", "MEMORY (IN GB)" );
	printf( "%15s   %4s   %s   %s   %s\n", "USER", "CPUS", "REQUESTED", "USED","UNUSED" ); 
	foreach $u ( sort(keys(%sum)) ) { 
	  printf( "%15s %6d %11d %6d %8d\n", $u, $sum{$u}{cpu}, $sum{$u}{requestmem} / 1024, $sum{$u}{usedmem} / 1024 , $sum{$u}{deltamem} / 1024 )
	}'
    ;;
    *)
        echo "Unrecognized type: $TYPE"
        ;;
esac

