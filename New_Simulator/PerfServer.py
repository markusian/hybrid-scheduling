from Simulator import Simulator
from Task import PeriodicTask, AperiodicTask
from Server import BackgroundServer, PollingServer
from Instance import Instance

AP_computation = 5
P_loads = [0.25, 0.5]
AP_loads = [0.01, 0.1]
tasksets = [[PeriodicTask("HARD", 1, 3), 
             PeriodicTask("HARD", 1, 4), 
             PeriodicTask("HARD", 1, 6)]]

for taskset in tasksets:
    for ap_load in AP_loads:
        for p_load in P_loads:
            averages = list()
            for i in range(10):
                s = Simulator()
                
                # Set the server
                s.server = PollingServer(3, PollingServer.util(3))

                # Scale the taskset
                scaled = list(taskset)
                for t in scaled:
                    t.wcet = int(t.wcet * p_load)
                    s.tasks.append(t)

                # Compute the aperiodic task
                ap = AperiodicTask("Soft",
                                   AP_computation,
                                   AP_computation / ap_load)
                s.tasks.append(ap)

                # Compute the execution time
                # (100 times LCM)
                until = PeriodicTask.lcm(scaled) * 10
                print "Init ..."
                s.init(until)
                print "Run !"
                s.run()

                # Compute the average response time
                total = 0
                average = 0
                for i in s.statistics.instances:
                    if i.type == Instance.SOFT:
                        average = float(average * total + 
                                  (i.finish - i.arrival)) / float(total + 1)
                        total += 1

                averages.append(average)
            print sum(averages) / len(averages)
