import os
import shutil
import ctypes
import sys
from tkinter import messagebox
import subprocess


def borrarCache():
    ruta = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google","Chrome","User Data")

    # Verifica si el script se está ejecutando con permisos de administrador
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Reiniciando con permisos de administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    try:
        shutil.rmtree(ruta)  # Borra la carpeta y todo su contenido
        messagebox.showinfo("Exito", "El cache de Google ha sido borrado")
        
    except FileNotFoundError:
        
        messagebox.showwarning("Cuidado", "Parece que no hay cache")
    except PermissionError:
       
        messagebox.showerror("Alerta", "Parece que no tienes permisos para ejecutar esta acción")
    except Exception as e:
        messagebox.showerror("Error","Ocurrio un error.")
        print(f"Ocurrió un error: {e}")

