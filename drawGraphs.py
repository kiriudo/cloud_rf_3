import math

import pandas
import matplotlib.pyplot as plt

def draw():
    df = pandas.read_csv('data_aws.csv')
    trackers = df["tracker"].tolist()
    unique_trackers = set(trackers)
    print(list(unique_trackers))
    d = dict()
    for tc in list(unique_trackers):
        print(tc)
        tc_data = df.loc[df['tracker'] == tc]
        Xcurrent_angles = tc_data['current_angle'].tolist()
        Yzigbee_last_message_txrx = tc_data["zigbee_last_message_txrx"].tolist()
        Yzigbee_last_message_txrx = [0 if math.isnan(x) else x for x in Yzigbee_last_message_txrx] # nan = 0
        for i in range(len(Xcurrent_angles)):
            d.update({Xcurrent_angles[i] : Yzigbee_last_message_txrx[i]}) # {angle : latence}
        print(d)
        print("Les angles du tc = ",tc,"-->",Xcurrent_angles)
        print("Latence du tc = ",tc,"-->",Yzigbee_last_message_txrx)
        plt.plot(Xcurrent_angles,Yzigbee_last_message_txrx)
        plt.title('courbe du tc = '+tc)
        plt.xlabel('angle')
        plt.ylabel('latence')
        plt.show()
        break
draw()
