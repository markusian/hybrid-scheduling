import sys
import json
from numpy import arange, linspace
from Task import PeriodicTask, AperiodicTask
from Server import PollingServer, DeferrableServer, BackgroundServer
from Simulator import Simulator
from Instance import Instance
from copy import deepcopy
from time import time

OUTPUT_FOLDER = "results_q1/"
filename = '../CaseStudies/ts13.json'

PERIODIC_LOADS = [0.20, 0.40]
MIN_AP_LOAD = 0.01 #minimum aperiodic load
NUM_POINTS = 9 # number of points to consider for the aperiodic load range
MAX_AP_LOAD = 0.20
until = 500000


def computeAverage(filename):
    fi = open(filename, 'r')
    somma = 0.0
    n = 0.0
    lines = fi.readlines()[3:-3]
    #print lines, filename
    for line in lines:
        line_split = line.split('|')
        if line_split[1].strip() == 'SOFT':
            n = n+1
            finish = float(line_split[4])
            start = float(line_split[2])
            somma = somma + (finish-start)
    return somma/n, 0





def simulationLoop(server, capacity, period, scaled, ex_time, int_time):
        name = server + ".csv"
        s = Simulator(stats = name)

        # Set the server
        if server == 'polling':
            s.server = PollingServer(capacity, period)
        elif server == 'deferrable':
            s.server = DeferrableServer(capacity, period)
        else:
            s.server = BackgroundServer()


        # Load the taskset
        for t in scaled:
            s.tasks.append(t)

        # Create the aperiodic task
        ap = AperiodicTask("Soft", ex_time, int_time)
        s.tasks.append(ap)


        # RUUUUUUUUN !!!
        s.init(until)
        s.run()


        return computeAverage(name)

for i in range(1,11):
    print '\n'

    print '-'*60
    print "TASK SET N. " + str(i)
    print '-'*60, '\n'

    filename = '../CaseStudies/ts'+ str(i) +'.json'

    res = dict()
    start = time()
    file = open(filename, 'rb')
    data = json.load(file)
    taskset = list()
    periodics = data["periodics"]
    for t in periodics:
        taskset.append(PeriodicTask(t["id"], t["wcet"], t["period"]))

    for p_load in PERIODIC_LOADS:
        res[p_load] = dict()

        # Scale the task set
        scaled = deepcopy(list(taskset))
        for t in scaled:
            t.wcet = t.wcet * p_load

        # Compute the execution time
        #until = PeriodicTask.lcm(scaled)*NUM_HYPERPERIODS
        #print "HYPERPERIOD", PeriodicTask.lcm(scaled)
        res[p_load]['pol'] = dict()
        res[p_load]['def'] = dict()
        res[p_load]['bac'] = dict()

        # Compute variables for the server
        util = PollingServer.util(p_load)
        util_def = DeferrableServer.util2(p_load)

        period = 18
        #period = min([t.period for t in scaled])*1
        capacity = util * period
        capacity_def = util_def * period

        print "\nPERIODIC LOAD: " + str(p_load),
        print "\tUTIL POLLING: " + str(util),
        print "\tUTIL DEFERRABLE: " + str(util_def)
        print "*"*40

        APERIODIC_LOAD = linspace(MIN_AP_LOAD, MAX_AP_LOAD, NUM_POINTS)

        for ap_load in APERIODIC_LOAD:
            int_time = 18
            ex_time = int_time * ap_load

            print "\nAPERIODIC LOAD: " + str(ap_load),
            print "\t\tEXECUTION TIME: " + str(ex_time)
            avp = simulationLoop('polling', capacity, period, scaled, ex_time, int_time)
            res[p_load]['pol'][ap_load] = avp[0]

            avd = simulationLoop('deferrable', capacity_def, period, scaled, ex_time, int_time)
            res[p_load]['def'][ap_load] = avd[0]

            avb = simulationLoop('background', capacity, period, scaled, ex_time, int_time)
            res[p_load]['bac'][ap_load] = avb[0]

            print "POL: " +str(avp[0]) + "\tDEF: " +str(avd[0]) + "\tBAC: " +str(avb[0])



    print "ELAPSED TIME: ",  time() - start
    fi = open(OUTPUT_FOLDER + filename.split('/')[-1].split('\\')[-1],'w')
    json.dump(res,fi)

