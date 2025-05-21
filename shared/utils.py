import hashlib
import platform
import wmi


def get_bios_serial():
    c = wmi.WMI()
    for bios in c.Win32_BIOS():
        return bios.SerialNumber.strip()


def get_system_uuid():
    c = wmi.WMI()
    for cs in c.Win32_ComputerSystemProduct():
        return cs.UUID.strip()

def getHostname():
    return platform.node()



class GetToken:
    def __init__(self):
        self.token = None
        self.BIOSserial = get_bios_serial()
        self.uuid = get_system_uuid()
        self.hostname = getHostname()
    
    def generate_token(self):
        return str(self.BIOSserial) +';' + str(self.uuid) +';' + str(self.hostname)