#!/bin/sh

# ----------------------------------------------
# author: Jakub Krzywda, Umea University, Sweden
# email: jakub@cs.umu.se
# ----------------------------------------------

HOST= # the address of a physical server hosting virtual machines
USER= # the username at HOST with permissions to execute virsh commands
FREQ= # the desired CPU frequency of HOST
COOL_DOWN_POWER= # the power consumption of an idle HOST

./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
ssh $USER@$HOST "./unpinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 4 -f $FREQ -i unpinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 4 -f $FREQ -i unpinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 4 -f $FREQ -i unpinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

ssh $USER@$HOST "./pinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 4 -f $FREQ -i pinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 4 -f $FREQ -i pinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 4 -f $FREQ -i pinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

ssh $USER@$HOST "virsh shutdown WikiImage_German31"

ssh $USER@$HOST "./unpinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 3 -f $FREQ -i unpinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 3 -f $FREQ -i unpinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 3 -f $FREQ -i unpinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

ssh $USER@$HOST "./pinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 3 -f $FREQ -i pinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 3 -f $FREQ -i pinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 3 -f $FREQ -i pinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

ssh $USER@$HOST "virsh shutdown WikiImage_German33"
sleep 120

ssh $USER@$HOST "./unpinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 2 -f $FREQ -i unpinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 2 -f $FREQ -i unpinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 2 -f $FREQ -i unpinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

ssh $USER@$HOST "./pinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 2 -f $FREQ -i pinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 2 -f $FREQ -i pinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 2 -f $FREQ -i pinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

ssh $USER@$HOST "virsh shutdown WikiImage_German34"
sleep 120

ssh $USER@$HOST "./unpinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 1 -f $FREQ -i unpinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 1 -f $FREQ -i unpinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 1 -f $FREQ -i unpinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

ssh $USER@$HOST "./pinVMs8cores.sh"

sleep 10
./test-horizontal-performance.sh -c 1 -f $FREQ -i pinned_memcached_0
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 1 -f $FREQ -i pinned_memcached_1
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
./test-horizontal-performance.sh -c 1 -f $FREQ -i pinned_memcached_2
./tests-multi-cores-util-power-cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER
