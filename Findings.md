This file describes my findings so far (they're not perfect).

## Outgoing Packet
The first byte for when the host sends out a command to the mouse is `08`, while the mouse's response is `00`. Doesn't matter if the host is reading or writing to the device, i've yet got to a packet where there's a different first byte.

All packets that are sent are 64-bits long with padded zeros at the end. For the rest of this document, I will not show the trailing zeros.

## Firmware version
If the following command is sent out to the mouse: `08 02 13`, then the mouse will respond with the following packet: `00 02 00 XX YY ZZ`, where XX, YY, and ZZ are the version number in hex, corresponding to the sub-version. For example, if firmware version is 1.16.107, we except XX to be 0x01, YY to be 0x10, and ZZ to be 0x6B.

## Changing device polling speed
The following command must be sent by the host to change the polling rate:
`08 01 01 00 XX`, where XX is:

- 01 for 125Hz/8ms
- 02 for 250Hz/4ms
- 03 for 500Hz/2ms
- 04 for 1000Hz/1ms

After the command has been sent to the mouse, it will respond with the following packet:
`00 01`. Then, it will reset and reconnecting it in software is required.

## LED Color

##### Testing Method
While the Icue software is open, I had it preview the colors on the GUI and recorded the packets with Wireshark (and saved the data as `IronclawWireless_While_Icue_Open_Color_Change_All_1.json`). The logo was switching between light-blue and yellow, the scrollwheel was switching between red and blue, and the front of the mouse was switching between green and purple. From then, I am passing the packets thru a Python script that plots each settable color place/area on the mouse on a graph. The colors are stored as a RGB bytes in different locations, so I combine them in Python to recreate the colors. Here are the screenshots for that finding:
![Icue software color and location](Screenshots/IronclawWireless_While_Icue_Open_Color_Change_All_1_settings.PNG)
![Python color plot](Screenshots/IronclawWireless_While_Icue_Open_Color_Change_All_1_plot_output.PNG)

##### Conclusion in LED coloring
After analyzing the data, I conclude that each 'LED' packet looks like the following:

`08 06 01 12 00 00 00 COLOR COLOR COLOR 00 00 00 COLOR COLOR COLOR fb fb 00 COLOR COLOR COLOR ff ff`
Where COLOR is the diffrent RGB bytes for each section of the mouse, such as:

- Bytes 7, 13, and 19 for the logo's RGB colors
- Bytes 8, 14, and 20 for the scroll wheel's RGB colors
- Bytes 9, 15, and 21 for the front's RGB colors

The mouse seems to always respond with the following packet after a color has been set:
`00 06`

Interestingly, the packets don't different if the color is set in "Lightning Effects" and "Hardware Lightning", where the host will still seem to command the mouse during "Hardware Lightning" mode, which in my opinion is a waste of resources.