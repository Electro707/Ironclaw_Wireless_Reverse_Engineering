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

# Create root for file dialog
root = tkinter.Tk()
root.withdraw()


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


def find_similar(data_array, preamble=""):
    shared_data = None
    for data in data_array:
        if shared_data is None:
            shared_data = data.copy()
            continue
        for b in range(len(data)):
            if data[b] != shared_data[b]:
                shared_data[b] = None
    print("%sShared data in array:\n%s" % (preamble, shared_data))


def load_json_from_file():
    file_name = filedialog.askopenfilename(initialdir="../", title="Select file", filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
    if file_name is None:
        return None
    if file_name is '':
        return None
    print("Opening %s" % file_name)

    f = open(file_name, 'r')
    json_content = f.read()
    f.close()

    disected_json = json.loads(json_content)
    return disected_json


def match_different_captures():
    disected_jsons = []
    while 1:
        ds = load_json_from_file()
        if ds is None:
            break
        disected_jsons.append(ds)

    host_sent_info = []
    device_sent_info = []

    for json_index, json in enumerate(disected_jsons):
        hsi = []
        dsi = []
        for i in json:
            if int(i['_source']['layers']['usb']['usb.transfer_type'], 0) == 0x02:
                continue
            elif int(i['_source']['layers']['usb']['usb.transfer_type'], 0) == 0x01:
                if int(i['_source']['layers']['usb']['usb.data_len']) != 0:
                    data = i['_source']['layers']['usb.capdata']
                    data = data.split(':')
                    if i['_source']['layers']['usb']['usb.src'] == 'host':
                        # print("HOST: %s" % data)
                        hsi.append(data)
                    else:
                        # print("DEVICE: %s" % data)
                        dsi.append(data)
                        pass
        find_similar(hsi, "For host->device #%s :" % json_index)
        find_similar(dsi, "For device->host #%s :" % json_index)
        host_sent_info.append(hsi)
        device_sent_info.append(dsi)

    total_lenght_host = len(host_sent_info[0])
    for i in host_sent_info:
        if len(i) != total_lenght_host:
            print("Lenght of data (host->device) does not match between different runs")
            sys.exit(2)
    total_lenght_device = len(device_sent_info[0])
    for i in device_sent_info:
        if len(i) != total_lenght_device:
            print("Lenght of data (host->device) does not match between different runs")
            sys.exit(2)
    #
    # for index in range(total_lenght_host):
    #     for data_i_1, numb_hosts in enumerate(host_sent_info):
    #         for data_i_2, numb_hosts2 in enumerate(host_sent_info):
    #             if numb_hosts[index] != numb_hosts2[index]:
    #                 print("Line from json #%s and #%s don't match on line %s: \n%s\n%s" % (data_i_1, data_i_2, index, numb_hosts[index], numb_hosts2[index]))
    #                 break


def analyze_rgb_colors():
    disected_json = load_json_from_file()
    if disected_json is None:
        return
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
                    # print("DEVICE: %s" % data)
                    # host_sent_info.append(data)
                    pass

    find_similar(host_sent_info)
    plot_rgb_data_over_time(host_sent_info)


if __name__ == '__main__':
    # Change this to whichever analyzer you
    program_to_run = 'color'

    if program_to_run == 'color':
        # Program to load a Wireshark JSON output with only color data ( by starting wireshark sniffing with another mouse while Icue is running
        # in the background, which it should only send data for the LED's color)
        analyze_rgb_colors()
    elif program_to_run == 'match_differnt_programs':
        match_different_captures()


