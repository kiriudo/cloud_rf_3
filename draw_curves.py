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

def median(min, max, d1):
    angles = d1.keys()
    list_median = []
    for angle in angles:
        if angle > min and angle < max:
            list_median.append(d1[angle])
    # list_median = sorted(list_median)
    return np.median(np.array(list_median))

def update_dict(step, d1):
    angles = d1.keys() # get angles
    angles = sorted(angles)
    d2 = dict()
    for angle in angles:
        angle_value = round(angle)
        if angle_value%step == 0:
           #d2.update({ str(angle_value-step) + "<->" + str(angle_value) : median(angle_value - step, angle_value, d1)})
           d2.update({ str(angle_value) : median(angle_value - step, angle_value, d1)})
    return d2

def draw_curves(X, Y):
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
        Ylatence = tc_data[Y].tolist()
        Ylatence = [0 if math.isnan(x) else x for x in Ylatence] # nan = 0
        for i in range(len(Xcurrent_angles)):
            d.update({Xcurrent_angles[i] : Ylatence[i]}) # {angle : latence}
        d = update_dict(15, d)
        y = list(d.values())
        #x = range(len(y))
        x = list(d.keys())
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
output = template.render(images=draw_all_curves()
    , hello="world")
with io.open("index2.html", "w") as file_point:
    file_point.write(output)
###############################################################
#geopy