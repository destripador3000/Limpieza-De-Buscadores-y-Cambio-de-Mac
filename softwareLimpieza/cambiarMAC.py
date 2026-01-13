import os
import sys
import re
import random
import subprocess
import winreg
import ctypes
import customtkinter as ctk
from tkinter import messagebox

def is_admin():
    """Verifica si el script se está ejecutando como Administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Reinicia el script con privilegios de Administrador si no los tiene."""
    if not is_admin():
        
        script = sys.argv[0]
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()

def get_network_adapters():
    """Obtiene la lista de adaptadores de red con sus nombres e índices."""
    adapters = []
    result = subprocess.run(["wmic", "nic", "get", "Index,NetConnectionID"], capture_output=True, text=True)
    for line in result.stdout.split("\n")[1:]:
        parts = line.strip().split()
        if len(parts) >= 2:
            adapters.append((parts[0], " ".join(parts[1:])))
    return adapters

def generate_mac():
    """Genera una dirección MAC válida con el bit de local administrado activado."""
    mac = [0x02] + [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join(f"{octet:02X}" for octet in mac)

def set_mac(adapter_index, new_mac):
    """Modifica la MAC Address en el Registro de Windows."""
    key_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
    
    for i in range(100):  # Normalmente hay menos de 100 adaptadores
        try:
            reg_path = f"{key_path}\\{i:04d}"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    name, _ = winreg.QueryValueEx(key, "DriverDesc")
                    if str(adapter_index) in name:
                        winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac.replace(":", ""))
                        return True
                except FileNotFoundError:
                    continue
        except PermissionError:
            messagebox.showerror("❌ Error", "No tienes permisos para modificar el Registro de Windows.")
            return False
    print(f"No se encontró la clave de registro para el adaptador con índice {adapter_index}.")
    return False

def restart_adapter(adapter_name):
    """Reinicia el adaptador de red para aplicar los cambios."""
    subprocess.run(["netsh", "interface", "set", "interface", f'"{adapter_name}"', "admin=disable"], shell=True)
    subprocess.run(["netsh", "interface", "set", "interface", f'"{adapter_name}"', "admin=enable"], shell=True)

def cambiarMac():
    run_as_admin()  
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Cambiar Dirección MAC")
    root.geometry("400x300")
    
    label = ctk.CTkLabel(root, text="🔍 Detectando adaptadores de red...", font=("Arial", 12))
    label.pack(pady=10)
    
    adapters = get_network_adapters()
    
    if not adapters:
        messagebox.showwarning("⚠️ Advertencia", "No se encontraron adaptadores de red.")
        return
    
    adapter_var = ctk.StringVar()
    adapter_var.set(adapters[0][1])
    adapter_menu = ctk.CTkOptionMenu(root, variable=adapter_var, values=[name for _, name in adapters])
    adapter_menu.pack(pady=10)
    
    def change_mac():
        selected_adapter_name = adapter_var.get()
        adapter_index = [index for index, name in adapters if name == selected_adapter_name][0]
        new_mac = generate_mac()
        if set_mac(adapter_index, new_mac):
            restart_adapter(selected_adapter_name)
            messagebox.showinfo("✅ Éxito", f"MAC cambiada con éxito a {new_mac}")
        else:
            messagebox.showerror("❌ Error", "No se pudo cambiar la MAC. Es posible que el adaptador no lo permita.")
    
    change_button = ctk.CTkButton(root, text="Cambiar MAC", command=change_mac)
    change_button.pack(pady=10)
    
    root.mainloop()

