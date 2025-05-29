
# import winreg as reg
# import uuid
# import os
# import ctypes
# import subprocess
# import sys

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# def run_as_admin():
#     print("🔐 Solicitando permissões administrativas...")
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

# def restart_explorer():
#     subprocess.run("taskkill /f /im explorer.exe", shell=True)
#     subprocess.run("start explorer.exe", shell=True)

# def add_custom_folder(name, target_path):
#     if not os.path.exists(target_path):
#         print(f"⚠ Criando pasta ausente: {target_path}")
#         os.makedirs(target_path)

#     # GUID fixo (você pode salvar esse para remoção depois)
#     guid = str(uuid.uuid4()).upper()
#     guid_str = f"{{{guid}}}"
#     print(f"📌 Usando GUID: {guid_str}")

#     # Caminhos no Registro
#     clsid_path = fr"Software\Classes\CLSID\{guid_str}"
#     shell_folder_path = fr"{clsid_path}\ShellFolder"
#     instance_path = fr"{clsid_path}\Instance"
#     init_property_bag_path = fr"{instance_path}\InitPropertyBag"
#     namespace_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{guid_str}"
#     hide_icons_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel"

#     try:
#         # CLSID principal
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, clsid_path) as key:
#             reg.SetValueEx(key, None, 0, reg.REG_SZ, name)
#             reg.SetValueEx(key, "System.IsPinnedToNameSpaceTree", 0, reg.REG_DWORD, 1)
#             reg.SetValueEx(key, "SortOrderIndex", 0, reg.REG_DWORD, 66)

#         # ShellFolder - define visibilidade e comportamento
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, shell_folder_path) as shell_key:
#             reg.SetValueEx(shell_key, "Attributes", 0, reg.REG_DWORD, 0xf080004d)
#             reg.SetValueEx(shell_key, "FolderValueFlags", 0, reg.REG_DWORD, 0x28)

#         # Instance e InitPropertyBag
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, instance_path) as instance_key:
#             reg.SetValueEx(instance_key, "CLSID", 0, reg.REG_SZ, "{0E5AAE11-A475-4C5B-AB00-C66DE400274E}")

#         with reg.CreateKey(reg.HKEY_CURRENT_USER, init_property_bag_path) as init_key:
#             reg.SetValueEx(init_key, "TargetFolderPath", 0, reg.REG_SZ, target_path)

#         # Namespace (explorer)
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, namespace_path) as ns_key:
#             reg.SetValueEx(ns_key, None, 0, reg.REG_SZ, name)

#         # HideDesktopIcons
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, hide_icons_path) as hide_key:
#             reg.SetValueEx(hide_key, guid_str, 0, reg.REG_DWORD, 0)

#         print("✅ Pasta adicionada ao painel lateral com sucesso!")
#         print("🔄 Reiniciando o Windows Explorer...")
#         restart_explorer()

#     except PermissionError:
#         print("❌ Permissão negada. Execute como administrador.")

# if __name__ == "__main__":
#     if not is_admin():
#         run_as_admin()
#         sys.exit()

#     # 🔧 Personalize aqui:
#     nome_da_pasta = "Meus Projetos"
#     caminho = r"C:\MeusProjetos"

#     add_custom_folder(nome_da_pasta, caminho)


import winreg as reg
import uuid
import os
import ctypes
import subprocess
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def restart_explorer():
    subprocess.run("taskkill /f /im explorer.exe", shell=True)
    subprocess.run("start explorer.exe", shell=True)

def add_custom_folder(name, target_path, icon_path):
    if not os.path.exists(target_path):
        print(f"⚠ Criando pasta ausente: {target_path}")
        os.makedirs(target_path)

    if not os.path.isfile(icon_path):
        print(f"❌ Ícone '{icon_path}' não encontrado.")
        return

    # GUID fixo ou salvo
    guid = str(uuid.uuid4()).upper()
    guid_str = f"{{{guid}}}"
    print(f"📌 Usando GUID: {guid_str}")

    # Caminhos
    clsid_path = fr"Software\Classes\CLSID\{guid_str}"
    shell_folder_path = fr"{clsid_path}\ShellFolder"
    instance_path = fr"{clsid_path}\Instance"
    init_property_bag_path = fr"{instance_path}\InitPropertyBag"
    namespace_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{guid_str}"
    hide_icons_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel"

    try:
        # CLSID principal
        with reg.CreateKey(reg.HKEY_CURRENT_USER, clsid_path) as key:
            reg.SetValueEx(key, None, 0, reg.REG_SZ, name)
            reg.SetValueEx(key, "System.IsPinnedToNameSpaceTree", 0, reg.REG_DWORD, 1)
            reg.SetValueEx(key, "SortOrderIndex", 0, reg.REG_DWORD, 66)
            reg.SetValueEx(key, "DefaultIcon", 0, reg.REG_SZ, icon_path)

        # ShellFolder
        with reg.CreateKey(reg.HKEY_CURRENT_USER, shell_folder_path) as shell_key:
            reg.SetValueEx(shell_key, "Attributes", 0, reg.REG_DWORD, 0xf080004d)
            reg.SetValueEx(shell_key, "FolderValueFlags", 0, reg.REG_DWORD, 0x28)

        # Instance
        with reg.CreateKey(reg.HKEY_CURRENT_USER, instance_path) as instance_key:
            reg.SetValueEx(instance_key, "CLSID", 0, reg.REG_SZ, "{0E5AAE11-A475-4C5B-AB00-C66DE400274E}")

        with reg.CreateKey(reg.HKEY_CURRENT_USER, init_property_bag_path) as init_key:
            reg.SetValueEx(init_key, "TargetFolderPath", 0, reg.REG_SZ, target_path)

        # Namespace
        with reg.CreateKey(reg.HKEY_CURRENT_USER, namespace_path) as ns_key:
            reg.SetValueEx(ns_key, None, 0, reg.REG_SZ, name)

        # Mostrar ícone na área de trabalho (oculto = 0)
        with reg.CreateKey(reg.HKEY_CURRENT_USER, hide_icons_path) as hide_key:
            reg.SetValueEx(hide_key, guid_str, 0, reg.REG_DWORD, 0)

        print("✅ Pasta personalizada adicionada com ícone!")
        print("🔄 Reiniciando o Explorer...")
        restart_explorer()

    except PermissionError:
        print("❌ Permissão negada. Execute como administrador.")

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
        sys.exit()

    # PERSONALIZE AQUI 👇
    nome_da_pasta = "Meus Projetos"
    caminho_da_pasta = r"C:\MeusProjetos"
    caminho_do_icone = r"C:\MeusProjetos\OneDrive_23654.ico"  # Caminho absoluto do ícone .ico

    add_custom_folder(nome_da_pasta, caminho_da_pasta, caminho_do_icone)
