import usb.core
import usb.util
import usb.backend.libusb1
import sys
import time

dev = usb.core.find(idVendor=0x1b1c, idProduct=0x1b4c)
reattach = []


def create_packet(data_array):
    ret = bytearray(64)
    for d_i, d in enumerate(data_array):
        ret[d_i] = d
    return ret


def send_and_print_packet(data):
    if isinstance(data, str):
        packet_to_send = bytearray(data)
    else:
        packet_to_send = create_packet(data)
    dev.write(0x04, packet_to_send, 1000)
    print("Sent %s" % packet_to_send)
    print("Recieved %s" % bytearray(dev.read(0x84, 64, 1000)))
    print('')


def main():
    global dev, reattach

    if dev is None:
        raise ValueError('Device not found')

    print(vars(dev))

    for i in range(4):
        if dev.is_kernel_driver_active(i):
            reattach.append(i)
            dev.detach_kernel_driver(i)

    try:
        usb.util.claim_interface(dev, 1)
    except usb.core.USBError:
        pass

    send_and_print_packet([0x08, 0x01, 0x03, 0x00, 0x02])
    send_and_print_packet([0x08, 0x01, 0x02, 0x00, 0xe8, 0x03])
    send_and_print_packet([0x08, 0x06, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])
    send_and_print_packet([0x08, 0x06, 0x01, 0x0a, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])
    send_and_print_packet([0x08, 0x0d, 0x00, 0x01])

    time.sleep(0.5)
    send_and_print_packet([0x08, 0x06, 0x01, 0x12, 0x00, 0x00, 0x00, 0xaa, 0xaa, 0xaa,
                           0x00, 0x00, 0x00, 0xaa, 0xaa, 0xaa, 0xfb, 0xfb, 0x00,
                           0xaa, 0xaa, 0xaa, 0xff, 0xff])


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Exception: %s" % e)
        pass
    # Packet that gets sent out when Icue closes
    send_and_print_packet([0x08, 0x01, 0x03, 0x00, 0x01])
    # Release interface
    usb.util.release_interface(dev, 1)
    usb.util.dispose_resources(dev)
    for i in reattach:
        dev.attach_kernel_driver(i)
