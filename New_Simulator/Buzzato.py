from Task import PeriodicTask, AperiodicTask
from Simulator import Simulator
from Server import PollingServer

periods = [877, 458, 344, 1065, 817, 696, 698, 344, 215, 283]
wcet = [i * 0.069 for i in periods]

# Building tasks set
taskset = list()
for i in range(0,10):
    t = PeriodicTask("H" + str(i), wcet[i], periods[i])
    taskset.append(t)

for load in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
    # Try the simulator
    s = Simulator()

    server_period = min([t.period for t in taskset])
    server_capacity = server_period * 0.248
    s.server = PollingServer(server_capacity, server_period)

    for t in taskset:
        s.tasks.append(t)

    # Building the aperiodic task
    interrarival = 18
    computation = load * interrarival
    t = AperiodicTask("S", computation, interrarival)
    
    s.tasks.append(t)

    until = PeriodicTask.lcm(taskset)
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

    print str(load) + ":" + str(average)
