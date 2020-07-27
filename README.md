# IronClaw Wireless Protocol Reverse Engineering

This is a repository containing everything that I use/recorded to reverse engineer the IronClaw Wireless mouse, which aparantly uses a different protocol than the "regular" IronClaw(why would it not, right?).

Feel free to contribute/join if you so wish (the more people the merrier)

## Folder Structure:

- Extracted JSON: As the name says, it's extracted packets from each Wireshark probing as a JSON file, to make it easier to interact with Python
- Wireshark Captures: The output of each Wireshark capture
- Python Stuff: All Python modules/programs that I use to attempt to parase the data aquired from Wireshark.
- Wireshark LUA Plugin: My own WIP Plugin for Wireshark to analyze the Ironclaw Wireless packets. Based on CKB-Next's LUA Pluggin (Had to fork it due to the different protocol)

## Findings

All discoveries that I made will be documented in the ![Findings.md](Findings.md) file.
