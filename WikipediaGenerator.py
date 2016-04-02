'''
Created on Jun 1, 2015
Last modified on Mar 29, 2016

@author: ahmeda, jakub
'''

import multiprocessing as mp
import time,requests,math,traceback
from __main__ import traceback
from itertools import chain
import numpy as np
import sys, getopt


HOST='http://p08.ds.cs.umu.se:8112/gw'
#HOST='http://p03.ds.cs.umu.se:8082/gw'
#LINK='/index.php/Liste_der_DIN-Normen'
LINK='/index.php/Porsche_935'

# Links=open("links.out",'r')
# links=Links.readlines()

# host='http://p18.ds.cs.umu.se:8112/gw'
host=HOST
# links=["%s%s"%(host,l.strip()) for l in links]

DROP_REQUESTS_AFTER=10

# workload=open('de.out','r')
# workload=workload.readlines()
# workload_German=[math.ceil(int(i.split()[2].strip())/3600) for i in workload]
# workload_ramp=range(1,101)
# print workload
# print r.text

 
fn = './MultiProcessedResponseTime.out'
# 
def worker(j,q):
    '''stupidly simulates long running process'''
#     for weights in ['uniform', 'distance']:
    t1=time.time()
    r = requests.get('%s%s'%(host,LINK), timeout=DROP_REQUESTS_AFTER)
    t2=time.time()
    
    RT=t2-t1
    out=str(RT)+"  "+str(j)+"   "+str(t1)+"   ",r.status_code
    q.put(out)
#    print "out", out
    return out
 
def listener(q):
    '''listens for messages on the q, writes to file. '''
 
    f = open(fn, 'wb') 
    while 1:
        m = q.get()
#	print "m", m
        if m == 'kill':
            f.write('killed')
            break
        f.write(str(m) + '\n')
        f.flush()
    f.close()
 
def main(argv):
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)

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

    #DROP_REQUESTS_AFTER=10
    SLEEP=1

    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(requestPoolSize)
 
    #put listener to work first
    watcher = pool.apply_async(listener, (q,))
 
     
    jobs = []
    #fire off workers
    for i in NUMBER_OF_REQUESTS:
        print i
        #if distribution == 'concurrent':
        time.sleep(SLEEP)
        #if distribution in ("evenly_spread", "poissonian"):
        #    if i > 0:
        #        SLEEP_DIVIDED = SLEEP / float(i)
        #    else:
        #        time.sleep(SLEEP)

        for j in range(1,i+1):
        #    if distribution in ("evenly_spread", "poissonian"):
        #        time.sleep(SLEEP_DIVIDED)
            job = pool.apply_async(worker, (i,q))
            jobs.append(job)        
 
    # collect results from the workers through the pool result queue
    for job in jobs: 
        try:
            job.get()
#	    print xxx
        except :
          print "There was an error"
          print traceback.print_exc()
          continue
  
    #now we are done, kill the listener
    q.put('kill')
    pool.close()
 
if __name__ == "__main__":
   main(sys.argv[1:])
