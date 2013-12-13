# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:49:31 2013

@author: ferdinando
"""
import json
from pprint import pprint
from collections import OrderedDict
import matplotlib.pyplot as plt

OUTPUT_FOLDER = "results_q3/"
IMAGES_FOLDER = OUTPUT_FOLDER + "images/"

PERIODIC_LOADS = [0.20, 0.40]
PERIOD_PERC = [0.5, 1, 2, 4]
PERIODS = [18*i for i in PERIOD_PERC]
markers = {9:'-+',18:'-s',36:'-+',72:'-*'}

def getxy(li,pload):
    ordered = OrderedDict(sorted(li.items()))

    x = [float(i) for i in ordered.keys()]
    y = [float(i) for i in ordered.values()]
    return x,y

ps = {0.20: 0.637 , 0.40:0.341}
ds = {0.20: 0.540, 0.40:0.256}


indexes = [1]

for i in indexes:
    fi = open(OUTPUT_FOLDER + "ts" + str(i) + ".json")
    di = json.load(fi)


    for pload in PERIODIC_LOADS:
        plt.figure()
        fa = di[str(pload)]

        for period in PERIODS:
            li_def = fa['def'][str(period)]
            x_def, y_def = getxy(li_def,pload)

            #plt.figure()

            #plt.yscale('log')
            plt.plot(x_def,y_def,markers[period],label="Period = {0}".format(int(period)))

        plt.xlim(min(x_def),max(x_def))
        plt.ylabel("Average Aperiodic Response Time")
        plt.xlabel("Average Aperiodic Load")
        plt.title(r'Performance against server period - DS     $U_p = {0}$'.format(pload))
        plt.legend(loc = 'upper left')
        name = "ts" + str(i) + "_" + str(pload)
        plt.savefig(IMAGES_FOLDER + name  + "def.pdf")
        plt.savefig(IMAGES_FOLDER + name  + "def.png")


    for pload in PERIODIC_LOADS:
        plt.figure()
        fa = di[str(pload)]

        for period in PERIODS:
            li_def = fa['pol'][str(period)]
            x_def, y_def = getxy(li_def,pload)

            #plt.figure()

            #plt.yscale('log')
            plt.plot(x_def,y_def,markers[period],label="Period = {0}".format(int(period)))

        plt.xlim(min(x_def),max(x_def))
        plt.ylabel("Average Aperiodic Response Time")
        plt.xlabel("Average Aperiodic Load")
        plt.title(r'Performance against server period - PS     $U_p = {0}$'.format(pload))
        plt.legend(loc = 'upper left')
        name = "ts" + str(i) + "_" + str(pload)
        plt.savefig(IMAGES_FOLDER + name  + "pol.pdf")
        plt.savefig(IMAGES_FOLDER + name  + "pol.png")


