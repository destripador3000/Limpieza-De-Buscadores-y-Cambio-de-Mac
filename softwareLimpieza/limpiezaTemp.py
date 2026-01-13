import os
import ctypes
import sys
import shutil
from tkinter import messagebox

def ejecutar_como_admin():
    """Reinicia el script con permisos de administrador si no los tiene."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Reiniciando con permisos de administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()  

def eliminarArchivos():
    """Elimina archivos y carpetas temporales en Windows con permisos elevados."""
    ejecutar_como_admin()  

    try:
        ruta = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Temp")
        archivos = os.listdir(ruta)  

        for archivo in archivos:
            ruta_completa = os.path.join(ruta, archivo)

            try:
                # Cambiar permisos antes de eliminar
                os.chmod(ruta_completa, 0o777)

                if os.path.isfile(ruta_completa):
                    os.remove(ruta_completa)
                    print(f"Eliminado: {ruta_completa}")

                elif os.path.isdir(ruta_completa):
                    shutil.rmtree(ruta_completa, ignore_errors=True)  # Elimina carpetas con contenido
                    print(f"Carpeta eliminada: {ruta_completa}")

            except Exception as e:
                print(f"Error eliminando {ruta_completa}: {e}")

        messagebox.showinfo("Genial!", "Archivos eliminados con éxito.")

    except FileNotFoundError:
        messagebox.showwarning("Cuidado", "Uno o más archivos no fueron encontrados.")
    except PermissionError:
        messagebox.showerror("Error", "No tienes permisos para eliminar algunos archivos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


