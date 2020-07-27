--[[
	Ironshark Wireless Packet Disector
	WORK IN PROGRESS
	
	Based on CKB-Next's Pluggin:
	https://github.com/ckb-next/CueShark
--]]
cue_proto = Proto("cue", "Corsair Utility Engine protocol")

local commands = {
    -- [0x01] = "HID Event",
    -- [0x02] = "Media Key Event",
    -- [0x03] = "Corsair HID Event",
    [0x08] = "Set",
    [0x00] = "Get",
    -- [0x7f] = "Write Multiple",
    -- [0xff] = "Read Multiple"
}

local subcommands = {
    [0x060112] = "Set LED color",
    [0x02] = "Reset",
}

local reset_types = {
    [0x00] = "Medium Reset",
    [0x01] = "Fast Reset",
    [0x03] = "New Reset", -- Needs to be investigated
    [0xaa] = "Reboot to Bootloader",
    [0xf0] = "Slow Reset"
}

local control_types = {
    [0x01] = "Hardware",
    [0x02] = "Software"
}

local colour_types = {
    [0x01] = "Red",
    [0x02] = "Green",
    [0x03] = "Blue"
}

local vendor_ids = {
    [0x1b1c] = "Corsair"
}

local product_ids = {
    [0x1b4c] = "IRONCLAW_WIRELESS"
}
local device_types = {
    [0xc0] = "Keyboard",
    [0xc1] = "Mouse",
    [0xc2] = "Mousepad"
}

local layout_types = {
    [0x00] = "ANSI",
    [0x01] = "ISO",
    [0x02] = "ABNT",
    [0x03] = "JIS",
    [0x04] = "Dubeolsik"
}

local hwprofile_commands = {
    [0x01] = "Get Buffer Size",
    [0x03] = "Get File Size",
    [0x04] = "Get File List",
    [0x05] = "Write to Filename",
    [0x07] = "Switch to File",
    [0x08] = "End File",
    [0x09] = "Write Segment",
    [0x0a] = "Set Read Mode",
    [0x0b] = "Set Write Mode",
    [0x0c] = "Switch Hardware Mode",
    [0x0d] = "Get Last Status"
}

local f = cue_proto.fields

-- Root commands
f.cmd = ProtoField.uint8("cue.command", "Command", base.HEX, commands)

-- Subcommands
f.subcmd = ProtoField.uint8("cue.subcommand", "Subcommand", base.HEX, subcommands)

-- Logo LED colors
f.logo_led_r = ProtoField.uint8("cue.color.logo.r", "Logo LED Red color", base.HEX)
f.logo_led_g = ProtoField.uint8("cue.color.logo.g", "Logo LED Green color", base.HEX)
f.logo_led_b = ProtoField.uint8("cue.color.logo.b", "Logo LED Blue color", base.HEX)

-- Scrollwheel LED colors
f.scrollwheel_led_r = ProtoField.uint8("cue.color.scrollwheel.r", "Scrollwheel LED Red color", base.HEX)
f.scrollwheel_led_g = ProtoField.uint8("cue.color.scrollwheel.g", "Scrollwheel LED Green color", base.HEX)
f.scrollwheel_led_b = ProtoField.uint8("cue.color.scrollwheel.b", "Scrollwheel LED Blue color", base.HEX)

-- Front LED colors
f.front_led_r = ProtoField.uint8("cue.color.front.r", "Front LED Red color", base.HEX)
f.front_led_g = ProtoField.uint8("cue.color.front.g", "Front LED Green color", base.HEX)
f.front_led_b = ProtoField.uint8("cue.color.front.b", "Front LED Blue color", base.HEX)



