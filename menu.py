import customtkinter as ctk
import webbrowser
from PIL import Image
from sesion import lanzar_inicio_sesion
from register import lanzar_registro

ruta_imagen = r'C:\Users\DesuLek\Documents\Python\Proyecto_Integrador\styles\wp.jpg'

def github():
    webbrowser.open('https://github.com/DesuLek07/proJects.git')
def patreon():
    webbrowser.open('https://patreon.com/DesuLek07?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink')

def ventana_principal():

    # Funcion Anidada1
    def abrir_registro():
        ventana.destroy()
        lanzar_registro()

    # Funcion Anidada2
    def abrir_inicio_Sesion():
        ventana.destroy()
        lanzar_inicio_sesion()

    # Atributos de la ventana
    ventana = ctk.CTk()
    ventana.title('SRPPM')
    ventana.geometry('1200x650+70+25')
    ventana._set_appearance_mode('dark')
    ventana.minsize(1200,650)
    ventana.maxsize(1200,650)

    # Fondo de la ventana
    imagen_pil = Image.open(ruta_imagen)
    imagen_fondo = ctk.CTkImage(light_image=imagen_pil, 
                                dark_image=imagen_pil, 
                                size=(1200, 650))
    fondo = ctk.CTkLabel(ventana, 
                         image=imagen_fondo)
    
    fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Contenedor 1
    frame1 = ctk.CTkFrame(ventana, width=570, 
                          height=460, 
                          fg_color='gray17', 
                          corner_radius=20, 
                          bg_color='black')
    
    frame1.place(relx=0.5, rely=0.5, anchor='center')

    # Contenedor 2
    frame2 = ctk.CTkFrame(ventana, width=540, 
                          height=430, 
                          fg_color='gray22', 
                          corner_radius=20, 
                          bg_color='gray17')
    
    frame2.place(relx=0.5, rely=0.5, anchor='center')

    # Fondo 2
    fondo2 = ctk.CTkLabel(frame2, image=imagen_fondo, text='')
    fondo2.place(x=0, y=0, relwidth=1, relheight=1)

    # Label 1
    label1 = ctk.CTkLabel(frame2, text='Sistema de Restitucion y Reparacion\n-Helpdesk-', 
                          font=ctk.CTkFont(32, weight='bold', size=25),
                          corner_radius=10,
                          fg_color='gray10',
                          text_color='snow',
                          bg_color='black')
    
    label1.place(relx=0.5, rely=0.15, anchor='center')

    # Boton de Registro
    Boton1 = ctk.CTkButton(frame2, text='Registrarse', font=ctk.CTkFont(32, weight='bold', size=20),
                           corner_radius=20,
                           fg_color='transparent',
                           text_color='snow',
                           bg_color='transparent',
                           command=abrir_registro)
    
    Boton1.place(relx=0.5, rely=0.4, anchor='center')

    # Boton de sesion
    Boton2 = ctk.CTkButton(frame2, text='Iniciar Sesion', font=ctk.CTkFont(32, weight='bold', size=20),
                           corner_radius=20,
                           fg_color='SkyBlue4',
                           text_color='snow',
                           bg_color='black',
                           command=abrir_inicio_Sesion)
    
    Boton2.place(relx=0.5, rely=0.6, anchor='center')

     # Boton de patreon
    Boton3 = ctk.CTkButton(frame2, text='Apoyar patreon', font=ctk.CTkFont(32, weight='bold', size=16),
                           corner_radius=20,
                           fg_color='red3',
                           text_color='snow',
                           bg_color='black',
                           command=patreon)
    
    Boton3.place(relx=0.95, rely=0.95, anchor='se')

    # Boton de github
    Boton4 = ctk.CTkButton(frame2, text='GitHub', font=ctk.CTkFont(32, weight='bold', size=16),
                           corner_radius=20,
                           fg_color='transparent',
                           text_color='snow',
                           bg_color='transparent',
                           command=github)
    
    Boton4.place(relx=0.95, rely=0.85, anchor='se')

    # Lanzar ventana
    ventana.mainloop()

# Inicializar proyecto
if __name__ == '__main__':
    ventana_principal()