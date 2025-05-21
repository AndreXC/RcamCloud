import platform
import subprocess

def get_bios_serial():
    """
    Obtém o número serial do BIOS via PowerShell.
    """
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-WmiObject Win32_BIOS | Select-Object -ExpandProperty SerialNumber'],
            capture_output=True, text=True, check=True
        )
        serial = result.stdout.strip()
        return serial if serial else "UNKNOWN_BIOS"
    except Exception:
        return "UNKNOWN_BIOS"

def get_system_uuid():
    """
    Obtém o UUID do sistema via PowerShell.
    """
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-WmiObject Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID'],
            capture_output=True, text=True, check=True
        )
        uuid = result.stdout.strip()
        return uuid if uuid else "UNKNOWN_UUID"
    except Exception:
        return "UNKNOWN_UUID"

def get_hostname():
    """
    Obtém o nome do host da máquina.
    """
    return platform.node()

class GetToken:
    """
    Classe para geração de token único do dispositivo.
    """
    def __init__(self):
        self.bios_serial = get_bios_serial()
        self.uuid = get_system_uuid()
        self.hostname = get_hostname()

    def generate_token(self):
        """
        Gera o token único baseado no BIOS serial, UUID e hostname.
        """
        return f"{self.bios_serial};{self.uuid};{self.hostname}"