This file describes my findings so far (they're not perfect).

## Outgoing Packet (so far)

So far, packets from the host to the mouse looks like this:
`['08', '06', '01', '12', '00', '00', '00', COLOR, COLOR, COLOR, '00', '00', '00', COLOR, COLOR, COLOR, 'fb', 'fb', '00', COLOR, COLOR, COLOR, 'ff', 'ff', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']`
Where COLOR is LED data described in the "LED Color" section.

### LED Color.

While the Icue software is open, I had it preview the colors on the GUI and recorded the packets with Wireshark (and saved the data as `IronclawWireless_While_Icue_Open_Color_Change_All_1.json`). The logo was switching between light-blue and yellow, the scrollwheel was switching between red and blue, and the front of the mouse was switching between green and purple. From then, I am passing the packets thru a Python script that plots each settable color place/area on the mouse on a graph. The colors are stored as a RGB bytes in different locations, so I combine them in Python to recreate the colors. Here are the screenshots for that finding:
![Icue software color and location](Screenshots/IronclawWireless_While_Icue_Open_Color_Change_All_1_settings.PNG)
![Python color plot](Screenshots/IronclawWireless_While_Icue_Open_Color_Change_All_1_plot_output.PNG)
From that, we could tell that the RGB bytes in the outgoing data from the host to the mouse are mapped as follows:

- Bytes 7, 13, and 19 for the logo's RGB colors
- Bytes 8, 14, and 20 for the scroll wheel's RGB colors
- Bytes 9, 15, and 21 for the front's RGB colors

Interestingly, the packets don't different if the color is set in "Lightning Effects" and "Hardware Lightning", where the host will still seem to command the mouse during "Hardware Lightning" mode, which in my opinion is a waste of resources.