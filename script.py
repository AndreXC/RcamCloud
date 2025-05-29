# import winreg as reg
# import uuid
# import os
# import ctypes
# import subprocess

# def restart_explorer():
#     subprocess.run("taskkill /f /im explorer.exe", shell=True)
#     subprocess.run("start explorer.exe", shell=True)

# def add_custom_folder(name, target_path):
#     if not os.path.exists(target_path):
#         print(f"Erro: o caminho '{target_path}' não existe.")
#         return

#     # GUID fixo para facilitar testes (pode ser alterado para uuid.uuid4())
#     guid = str(uuid.uuid4()).upper()
#     guid_str = f"{{{guid}}}"
#     print(f"Usando GUID: {guid_str}")

#     # Caminho no registro
#     base_clsid = fr"Software\Classes\CLSID\{guid_str}"
#     shell_folder_path = fr"Software\Classes\CLSID\{guid_str}\ShellFolder"
#     namespace_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{guid_str}"

#     try:
#         # CLSID
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, base_clsid) as key:
#             reg.SetValueEx(key, None, 0, reg.REG_SZ, name)
#             reg.SetValueEx(key, "System.IsPinnedToNameSpaceTree", 0, reg.REG_SZ, "1")

#         # ShellFolder
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, shell_folder_path) as shell_key:
#             # Valor que define visibilidade no painel lateral
#             reg.SetValueEx(shell_key, "Attributes", 0, reg.REG_DWORD, 0xf080004d)

#         # DefaultIcon (opcional)
#         # icon_path = r"C:\Windows\System32\shell32.dll,3"
#         # reg.SetValueEx(key, "DefaultIcon", 0, reg.REG_SZ, icon_path)

#         # Instance e InitPropertyBag
#         instance_path = base_clsid + r"\Instance"
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, instance_path) as instance_key:
#             reg.SetValueEx(instance_key, "CLSID", 0, reg.REG_SZ, "{0E5AAE11-A475-4c5b-AB00-C66DE400274E}")

#         init_path = instance_path + r"\InitPropertyBag"
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, init_path) as init_key:
#             reg.SetValueEx(init_key, "TargetFolderPath", 0, reg.REG_SZ, target_path)

#         # Adiciona ao painel de navegação
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, namespace_path) as ns_key:
#             reg.SetValueEx(ns_key, None, 0, reg.REG_SZ, name)

#         print("✔ Pasta adicionada com sucesso!")
#         print("🔄 Reiniciando o Windows Explorer para aplicar...")
#         restart_explorer()

#     except PermissionError:
#         print("❌ Erro: execute o script como administrador.")

# # 👇 Customize aqui:
# nome_da_pasta = "Meus Projetos"
# caminho = r"C:\MeusProjetos"

# add_custom_folder(nome_da_pasta, caminho)


# import os
# import sys
# import ctypes
# import winreg as reg
# import uuid
# import subprocess

# def is_admin():
#     """Verifica se o script está rodando como administrador."""
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# def run_as_admin():
#     """Reexecuta o script com privilégios elevados (UAC)."""
#     script = os.path.abspath(sys.argv[0])
#     params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)

# def restart_explorer():
#     subprocess.run("taskkill /f /im explorer.exe", shell=True)
#     subprocess.run("start explorer.exe", shell=True)

# def add_custom_folder(name, target_path):
#     if not os.path.exists(target_path):
#         print(f"Erro: o caminho '{target_path}' não existe.")
#         return

#     # GUID fixo para facilitar testes (pode ser alterado para uuid.uuid4())
#     guid = str(uuid.uuid4()).upper()
#     guid_str = f"{{{guid}}}"
#     print(f"Usando GUID: {guid_str}")

#     # Caminho no registro
#     base_clsid = fr"Software\Classes\CLSID\{guid_str}"
#     shell_folder_path = fr"Software\Classes\CLSID\{guid_str}\ShellFolder"
#     namespace_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{guid_str}"

#     try:
#         # CLSID
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, base_clsid) as key:
#             reg.SetValueEx(key, None, 0, reg.REG_SZ, name)
#             reg.SetValueEx(key, "System.IsPinnedToNameSpaceTree", 0, reg.REG_SZ, "1")

#         # ShellFolder
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, shell_folder_path) as shell_key:
#             reg.SetValueEx(shell_key, "Attributes", 0, reg.REG_DWORD, 0xf080004d)

#         # Instance
#         instance_path = base_clsid + r"\Instance"
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, instance_path) as instance_key:
#             reg.SetValueEx(instance_key, "CLSID", 0, reg.REG_SZ, "{0E5AAE11-A475-4c5b-AB00-C66DE400274E}")

#         init_path = instance_path + r"\InitPropertyBag"
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, init_path) as init_key:
#             reg.SetValueEx(init_key, "TargetFolderPath", 0, reg.REG_SZ, target_path)

#         # Adiciona ao painel de navegação
#         with reg.CreateKey(reg.HKEY_CURRENT_USER, namespace_path) as ns_key:
#             reg.SetValueEx(ns_key, None, 0, reg.REG_SZ, name)

#         print("✔ Pasta adicionada com sucesso!")
#         print("🔄 Reiniciando o Windows Explorer para aplicar...")
#         restart_explorer()

#     except PermissionError:
#         print("❌ Erro: execute o script como administrador.")

# # 🚀 Execução segura com UAC
# if __name__ == "__main__":
#     if not is_admin():
#         print("Solicitando privilégios de administrador...")
#         run_as_admin()
#         sys.exit()

#     # 👇 Personalize aqui:
#     nome_da_pasta = "Meus Projetos"
#     caminho = r"C:\MeusProjetos"

#     add_custom_folder(nome_da_pasta, caminho)



import os
import sys
import ctypes
import winreg as reg
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)

def restart_explorer():
    subprocess.run("taskkill /f /im explorer.exe", shell=True)
    subprocess.run("start explorer.exe", shell=True)

def delete_registry_tree(root, subkey):
    try:
        with reg.OpenKey(root, subkey, 0, reg.KEY_READ | reg.KEY_WRITE) as key:
            i = 0
            while True:
                try:
                    sub = reg.EnumKey(key, i)
                    delete_registry_tree(root, f"{subkey}\\{sub}")
                except OSError:
                    break
        reg.DeleteKey(root, subkey)
        print(f"🗑 Removido: {subkey}")
    except FileNotFoundError:
        print(f"⚠ Não encontrado: {subkey}")
    except PermissionError:
        print(f"❌ Permissão negada para remover: {subkey}")

def remove_custom_folder(guid_str):
    base_clsid = fr"Software\Classes\CLSID\{guid_str}"
    namespace_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace\{guid_str}"

    delete_registry_tree(reg.HKEY_CURRENT_USER, namespace_path)
    delete_registry_tree(reg.HKEY_CURRENT_USER, base_clsid)

    print("✔ Remoção concluída.")
    print("🔄 Reiniciando o Windows Explorer para aplicar...")
    restart_explorer()

# 🧠 Substitua abaixo pelo GUID que foi usado na criação (sem as chaves extras)
guid = "D925F12A-2494-41AE-ABD6-9FDCD67EEF8D"  # <-- coloque seu GUID aqui

if __name__ == "__main__":
    if not is_admin():
        print("Solicitando privilégios de administrador...")
        run_as_admin()
        sys.exit()

    remove_custom_folder(f"{{{guid}}}")
