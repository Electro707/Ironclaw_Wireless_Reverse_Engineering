"""
    This python file is to disect data exported from Wireshark with the IronClaw Wireless
    The goal of this program is to generalize it so it could intepret any kind of data, thus allowing us to port that information over
    to the ckb-next project.
"""
import json
from tkinter import filedialog
import tkinter
import sys
import matplotlib.pyplot as plt


def plot_rgb_data_over_time(data_arr):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    ax3 = ax2.twiny()
    for index, data in enumerate(data_arr):
        ax1.scatter(index, 0, color="#%s%s%s" % (data[7], data[13], data[19]))
        ax2.scatter(index, 1, color="#%s%s%s" % (data[8], data[14], data[20]))
        ax3.scatter(index, 2, color="#%s%s%s" % (data[9], data[15], data[21]))
    plt.show()


def find_similar(data_array):
    shared_data = None
    for data in data_array:
        if shared_data is None:
            shared_data = data.copy()
            continue
        for b in range(len(data)):
            if data[b] != shared_data[b]:
                shared_data[b] = None
    print("Shared data in array:\n%s" % shared_data)


def main_program():
    root = tkinter.Tk()
    root.withdraw()
    file_name = filedialog.askopenfilename(initialdir="../", title="Select file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
    if file_name is None:
        sys.exit(2)
    if file_name is '':
        sys.exit(2)

    f = open(file_name, 'r')
    json_content = f.read()
    f.close()

    disected_json = json.loads(json_content)

    host_sent_info = []

    for i in disected_json:
        if int(i['_source']['layers']['usb']['usb.transfer_type'], 0) == 0x02:
            continue
        elif int(i['_source']['layers']['usb']['usb.transfer_type'], 0) == 0x01:
            if int(i['_source']['layers']['usb']['usb.data_len']) != 0:
                data = i['_source']['layers']['usb.capdata']
                data = data.split(':')
                if i['_source']['layers']['usb']['usb.src'] == 'host':
                    print("HOST: %s" % data)
                    host_sent_info.append(data)
                else:
                    #print("DEVICE: %s" % data)
                    #host_sent_info.append(data)
                    pass
    print(host_sent_info[0][8])

    find_similar(host_sent_info)
    plot_rgb_data_over_time(host_sent_info)


if __name__ == '__main__':
    main_program()
