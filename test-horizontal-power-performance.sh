#!/bin/bash

# ----------------------------------------------
# author: Jakub Krzywda, Umea University, Sweden
# email: jakub@cs.umu.se
# ----------------------------------------------

host= # address of the physical machine hosting virtual machines
user= # user at the physical machine with permisions to
address= # address for measuring the power consumption
vms=1 # number of virtual machines
frequency=2.1 # cpu frequency
measurement_duration=440 # measurement duration [in seconds]: 40 [steps/levels] * 10 [repetitions at each step/level] + 40 [safe margin]
node=p05 # name of physical machine for logging purposes
        
while [ "$1" != "" ]; do
    case $1 in
        -i | --id )             shift
                                experiment_id=$1
                                ;;
        -v | --vms )          shift
                                vms=$1
                                ;;
        -f | --freq )           shift
                                frequency=$1
    esac
    shift
done

# set the CPU frequency of the physical machine
ssh $user@$host "for j in \$(seq 0 31); do sudo cpufreq-set -c \$j -f $frequency''GHz ; done"

sleep 5

# get the CPU frequency of the physical machine
freq_m=`ssh $user@$host 'lscpu' | awk '/^CPU MHz/{print $3}'`

# start workload generator
python WikipediaGenerator.py -p evenly_spread -m 200 -s 5 -r 10 -w 200 &

# measurement loop
start_time=$SECONDS
while [ $SECONDS -lt $((start_time + measurement_duration)) ]
do
  snmpget -c public -v 2c bigmama.ds.cs.umu.se $address | awk -v pm="$node" -v freq="$freq_m" -v vms="$vms" -v time="$((SECONDS - beginning))" -v percentage="$percentage" -v iteration="$i" -v temperature="$temperature" '//{print pm";"freq";"vms";"$4";"time";"percentage";"iteration temperature}' >> tests/dvfs-power-performance_${vms}_${frequency}_${experiment_id}.csv
  sleep 1
done

# save temporary log file
mv MultiProcessedResponseTime.out tests/horizontal-scaling-power-performance_${vms}_${frequency}_${experiment_id}_MultiProcessedResponseTime.out