--[[
-- Root commands
f.cmd = ProtoField.uint8("cue.command", "Command", base.HEX, commands)

-- Subcommands
f.subcmd = ProtoField.uint8("cue.subcommand", "Subcommand", base.HEX, subcommands)

-- Reset Subcommands
f.reset_type = ProtoField.uint8("cue.reset.type", "Reset Type", base.HEX, reset_types)

-- Control Subcommands
f.special_mode = ProtoField.uint8("cue.special_function.mode", "Special Function Control Mode", base.DEC, control_types)
f.lighting_mode = ProtoField.uint8("cue.lighting.mode", "Lighting Control Mode", base.DEC, control_types)

-- Colour Subcommands
f.colour_type = ProtoField.uint8("cue.colour.type", "Colour Type", base.DEC, colour_types)

-- Firmware Update
f.fwupdate_position = ProtoField.uint8("cue.fwupdate.position", "Firmware Update Data Position", base.DEC)

-- FW identification fields
f.ident_fwver = ProtoField.uint16("cue.ident.fwver", "Firmware Version", base.HEX)
f.ident_bldver = ProtoField.uint16("cue.ident.bldver", "Bootloader Version", base.HEX)
f.ident_vendor = ProtoField.uint16("cue.ident.vendor", "USB Vendor ID", base.HEX, vendor_ids)
f.ident_product = ProtoField.uint16("cue.ident.product", "USB Product ID", base.HEX, product_ids)
f.ident_pollrate = ProtoField.uint8("cue.ident.pollrate", "Poll Rate (msec)", base.DEC)
f.ident_devtype = ProtoField.uint8("cue.ident.device_type", "Device Type", base.HEX, device_types)
f.ident_layout = ProtoField.uint8("cue.ident.layout", "Keyboard Layout", base.HEX, layout_types)

-- Hardware modes
f.profile_init_buffer = ProtoField.uint16("cue.profile.init.bufsize", "Data Buffer Size")

f.profile_size = ProtoField.uint32("cue.profile.size", "Profile File Size")

f.profile_guid = ProtoField.guid("cue.profile.guid", "Profile GUID")
f.profile_name = ProtoField.string("cue.profile.name", "Profile Name")

f.profile_command = ProtoField.uint8("cue.profile.command", "Profile Command", base.DEC, hwprofile_commands)
f.profile_filename = ProtoField.stringz("cue.profile.filename", "Filename")
f.profile_mode = ProtoField.uint8("cue.profile.modenum", "Profile Mode Number", base.DEC)

f.profile_status = ProtoField.uint8("cue.profile.status", "Profile Operation Status")

-- Payload fields
f.payload_payload = ProtoField.bytes("cue.payload.payload", "Payload")
f.payload_size = ProtoField.uint8("cue.payload.size", "Payload Size", base.DEC)
f.payload_seqnum = ProtoField.uint8("cue.payload.seqnum", "Payload Sequence Number", base.DEC)

-- Mouse specific
f.mouse_dpi_independent = ProtoField.bool("cue.mouse.dpi.independent", "Mouse Independent X/Y")
f.mouse_dpi_x = ProtoField.uint16("cue.mouse.dpi.x", "Mouse X DPI", base.DEC)
f.mouse_dpi_y = ProtoField.uint16("cue.mouse.dpi.y", "Mouse Y DPI", base.DEC)
f.mouse_dpi_red = ProtoField.uint8("cue.mouse.dpi.red", "Mouse DPI Indicator Red", base.DEC)
f.mouse_dpi_green = ProtoField.uint8("cue.mouse.dpi.green", "Mouse DPI Indicator Green", base.DEC)
f.mouse_dpi_blue = ProtoField.uint8("cue.mouse.dpi.blue", "Mouse DPI Indicator Blue", base.DEC)

f.mouse_snap = ProtoField.bool("cue.mouse.snap", "Angle Snap Enabled")

f.mouse_pollrate = ProtoField.uint8("cue.mouse.pollrate", "Mouse Poll Rate", base.DEC)

-- Wireless settings
f.wireless_powersave = ProtoField.uint8("cue.wireless.powersave", "Wireless Power Saving", base.DEC)
f.wireless_sleeptime = ProtoField.uint8("cue.wireless.sleeptime", "Time before sleeping (minutes)")
f.wireless_id = ProtoField.uint32("cue.wireless.pairing_id", "Wireless pairing ID")
f.wireless_fwver = ProtoField.uint16("cue.wireless.fwver", "Radio Firmware Version", base.HEX)

-- Misc
f.somethingu32 = ProtoField.uint32("cue.something", "Something", base.HEX)

--]]

function cue_proto.dissector(buffer, pinfo, tree)
    -- Corsair packets are 64 bytes long.
    if buffer:len() ~= 64 then
        return
    end

    local command = buffer(offset, 1)

    pinfo.cols["protocol"] = "CUE"

    local t_cue = tree:add(cue_proto, buffer())
    local offset = 0

    t_cue:add(f.cmd, command)
    command = command:uint()
    offset = offset + 1

    local subcommand = buffer(offset, 3)
    offset = offset + 4

    if command == 0x08 or command == 0x00 then -- Read/Write
        if command == 0X08 then
            pinfo.cols["info"] = "Set"
        else
            pinfo.cols["info"] = "Get"
        end
        t_cue:add(f.subcmd, subcommand)
        subcommand = subcommand:uint()
		
		if subcommand == 0x060112 then
			pinfo.cols["info"]:append(" LED Set")
			offset = offset + 2
			
			local led_subtree = t_cue:add(cue_proto, buffer(), "LED Colors")
			
			local logo_led_subtree = led_subtree:add(cue_proto, buffer(), "Logo Colors")
			local scrollwheel_led_subtree = led_subtree:add(cue_proto, buffer(), "Scrollwheel Colors")
			local front_led_subtree = led_subtree:add(cue_proto, buffer(), "Front Colors")
			
			
			logo_led_subtree:add(f.logo_led_r, buffer(offset, 1))
			offset = offset + 1
			scrollwheel_led_subtree:add(f.scrollwheel_led_r, buffer(offset, 1))
			offset = offset + 1
			front_led_subtree:add(f.front_led_r, buffer(offset, 1))
			offset = offset + 1
			
			offset = offset + 3
			
			logo_led_subtree:add(f.logo_led_g, buffer(offset, 1))
			offset = offset + 1
			scrollwheel_led_subtree:add(f.scrollwheel_led_g, buffer(offset, 1))
			offset = offset + 1
			front_led_subtree:add(f.front_led_g, buffer(offset, 1))
			offset = offset + 1
			
			offset = offset + 3
			
			logo_led_subtree:add(f.logo_led_b, buffer(offset, 1))
			offset = offset + 1
			scrollwheel_led_subtree:add(f.scrollwheel_led_b, buffer(offset, 1))
			offset = offset + 1
			front_led_subtree:add(f.front_led_b, buffer(offset, 1))
			offset = offset + 1
			
			offset = offset + 3
			
        else
            pinfo.cols["info"]:append(" Unknown " .. tostring(subcommand))
        end

    else
        pinfo.cols["info"] = "Unknown " .. tostring(command)
    end
end

usb_table = DissectorTable.get("usb.interrupt")
usb_table:add(0x03, cue_proto)
usb_table:add(0xffff, cue_proto)
