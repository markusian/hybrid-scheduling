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

PERIODIC_LOADS = [0.68]



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

        fa = di[str(pload)]
        li_def, li_pol, li_bac = fa['def'], fa['pol'], fa['bac']

        x_def, y_def = getxy(li_def,pload)
        x_pol, y_pol = getxy(li_pol,pload)
        x_bac, y_bac = getxy(li_bac,pload)

        ds_red = [float(y_def[j])/y_bac[j] for j in range(len(y_bac))]
        ps_red = [float(y_pol[j])/y_bac[j] for j in range(len(y_bac))]
        plt.figure()
        plt.ylabel("Average response time with respect to Background")
        plt.xlabel("Average aperiodic load")
        plt.title(r'$ U_p = 0.69$,  $U_{PS} = 24.8\%$,  $U_{DS} = 23.9\% $')
        #plt.yscale('log')
        plt.xlim(min(x_def),max(x_def))
        plt.plot(x_def,ds_red,'-s',label="Deferrable")
        plt.plot(x_pol,ps_red,'-o',label="Polling")
        plt.legend(loc='upper left')
        name = "validation_2"
        plt.savefig(IMAGES_FOLDER + name  + ".pdf")
        plt.savefig(IMAGES_FOLDER + name  + ".png")

