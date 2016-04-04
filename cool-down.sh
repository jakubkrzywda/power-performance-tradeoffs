#!/bin/sh

# ----------------------------------------------
# author: Jakub Krzywda, Umea University, Sweden
# email: jakub@cs.umu.se
# ----------------------------------------------

power_measurement_server= # address of the physical machine providing the power consumption measurements
node= # name of the default node for logging purposes
address= # default address for measuring the power consumption of the host
cooldown_power=85 # default power consumption (in Watts) that is consider as acceptable to start next experiment
results_directory=tests # directory to store experiment results

while [ "$1" != "" ]; do
    case $1 in
        -n | --node )           shift
                                node=$1
                                ;;
        -a | --address )        shift
                                address=$1
                                ;;
        -c | --cooldownpower )  shift
                                cooldown_power=$1
    esac
    shift
done

case $node in
  "node_1" )                  address=1.1.1.1.1
                                ;;
  "node_2" )                  address=2.2.2.2.2
                                ;;
  "node_3" )                  address=3.3.3.3.3
esac

date=`date "+%y_%m_%d-%H:%M:%S"` # date and time of beginning of experiment (used for naming the log files)

    # let physical machine to cool down (waiting till power consumption decreases to "acceptable" level)
    cool_down_start=$SECONDS
    while : ; do
      pc=`snmpget -c public -v 2c $power_measurement_server $address | awk -v pm="$node" '//{print $4}'` # measure power consumption
      echo $node";cooling_time;"$pc";"$((SECONDS - cool_down_start)) >> ${results_directory}/power-cooldown_$date.csv # store results to log
      if [ "$pc" -lt "$cooldown_power" ]; then
        break
      fi
      sleep 1 # time between measurements
    done
