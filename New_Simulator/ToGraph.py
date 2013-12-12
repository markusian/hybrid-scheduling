# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:49:31 2013

@author: ferdinando
"""
import json
from pprint import pprint
from collections import OrderedDict
import matplotlib.pyplot as plt

OUTPUT_FOLDER = "results_q1/"
IMAGES_FOLDER = OUTPUT_FOLDER + "images/"

PERIODIC_LOADS = [0.20, 0.40]
APERIODIC_EXECUTION_TIME = [0.02, 0.04]


def getxy(li,pload):
    ordered = OrderedDict(sorted(li.items()))

    x = [float(i) for i in ordered.keys()]
    y = [float(i) for i in ordered.values()]
    return x,y

indexes = [11]

for i in indexes:
    fi = open(OUTPUT_FOLDER + "ts" + str(i) + ".json")
    di = json.load(fi)

    for pload in PERIODIC_LOADS:
        for apex in APERIODIC_EXECUTION_TIME:

            fa = di[str(pload)][str(apex)]
            li_def, li_pol, li_bac = fa['def'], fa['pol'], fa['bac']

            x_def, y_def = getxy(li_def,pload)
            x_pol, y_pol = getxy(li_pol,pload)
            x_bac, y_bac = getxy(li_bac,pload)
            plt.figure()
            plt.ylabel("Average Aperiodic Response Time")
            plt.xlabel("Average Aperiodic Load")
            #plt.yscale('log')
            plt.xlim(min(x_def),max(x_def))
            plt.plot(x_def,y_def,'-s',label="Deferrable")
            plt.plot(x_pol,y_pol,'-o',label="Polling")
            plt.plot(x_bac,y_bac,'-+',label="Background")
            plt.legend()
            name = "ts" + str(i) + "_" + str(pload) + "_" + str(apex)
            plt.savefig(IMAGES_FOLDER + name  + ".pdf")
            plt.savefig(IMAGES_FOLDER + name  + ".png")

