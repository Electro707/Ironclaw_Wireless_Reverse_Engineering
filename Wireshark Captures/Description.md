This folder describes what each file in the folder means, and what/how it was captured, and any other important imformation.

- IronclawWireless_Startup_x: Captures that were done when the Icue was started (the mouse wasn't moved or touched). This is the initialization, when Icue starts communicating with the mouse and getting things like firmware info and whatnot.
	
	Note: For Startups 1-2, the Ironclaw had 1 profile stored in hardware. In run #3, all hardware profiles were cleared and so was the device's memory.
- IronclawWireless_While_Icue_Open_Rainbow x: Captures that were done after Icue was started, and the mouse was lighting up it's LEDs in the 'rainbow' mode. Useful for seeing how Icue sends LED data to the mouse
- IronclawWireless_While_Icue_Open_Color_Change_All_1: Capture that was done when specific LEDs (the logo, scroll, and front) was changing at different colors. See (Findings.md)[../Findings.md] to know more about that process.
- IronclawWireless_Change_DPI_x: Captures where I change the DPI in software.
	
	For run#1, I was adjusting the second dpi level from 200->500->1000->2000. The first DPI level was set to 500, while the third was set to 2000.
	For run#2, I was adjusting the first dpi level from 200->500->1000->2000. The second and third level was set to 2000.