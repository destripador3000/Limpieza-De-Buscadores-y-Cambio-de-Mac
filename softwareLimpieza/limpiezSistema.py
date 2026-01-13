import os
import sys
import ctypes
from tkinter import messagebox

def limpiezDeSistema():
    try:
        # Verificar si el script tiene permisos de administrador
        if ctypes.windll.shell32.IsUserAnAdmin():
            os.system("netsh int ip reset")
            os.system("cleanmgr /sagerun:1")
            os.system("netsh winsock reset")
            
            messagebox.showinfo("Limpieza de Sistema", "La limpieza de su sistema se hizo con éxito.")
        else:
            # Si no tiene permisos, reiniciarlo con privilegios de administrador
            messagebox.showwarning("Permiso requerido", "Este programa necesita ejecutarse como administrador.")
            script = sys.argv[0]
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
            sys.exit()
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


