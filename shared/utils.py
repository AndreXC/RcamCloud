# shared/utils.py
import hashlib
import subprocess
import uuid
import platform
import os
import wmi
def calculate_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

   
def get_baseboard_serial():
    c = wmi.WMI()
    for board in c.Win32_BaseBoard():
        return board.SerialNumber.strip()

def get_bios_serial():
    c = wmi.WMI()
    for bios in c.Win32_BIOS():
        return bios.SerialNumber.strip()

def get_disk_serials():
    c = wmi.WMI()
    serials = []
    for disk in c.Win32_DiskDrive():
        serials.append(disk.SerialNumber.strip())
    return serials

def get_system_uuid():
    c = wmi.WMI()
    for cs in c.Win32_ComputerSystemProduct():
        return cs.UUID.strip()

def get_mac_addresses():
    c = wmi.WMI()
    macs = []
    for nic in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        macs.append(nic.MACAddress)
    return macs

def get_system_info():
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Node": platform.node(),
        "Processor": platform.processor(),
    }

# Coleta das informações
info = {
    "Baseboard Serial": get_baseboard_serial(),
    "BIOS Serial": get_bios_serial(),
    "Disk Serials": get_disk_serials(),
    "System UUID": get_system_uuid(),
    "MAC Addresses": get_mac_addresses(),
    "System Info": get_system_info(),
}

# Exibir
for key, value in info.items():
    print(f"{key}: {value}")
