#!/usr/bin/env python

'''Workload generator for MediaWiki'''

import sys
import getopt
import time
import requests
import math
import traceback
import random
import multiprocessing as mp
import numpy as np
from __main__ import traceback
from itertools import chain


'''
    Created on Jun 1, 2015
    Last modified on Apr 2, 2016
'''

__authors__ = "Ahmed Ali, Jakub Krzywda"
__copyright__ = "Copyright 2016, Umea University"
__credits__ = ["Ahmed Ali", "Jakub Krzywda"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Jakub Krzywda"
__email__ = "jakub@cs.umu.se"
__status__ = "Prototype"


HOST='http://p08.ds.cs.umu.se:8112/gw'
LINK='/index.php/Porsche_935'

host=HOST

DROP_REQUESTS_AFTER=10
 
fn = './MultiProcessedResponseTime.out'

def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter

def worker(j,q):
    ''' simulates long running process'''
    t1=time.time()
    r = requests.get('%s%s'%(host,LINK), timeout=DROP_REQUESTS_AFTER)
    t2=time.time()
    
    RT=t2-t1
    out=str(RT)+"  "+str(j)+"   "+str(t1)+"   ",r.status_code
    q.put(out)
    return out
 
def listener(q):
    '''listens for messages on the q, writes to file. '''
 
    f = open(fn, 'wb') 
    while 1:
        m = q.get()
        if m == 'kill':
            f.write('killed')
            break
        f.write(str(m) + '\n')
        f.flush()
    f.close()
 
def main(argv):
    # default configuration
    workloadProfile = 'constant'
    constReqNumber = 1
    maxReqNumber = 10
    repAtLevel = 2
    stepSize = 1
    distribution = 'evenly_spread'
    requestPoolSize = 200

    try:
      opts, args = getopt.getopt(argv,"hp:n:m:s:r:d:w:",["profile=","number=","max=","step=","rep=","distribution=","workers="])
    except getopt.GetoptError:
      print 'WikipediaGenerator.py -p <profile> -n <req per sec for constant profile> -m <max req per sec for step profile> -s <step size> -r <repetitions per level> -d <distribution> -w <number of workers>'
      print '  profiles: constant, step'
      print '  distributions: concurrent, evenly_spread, poissonian' 
      sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
         print 'WikipediaGenerator.py -p <profile> -n <req per sec for constant profile> -m <max req per sec for step profile> -s <step size> -r <repetitions per level> -d <distribution> -w <number of workers>'
         print '  profiles: constant, step'
         print '  distributions: concurrent, evenly_spread, poissonian'
         sys.exit()
      elif opt in ("-p", "--profile"):
         workloadProfile = arg
      elif opt in ("-n", "--number"):
         constReqNumber = int(arg)
      elif opt in ("-m", "--max"):
         maxReqNumber = int(arg)
      elif opt in ("-s", "--step"):
         stepSize = int(arg)
      elif opt in ("-r", "--rep"):
         repAtLevel = int(arg)
      elif opt in ("-d", "--distribution"):
         distribution = arg
      elif opt in ("-w", "--workers"):
         requestPoolSize = int(arg)

    if workloadProfile == 'constant':
       print 'Constant workload profile with', constReqNumber, 'requests per second repeated', repAtLevel, 'times'
       NUMBER_OF_REQUESTS=[constReqNumber]*repAtLevel
    elif workloadProfile == 'step':
       print 'Step workload profile from 0 to', maxReqNumber, 'requests per second with a step of', stepSize, 'and', repAtLevel, 'repetitions at each level'
       NUMBER_OF_REQUESTS=list(chain(*([x]*repAtLevel for x in xrange(0,maxReqNumber,stepSize))))
    else:
       print workloadProfile, 'is not an acceptable value of the workload profile'
       print 'Try one of the following profiles: constant, step'
       sys.exit(2)

    if distribution in ("concurrent", "evenly_spread", "poissonian"):
       print 'Request generation mode (distribution):', distribution
    else:
       print '"', distribution, '" is not an acceptable value of the distribution'
       print 'Try one of the following distributions: concurrent, evenly_spread, poissonian'
       sys.exit(2)

    print 'Max number of requests in the system (workers):', requestPoolSize

    SLEEP=1

    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(requestPoolSize)
 
    #put listener to work first
    watcher = pool.apply_async(listener, (q,))

    if distribution == 'poissonian':
        TimeOfReq = []
        for i in range(stepSize, maxReqNumber, stepSize):
            for j in range(repAtLevel):
                summer = 0
                for k in range(1, i):
                    const = nextTime(i)
                    TimeOfReq += [const]
                    summer += const
                if summer<1:
                    TimeOfReq[-1] = 1 - summer + TimeOfReq[-1]
#               elif summer>1:
#                   x[-1]=1-summer-x[-1]

    jobs = []
    #fire off workers
    k=0
    for i in NUMBER_OF_REQUESTS:
        print i

        if i == 0:
            time.sleep(SLEEP)
        else:
            if distribution == 'concurrent':
                time.sleep(SLEEP)
            if distribution == 'evenly_spread':
                SLEEP_DIVIDED = SLEEP / float(i)

        for j in range(1, i+1):
            if distribution == 'evenly_spread':
                time.sleep(SLEEP_DIVIDED)
            if distribution == 'poissonian':
                time.sleep(TimeOfReq[k])
                k += 1
            job = pool.apply_async(worker, (i,q))
            jobs.append(job)        
 
    # collect results from the workers through the pool result queue
    for job in jobs: 
        try:
            job.get()
        except :
          print "There was an error"
          print traceback.print_exc()
          continue
  
    #now we are done, kill the listener
    q.put('kill')
    pool.close()
 
if __name__ == "__main__":
   main(sys.argv[1:])
