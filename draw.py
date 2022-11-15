import math
import numpy as np
import pandas
import statistics as stat
import matplotlib.pyplot as plt
import pylab
from numpy import polyfit
from scipy.stats import linregress
from scipy.optimize import curve_fit
import io

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
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

def draw(X, Y):
    df = pandas.read_csv('data_aws.csv')
    trackers = df["tracker"].tolist()
    unique_trackers = set(trackers)
    print(list(unique_trackers))
    images = []
    for tc in list(unique_trackers):
        print(tc)
        d = dict()
        tc_data = df.loc[df['tracker'] == tc]
        Xcurrent_angles = tc_data[X].tolist()
        Y_ = tc_data[Y].tolist()
        Y_ = [0 if math.isnan(x) else x for x in Y_] # nan = 0
        for i in range(len(Xcurrent_angles)):
            d.update({Xcurrent_angles[i] : Y_[i]}) # {angle : latence}
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
        src = 'courbe_' + tc + '.png'
        if Y == 'zigbee_rx_signal_strength':
            plt.ylabel('reception')
            plt.savefig('template/rec/courbe_' + tc + '.png')
        else:
            plt.ylabel('latence')
            plt.savefig('template/lat/courbe_' + tc + '.png')
        images.append(str(src))
        plt.show()
    print(images)
    return images

def draw_all():
    Y = ['zigbee_last_message_txrx', 'zigbee_rx_signal_strength']
    X = 'current_angle'
    lat_images = []
    rec_images = []
    for y in Y:
        if y == 'zigbee_last_message_txrx':
            lat_images = draw(X,y)
        else:
            rec_images = draw(X,y)
    all_img= lat_images+rec_images
    return  all_img



#draw('current_angle', 'zigbee_last_message_txrx')
# Y = ['zigbee_last_message_txrx', 'zigbee_rx_signal_strength']
# X = 'current_angle'
env = Environment(loader=FileSystemLoader("template"))
template = env.get_template("mytemplate.html.j2")
output = template.render(images=draw_all()
    , hello="world")
with io.open("index.html", "w") as file_point:
    file_point.write(output)
###############################################################
