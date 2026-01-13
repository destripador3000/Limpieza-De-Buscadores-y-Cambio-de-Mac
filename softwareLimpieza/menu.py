import customtkinter as ctk
from limpiezaTemp import eliminarArchivos
from borrarDns import eliminarDNS
from borrarCacheGoogle import borrarCache
from limpiezSistema import limpiezDeSistema
from cambiarMAC import cambiarMac

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

ventana=ctk.CTk()
ventana.title("Limpiador")
ventana.geometry("400x450px")
ventana.resizable(False, False) 
boton=ctk.CTkButton(ventana, text="Iniciar programa", width=150, height=30,command=lambda:(eliminarArchivos(),eliminarDNS(),borrarCache(), limpiezDeSistema()))
boton.place(x=130, y=100)

boton=ctk.CTkButton(ventana, text="Cambiar MAC",width=150, height=30, command=cambiarMac)
boton.place(x=130, y=300)



ventana.mainloop()