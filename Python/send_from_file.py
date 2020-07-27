"""
    This Python program takes a Wireshark capture and sends out all data which is sent to the host. From
    there, I could send whiever packets I want defined by the after_init() function. This is to try to find
    out how Icue takes control over the mouse

    This is a pseudo-desperate attempt at getting the mouse working. From there, i'll do start Muntzing the
    packets sent until it doesn't work.
"""

import usb.core
import usb.util
import usb.backend.libusb1
import sys
import time
import json
from tkinter import filedialog
import tkinter

dev = usb.core.find(idVendor=0x1b1c, idProduct=0x1b4c)
reattach = []

# Create root for file dialog
root = tkinter.Tk()
root.withdraw()


def pretty_string_bytes(byte_array):
    ret_str = "["
    for b in byte_array:
        ret_str += "%02x, " % b
    ret_str += "]"
    return ret_str


def create_packet(data_array):
    ret = bytearray(64)
    for d_i, d in enumerate(data_array):
        if isinstance(d, str):
            ret[d_i] = int(d, 16)
        else:
            ret[d_i] = d
    return ret


def send_and_print_packet(data):
    if isinstance(data, str):
        packet_to_send = bytearray(data)
    else:
        packet_to_send = create_packet(data)
    dev.write(0x04, packet_to_send, 1000)
    print("Sent      %s" % pretty_string_bytes(packet_to_send))
    print("Recieved  %s" % pretty_string_bytes(bytearray(dev.read(0x84, 64, 1000))))
    print('')


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


def after_init():
    for l in range(10):
        time.sleep(0.25)
        send_and_print_packet([0x08, 0x06, 0x01, 0x12,
                               0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
        time.sleep(0.25)

        send_and_print_packet([0x08, 0x06, 0x01, 0x12,
                               0x00, 0x00, 0x00,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                               0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    time.sleep(2)


def main():
    global dev, reattach

    if dev is None:
        raise ValueError('Device not found')

    disected_json = load_json_from_file()
    if disected_json is None:
        return

    for i in range(4):
        if dev.is_kernel_driver_active(i):
            reattach.append(i)
            dev.detach_kernel_driver(i)
    try:
        usb.util.claim_interface(dev, 1)
    except usb.core.USBError:
        pass

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
                    if int(data[0], 16) != 0x08:
                        raise UserWarning("ERROR: First byte is not 0x08 of host")

                    if int(data[1], 16) == 0x08:
                        continue
                    elif int(data[1], 16) == 0x08:
                        continue
                    elif int(data[1], 16) == 0x09:
                        continue
                    elif int(data[1], 16) == 0x06:
                        continue
                    else:
                        host_sent_info.append(data)
                else:
                    # print("DEVICE: %s" % data)
                    # host_sent_info.append(data)
                    pass

    for data in host_sent_info:
        send_and_print_packet(data)

    after_init()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Exception: %s" % e)
    # Packet that gets sent out when Icue closes
    send_and_print_packet([0x08, 0x01, 0x03, 0x00, 0x01])
    # Release interface
    usb.util.release_interface(dev, 1)
    usb.util.dispose_resources(dev)
    for i in reattach:
        dev.attach_kernel_driver(i)
