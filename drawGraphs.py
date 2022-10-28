import math
import numpy as np
import pandas
import statistics as stat
import matplotlib.pyplot as plt
import pylab
from numpy import polyfit
from scipy.stats import linregress
from scipy.optimize import curve_fit
def moyx(min,max,d1):
    n = 0
    i =0
    l = d1.keys()
    for el in l:
        if el > min and el < max:
            i = i+1
            n = n + d1[el]
    if i !=0:
        n = n/i
    else:
        n =0
    return n

def moydict(step,d1):
    l = d1.keys()
    d2 = dict()
    for i in l:
        n = round(i)
        if n%step == 0:
           d2.update({ str(n-step) + "<->" + str(n) : moyx(n-step,n,d1) })
    return d2

def func(x, a, b, c):
    return a*x**2 + b * x+ c

def draw():
    df = pandas.read_csv('data_aws.csv')
    trackers = df["tracker"].tolist()
    unique_trackers = set(trackers)
    print(list(unique_trackers))

    for tc in list(unique_trackers):
        print(tc)
        d = dict()
        tc_data = df.loc[df['tracker'] == tc]
        Xcurrent_angles = tc_data['current_angle'].tolist()
        Yzigbee_last_message_txrx = tc_data["zigbee_last_message_txrx"].tolist()
        Yzigbee_last_message_txrx = [0 if math.isnan(x) else x for x in Yzigbee_last_message_txrx] # nan = 0
        for i in range(len(Xcurrent_angles)):
            d.update({Xcurrent_angles[i] : Yzigbee_last_message_txrx[i]}) # {angle : latence}
        d = moydict(10,d)
        y = list(d.values())
        x = range(len(y))
        # popt, pcov = curve_fit(func, x, l)
        # slope,intercept, *other = linregress(x =x ,y = l )
        #fitline = slope * range(len(l)) + intercept
        #plt.plot(x,fitline)
        #plt.plot(x, func(x, *popt), 'r-', label="Modélisation")
        p4 = np.poly1d(np.polyfit(x, y, 6))
        xp = np.linspace(0, 10, 100)
        plt.plot(xp, p4(xp), c='r')
        plt.plot(x,y)
        plt.title('courbe du tc = '+tc)
        plt.xlabel('angle')
        plt.ylabel('latence')
        plt.show()
        break

draw()
