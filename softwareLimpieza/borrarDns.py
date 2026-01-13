import os
from tkinter import messagebox
import subprocess

def eliminarDNS():
    try:
        subprocess.run("ipconfig /flushdns", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run("ipconfig /release", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run("ipconfig /renew", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

        
        messagebox.showinfo("Eliminación DNS", "Las DNS de su equipo se eliminaron con éxito.")
    except:
        messagebox.showerror("Error", "Acaba de ocurrir un error")

  