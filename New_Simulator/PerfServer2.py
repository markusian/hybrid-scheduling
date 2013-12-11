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
PERIODIC_LOADS = [0.20, 0.4]
APERIODIC_EXECUTION_TIME = [0.02, 0.04]
NUM_HYPERPERIODS = 1 #number of hyperperiods to consider
MAX_TOTAL_LOAD = 0.60 #maximum total load considered
MIN_AP_LOAD = 0.01 #minimum aperiodic load
NUM_POINTS = 10 # number of points to consider for the aperiodic load range


def simulationLoop(server, capacity, period, scaled, ex_time, int_time):
        s = Simulator()

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

        # Compute the average response time
        total = 0
        average = 0
        for i in s.statistics.instances:
            if i.type == Instance.SOFT:
                average = float(average * total +
                          (i.finish - i.arrival)) / float(total + 1)
                total += 1
        return average

res = dict()
start = time()
file = open(sys.argv[1], 'rb')
if len(sys.argv) > 2:
    NUM_HYPERPERIODS = int(sys.argv[2])
if len(sys.argv) > 3:
    MAX_TOTAL_LOAD = float(sys.argv[3])
data = json.load(file)
taskset = list()
periodics = data["periodics"]
for t in periodics:
    taskset.append(PeriodicTask(t["id"], t["wcet"], t["period"]))

print "PER_LOAD, APER_EXEC_TIME, UTIL_POL"
for p_load in PERIODIC_LOADS:
    res[p_load] = dict()

    # Scale the task set
    scaled = deepcopy(list(taskset))
    for t in scaled:
        t.wcet = t.wcet * p_load
        #why there was an int here?

    # Compute the execution time
    until = PeriodicTask.lcm(scaled)*NUM_HYPERPERIODS

    for ap_ex_time in APERIODIC_EXECUTION_TIME:
        res[p_load][ap_ex_time] = dict()
        res[p_load][ap_ex_time]['pol'] = dict()
        res[p_load][ap_ex_time]['def'] = dict()
        res[p_load][ap_ex_time]['bac'] = dict()


        # Compute variables for the server
        util = PollingServer.util(p_load)*1.0
        util_def = DeferrableServer.util2(p_load)*1.0

        period = min([t.period for t in scaled])
        capacity = util * period
        capacity_def = util_def * period

        print p_load, ap_ex_time, util, util_def

        if util_def <= 0 or util_def > 1.0:
            print "Error!!!! ", capacity_def
            raise Exception("Problem with deferrable server")

        # Compute variables for the aperiodic task
        ex_time = period * ap_ex_time

        APERIODIC_LOAD = linspace(MIN_AP_LOAD, MAX_TOTAL_LOAD-p_load, NUM_POINTS)
        print "APERIODIC LOADS: ", APERIODIC_LOAD

        for ap_load in APERIODIC_LOAD:
            int_time = ex_time / ap_load

            av = simulationLoop('polling', capacity, period, scaled, ex_time, int_time)
            res[p_load][ap_ex_time]['pol'][ap_load] = av

            av = simulationLoop('deferrable', capacity_def, period, scaled, ex_time, int_time)
            res[p_load][ap_ex_time]['def'][ap_load] = av

            av = simulationLoop('background', capacity, period, scaled, ex_time, int_time)
            res[p_load][ap_ex_time]['bac'][ap_load] = av






print "ELAPSED TIME: ",  time() - start
fi = open(OUTPUT_FOLDER + sys.argv[1].split('/')[-1].split('\\')[-1],'w')
json.dump(res,fi)
