#!/bin/sh

# ----------------------------------------------
# author: Jakub Krzywda, Umea University, Sweden
# email: jakub@cs.umu.se
# ----------------------------------------------

HOST= # the address of a physical server hosting virtual machines
COOL_DOWN_POWER= # the power consumption of an idle HOST

./MediaWiki_single_experiment.sh -c 6 -f 1.2 -i memcache_intel_poisson_1
./cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

./MediaWiki_single_experiment.sh -c 6 -f 1.2 -i memcache_intel_poisson_2
./cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

./MediaWiki_single_experiment.sh -c 6 -f 1.2 -i memcache_intel_poisson_3
./cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

./MediaWiki_single_experiment.sh -c 6 -f 1.2 -i memcache_intel_poisson_4
./cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

./MediaWiki_single_experiment.sh -c 6 -f 1.2 -i memcache_intel_poisson_5
./cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

./MediaWiki_single_experiment.sh -c 6 -f 1.2 -i memcache_intel_poisson_6
./cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

./MediaWiki_single_experiment.sh -c 6 -f 1.2 -i memcache_intel_poisson_7
./cool-down.sh --node $HOST --cooldownpower $COOL_DOWN_POWER

