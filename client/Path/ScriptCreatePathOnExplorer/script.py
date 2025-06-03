import winreg as reg
import uuid
import os
import ctypes
import subprocess
import sys

class CustomFolderAdder:
    def __init__(self, name: str, folder_path: str, icon_path: str):
        self.name = name
        self.folder_path = folder_path
        self.icon_path = icon_path
        self.guid_str = f"{{{str(uuid.uuid4()).upper()}}}"
        self._ensure_admin()

    def _ensure_admin(self):
        if not self._is_admin():
            print("⚠ Reinicie este script como administrador...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()

    def _is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _restart_explorer(self):
        subprocess.run("taskkill /f /im explorer.exe", shell=True)
        subprocess.run("start explorer.exe", shell=True)

    def _set_folder_attributes(self):
        FILE_ATTRIBUTE_DIRECTORY = 0x10
        FILE_ATTRIBUTE_SYSTEM = 0x4
        FILE_ATTRIBUTE_READONLY = 0x1
        attrs = FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_READONLY

        SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW
        SetFileAttributes.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32]
        SetFileAttributes.restype = ctypes.c_bool

        if not SetFileAttributes(self.folder_path, attrs):
            print(f"⚠️ Falha ao definir atributos da pasta '{self.folder_path}'.")

    def _create_desktop_ini(self):
        desktop_ini = os.path.join(self.folder_path, "desktop.ini")
        content = f"""[.ShellClassInfo]
        IconResource={self.icon_path},0
        IconFile={self.icon_path}
        IconIndex=0
        """
        try:
            with open(desktop_ini, "w", encoding="utf-8") as f:
                f.write(content)

            FILE_ATTRIBUTE_HIDDEN = 0x2
            FILE_ATTRIBUTE_SYSTEM = 0x4
            attrs = FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM

            SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW
            SetFileAttributes.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32]
            SetFileAttributes.restype = ctypes.c_bool

            if not SetFileAttributes(desktop_ini, attrs):
                print(f"⚠️ Falha ao ocultar desktop.ini.")

        except Exception as e:
            print(f"❌ Erro ao criar desktop.ini: {e}")

    def _write_registry_entries(self):
        paths = {
            "clsid": fr"Software\Classes\CLSID\{self.guid_str}",
            "shell_folder": fr"Software\Classes\CLSID\{self.guid_str}\ShellFolder",
            "instance": fr"Software\Classes\CLSID\{self.guid_str}\Instance",
            "init": fr"Software\Classes\CLSID\{self.guid_str}\Instance\InitPropertyBag",
            "icon": fr"Software\Classes\CLSID\{self.guid_str}\DefaultIcon",
            "namespace": fr"Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{self.guid_str}",
            "hide_icon": fr"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel"
        }

        try:
            with reg.CreateKey(reg.HKEY_CURRENT_USER, paths["clsid"]) as key:
                reg.SetValueEx(key, None, 0, reg.REG_SZ, self.name)
                reg.SetValueEx(key, "System.IsPinnedToNameSpaceTree", 0, reg.REG_DWORD, 1)
                reg.SetValueEx(key, "SortOrderIndex", 0, reg.REG_DWORD, 66)

            with reg.CreateKey(reg.HKEY_CURRENT_USER, paths["icon"]) as key:
                reg.SetValueEx(key, None, 0, reg.REG_SZ, self.icon_path)

            with reg.CreateKey(reg.HKEY_CURRENT_USER, paths["shell_folder"]) as key:
                reg.SetValueEx(key, "Attributes", 0, reg.REG_DWORD, 0xf080004d)
                reg.SetValueEx(key, "FolderValueFlags", 0, reg.REG_DWORD, 0x28)

            with reg.CreateKey(reg.HKEY_CURRENT_USER, paths["instance"]) as key:
                reg.SetValueEx(key, "CLSID", 0, reg.REG_SZ, "{0E5AAE11-A475-4C5B-AB00-C66DE400274E}")

            with reg.CreateKey(reg.HKEY_CURRENT_USER, paths["init"]) as key:
                reg.SetValueEx(key, "TargetFolderPath", 0, reg.REG_SZ, self.folder_path)

            with reg.CreateKey(reg.HKEY_CURRENT_USER, paths["namespace"]) as key:
                reg.SetValueEx(key, None, 0, reg.REG_SZ, self.name)

            with reg.CreateKey(reg.HKEY_CURRENT_USER, paths["hide_icon"]) as key:
                reg.SetValueEx(key, self.guid_str, 0, reg.REG_DWORD, 0)

            print("✅ Pasta personalizada adicionada com ícone!")
            print("🔄 Reiniciando o Explorer para aplicar as alterações...")
            self._restart_explorer()

        except PermissionError:
            print("❌ Permissão negada. Execute como administrador.")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

    def create(self):
        if not os.path.exists(self.folder_path):
            print(f"⚠ Criando pasta: {self.folder_path}")
            os.makedirs(self.folder_path)

        if not os.path.isfile(self.icon_path):
            print(f"❌ Ícone não encontrado: {self.icon_path}")
            return

        print(f"📌 Usando GUID: {self.guid_str}")
        self._create_desktop_ini()
        self._set_folder_attributes()
        self._write_registry_entries()


# === USO SIMPLIFICADO ===
if __name__ == "__main__":
    folder = CustomFolderAdder(
        name="Meus Projetos",
        folder_path=r"C:\MeusProjetos",
        icon_path=r"C:\MeusProjetos\OneDrive_23654.ico"
    )
    folder.create()
