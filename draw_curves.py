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
import numpy as np
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

def mean(min, max, d1):
    mean_result = 0
    sum =0
    angles = d1.keys()
    for angle in angles:
        if angle > min and angle < max:
            sum = sum + 1
            mean_result = mean_result + d1[angle]
    if sum !=0:
        mean_result = mean_result/sum
    else:
        mean_result = 0
    return mean_result

def median(min, max, d1,p):
    angles = d1.keys()
    list_median = []
    for angle in angles:
        if angle > min and angle < max:
            list_median.append(d1[angle])
    # list_median = sorted(list_median)
    return np.percentile(np.array(list_median),p)

def update_dict(step, d1,p):
    angles = d1.keys() # get angles
    angles = sorted(angles)
    d2 = dict()
    for angle in angles:
        angle_value = round(angle)
        if angle_value%step == 0:
           #d2.update({ str(angle_value-step) + "<->" + str(angle_value) : median(angle_value - step, angle_value, d1)})
           d2.update({ str(angle_value) : median(angle_value - step, angle_value, d1,p)})
    return d2

def draw_curves(X, Y):
    df = pandas.read_csv('data_aws.csv')
    trackers = df["tracker"].tolist()
    unique_trackers = set(trackers)
    print(list(unique_trackers))
    unique_trackers = sorted(unique_trackers)
    images = []
    for tc in list(unique_trackers):
        print(tc)
        step = 15
        dmed = dict()
        dproved =dict()
        dpossible = dict()
        tc_data = df.loc[df['tracker'] == tc]
        Xcurrent_angles = tc_data[X].tolist()
        Ylatence = tc_data[Y].tolist()
        Ylatence2 = list()
        Xcurrent_angles2 = list()
        #Ylatence = [0 if math.isnan(x) else x for x in Ylatence] # nan = 0
        #Ylatence = [x for x in Ylatence if math.isnan(x) == False]  # supprimer nan
        for x in range(len(Ylatence)):
            val = Ylatence[x]
            if math.isnan(val) == False:
                Ylatence2.append(val)
                Xcurrent_angles2.append(Xcurrent_angles[x])

        for i in range(len(Xcurrent_angles2)):
            dmed.update({Xcurrent_angles2[i] : Ylatence2[i]}) # {angle : latence}
            dproved.update({Xcurrent_angles2[i]: Ylatence2[i]})  # {angle : latence}
            dpossible.update({Xcurrent_angles2[i]: Ylatence2[i]})  # {angle : latence}
        print(dpossible)
        dmed = update_dict(step, dmed,50)
        dproved = update_dict(step, dproved,90)
        dpossible = update_dict(step, dpossible, 10)
        x = list(dmed.keys())
        plt.plot(x,dmed.values(),x,dproved.values(),x, dpossible.values())
        plt.gca().legend(('median','P90','P10'))
        plt.xlabel('angle')
        src = 'courbe_' + tc + '.png'
        if Y == 'zigbee_rx_signal_strength':
            plt.ylabel('reception')
            plt.ylim([0,100])
            plt.savefig('template/rec/courbe_' + tc + '.png')
        else:
            plt.ylabel('latence')
            plt.ylim([0, 0.80])
            plt.savefig('template/lat/courbe_' + tc + '.png')
        images.append(str(src))
        plt.show()
    print(images)
    return images

def draw_all_curves():
    Y = ['zigbee_last_message_txrx', 'zigbee_rx_signal_strength']
    X = 'current_angle'
    lat_images = []
    rec_images = []
    for y in Y:
        if y == 'zigbee_last_message_txrx':
            lat_images = draw_curves(X, y)
        else:
            rec_images = draw_curves(X, y)
    all_img = lat_images + rec_images
    return  all_img


env = Environment(loader=FileSystemLoader("template"))
template = env.get_template("mytemplate.html.j2")
output = template.render(images=draw_all_curves())
with io.open("index2.html", "w") as file_point:
    file_point.write(output)
###############################################################
#geopy