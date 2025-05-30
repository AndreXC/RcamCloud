# import winreg as reg
# import uuid
# import os
# import ctypes
# import subprocess
# import sys
# import shutil

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# def run_as_admin():
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

# # def restart_explorer()
#     subprocess.run("taskkill /f /im explorer.exe", shell=True)
#     subprocess.run("start explorer.exe", shell=True)

# def set_folder_system_attributes(folder_path):
#     """
#     Define os atributos da pasta para sistema e oculta o desktop.ini
#     Isso permite que o Windows use o desktop.ini para personalização.
#     """
#     import ctypes.wintypes

#     FILE_ATTRIBUTE_HIDDEN = 0x2
#     FILE_ATTRIBUTE_SYSTEM = 0x4
#     FILE_ATTRIBUTE_READONLY = 0x1

#     FILE_ATTRIBUTE_DIRECTORY = 0x10

#     SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW
#     SetFileAttributes.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.DWORD]
#     SetFileAttributes.restype = ctypes.wintypes.BOOL

#     # Atributos atuais da pasta
#     attrs = FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_READONLY
#     result = SetFileAttributes(folder_path, attrs)
#     if not result:
#         print(f"⚠️ Falha ao definir atributos para a pasta '{folder_path}'. Execute como administrador.")

# def create_desktop_ini(folder_path, icon_path):
#     """
#     Cria o arquivo desktop.ini com as configurações para o ícone personalizado.
#     """
#     desktop_ini_path = os.path.join(folder_path, "desktop.ini")
#     content = f"""[.ShellClassInfo]
# IconResource={icon_path},0
# IconFile={icon_path}
# IconIndex=0
#     """

#     try:
#         with open(desktop_ini_path, "w", encoding="utf-8") as f:
#             f.write(content)

#         # Definir o arquivo desktop.ini como oculto e sistema
#         import ctypes.wintypes
#         FILE_ATTRIBUTE_HIDDEN = 0x2
#         FILE_ATTRIBUTE_SYSTEM = 0x4
#         attrs = FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM

#         SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW
#         SetFileAttributes.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.DWORD]
#         SetFileAttributes.restype = ctypes.wintypes.BOOL

#         if not SetFileAttributes(desktop_ini_path, attrs):
#             print(f"⚠️ Falha ao definir atributos para {desktop_ini_path}.")
#     except Exception as e:
#         print(f"❌ Erro ao criar desktop.ini: {e}")

# def add_custom_folder(name, target_path, icon_path):
#     if not os.path.exists(target_path):
#         print(f"⚠ Criando pasta ausente: {target_path}")
#         os.makedirs(target_path)

#     if not os.path.isfile(icon_path):
#         print(f"❌ Ícone '{icon_path}' não encontrado.")
#         return

#     # Criar desktop.ini dentro da pasta para o ícone
#     create_desktop_ini(target_path, icon_path)
#     set_folder_system_attributes(target_path)

#     guid = str(uuid.uuid4()).upper()
#     guid_str = f"{{{guid}}}"
#     print(f"📌 Usando GUID: {guid_str}")

#     clsid_path = fr"Software\Classes\CLSID\{guid_str}"
#     shell_folder_path = fr"{clsid_path}\ShellFolder"
#     instance_path = fr"{clsid_path}\Instance"
#     init_property_bag_path = fr"{instance_path}\InitPropertyBag"
#     default_icon_path = fr"{clsid_path}\DefaultIcon"
#     namespace_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{guid_str}"
#     hide_icons_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel"

#     try:
#         # CLSID principal
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, clsid_path) as key:
#             reg.SetValueEx(key, None, 0, reg.REG_SZ, name)
#             reg.SetValueEx(key, "System.IsPinnedToNameSpaceTree", 0, reg.REG_DWORD, 1)
#             reg.SetValueEx(key, "SortOrderIndex", 0, reg.REG_DWORD, 66)

#         # DefaultIcon - chave separada para o ícone
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, default_icon_path) as icon_key:
#             reg.SetValueEx(icon_key, None, 0, reg.REG_SZ, icon_path)

#         # ShellFolder com atributos corretos para pasta normal
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, shell_folder_path) as shell_key:
#             reg.SetValueEx(shell_key, "Attributes", 0, reg.REG_DWORD, 0xf080004d)
#             reg.SetValueEx(shell_key, "FolderValueFlags", 0, reg.REG_DWORD, 0x28)

#         # Instance - necessário para que o Explorer reconheça
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, instance_path) as instance_key:
#             reg.SetValueEx(instance_key, "CLSID", 0, reg.REG_SZ, "{0E5AAE11-A475-4C5B-AB00-C66DE400274E}")

#         with reg.CreateKey(reg.HKEY_CURRENT_USER, init_property_bag_path) as init_key:
#             reg.SetValueEx(init_key, "TargetFolderPath", 0, reg.REG_SZ, target_path)

#         # Namespace - adiciona ao painel lateral
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, namespace_path) as ns_key:
#             reg.SetValueEx(ns_key, None, 0, reg.REG_SZ, name)

#         # Exibir o ícone no painel (0 = visível)
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, hide_icons_path) as hide_key:
#             reg.SetValueEx(hide_key, guid_str, 0, reg.REG_DWORD, 0)

#         print("✅ Pasta personalizada adicionada com ícone!")
#         print("🔄 Reiniciando o Explorer para aplicar as alterações...")
#         restart_explorer()

#     except PermissionError:
#         print("❌ Permissão negada. Execute o script como administrador.")
#     except Exception as e:
#         print(f"❌ Erro inesperado: {e}")

# if __name__ == "__main__":
#     if not is_admin():
#         print("⚠ Reinicie este script como administrador...")
#         run_as_admin()
#         sys.exit()

#     # Configurações - personalize aqui
#     nome_da_pasta = "Meus Projetos"
#     caminho_da_pasta = r"C:\MeusProjetos"
#     caminho_do_icone = r"C:\MeusProjetos\OneDrive_23654.ico"  # Caminho absoluto para o arquivo .ico

#     add_custom_folder(nome_da_pasta, caminho_da_pasta, caminho_do_icone)
