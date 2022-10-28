import pandas
import matplotlib.pyplot as plt

def draw():
    df = pandas.read_csv('data_aws.csv')
    trackers = df["tracker"].tolist()
    unique_trackers = set(trackers)
    print(unique_trackers)
    Xcurrent_angles = df["current_angle"].tolist()
    Yzigbee_last_message_txrx = df["zigbee_last_message_txrx"].tolist()
    plt.plot(Xcurrent_angles,Yzigbee_last_message_txrx)
    plt.xlabel('current_angle')
    plt.ylabel('zigbee_last_message_txrx')
    plt.show()
draw()