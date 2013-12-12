from Task import PeriodicTask, AperiodicTask
from Simulator import Simulator
from Server import PollingServer, BackgroundServer, DeferrableServer
from Instance import Instance

periods = [877, 458, 344, 1065, 817, 696, 698, 344, 215, 283]
wcet = [i * 0.069 for i in periods]

# Building tasks set
taskset = list()
for i in range(0,10):
    t = PeriodicTask("H" + str(i), wcet[i], periods[i])
    taskset.append(t)

#for load in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
for load in [0.05]:
    # Try the simulator
    s = Simulator(render = "results.svg")

    server_period = min([t.period for t in taskset])
    server_period = 18  
    #server_period = max([t.period for t in taskset]) + 1
    server_capacity = server_period * 0.248
    s.server = PollingServer(server_capacity, server_period)
    server_capacity = server_period * 0.239
    s.server = DeferrableServer(server_capacity, server_period)
    #s.server = DeferrableServer(server_period, server_period)
    #s.server = BackgroundServer()

    for t in taskset:
        s.tasks.append(t)

    # Building the aperiodic task
    interrarival = 18
    computation = load * interrarival
    t = AperiodicTask("S", computation, interrarival)
    
    s.tasks.append(t)

    until = PeriodicTask.lcm(taskset)
    until = 1000
    s.init(until)
    s.run()
