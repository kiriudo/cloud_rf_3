import pandas
import matplotlib.pyplot as plt

def draw():
    df = pandas.read_csv('data_aws.csv')
    trackers = df["tracker"].tolist()
    unique_trackers = set(trackers)
    print(list(unique_trackers))
    for tc in list(unique_trackers):
        print(tc)
        tc_data = df.loc[df['tracker'] == tc]
        Xcurrent_angles = tc_data['current_angle'].tolist()
        Yzigbee_last_message_txrx = tc_data["zigbee_last_message_txrx"].tolist()
        print("Les angles du tc = ",tc,"-->",Xcurrent_angles)
        print("Latence du tc = ",tc,"-->",Yzigbee_last_message_txrx)
        plt.plot(Xcurrent_angles,Yzigbee_last_message_txrx)
        plt.title('courbe du tc = '+tc)
        plt.xlabel('current_angle')
        plt.ylabel('zigbee_last_message_txrx')
        plt.show()
        break
draw()