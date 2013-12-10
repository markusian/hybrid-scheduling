import sys
import json
from numpy import arange
from Task import PeriodicTask, AperiodicTask
from Server import PollingServer
from Simulator import Simulator
from Instance import Instance

PERIODIC_LOADS = [0.20, 0.5]
APERIODIC_EXECUTION_TIME = [0.1, 0.01]

res = dict()

# TODO : Load the task set
file = open(sys.argv[1], 'rb')
data = json.load(file)
taskset = list()
periodics = data["periodics"]
for t in periodics:
    taskset.append(PeriodicTask(t["id"], t["wcet"], t["period"]))

for p_load in PERIODIC_LOADS:
    res[str(p_load)] = dict()
    for ap_ex_time in APERIODIC_EXECUTION_TIME:
        res[str(p_load)][str(ap_ex_time)] = dict()
        # Scale the task set
        scaled = list(taskset)
        for t in scaled:
            t.wcet = int(t.wcet * p_load)

        # Compute variables for the server
        util = PollingServer.util(p_load)

        period = min([t.period for t in scaled])
        capacity = util * period

        # Compute variables for the aperiodic task
        ex_time = period * ap_ex_time

        APERIODIC_LOAD = arange(p_load, 0.9, 0.1)

        for ap_load in APERIODIC_LOAD:
            int_time = ex_time / ap_load

            s = Simulator()

            # Set the server
            s.server = PollingServer(capacity, period)

            # Load the taskset
            for t in scaled:
                s.tasks.append(t)

            # Create the aperiodic task
            ap = AperiodicTask("Soft", ex_time, int_time)
            s.tasks.append(ap)

            # Compute the execution time
            until = PeriodicTask.lcm(scaled)

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

            res[str(p_load)][str(ap_ex_time)][str(ap_load)] = average

print json.dumps(res)
