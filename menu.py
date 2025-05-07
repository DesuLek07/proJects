import customtkinter as ctk
import webbrowser
from PIL import Image
from ventana_base import ventana_principal

# Ruta de la imagen
ruta_fondo = r'C:\Users\DesuLek\Desktop\SRPP\styles\wp.jpg'

# Cargar la imagen con PIL
imagen_fondo = Image.open(ruta_fondo)

# Crear el objeto CTkImage
imagen_fondo_ctk = ctk.CTkImage(light_image=imagen_fondo, dark_image=imagen_fondo, size=(1200, 650))

# Funciones de botones
def github():
    webbrowser.open('https://github.com/DesuLek07/proJects/tree/helpdesk#')
def patreon():  
    webbrowser.open('https://patreon.com/DesuLek07')

class ventana_menu(ventana_principal):
    def __init__(self):
            super().__init__(
            titulo='SRPP',
            tamaño=(1200, 650, 70, 25),
            tema='dark',
            minimo=(1200, 650),
            maximo=(1200, 650))
            
            self.construir_interfaz()

    def enviar_a_sesion(self):
        from sesion import ventana_sesion
        self.root.withdraw()
        sesion = ventana_sesion(menu_ref=self, imagen_fondo_ctk=imagen_fondo_ctk)
        sesion.lanzar()

    def enviar_a_registro(self):   
        from registro import ventana_registro
        self.root.withdraw() 
        self.registro_ventana = ventana_registro(self)
        self.registro_ventana.lanzar()

    def mostrar_ventana(self):
        self.root.deiconify()

    def construir_interfaz(self):
            # Fondo de la ventana
            fondo = ctk.CTkLabel(self.root, image=imagen_fondo_ctk, text='')
            fondo.place(x=0, y=0, relwidth=1, relheight=1)

            # Contenedor 1
            frame1 = ctk.CTkFrame(self.root, width=570, 
                            height=460, 
                            fg_color='gray17', 
                            corner_radius=20, 
                            bg_color='black')
        
            frame1.place(relx=0.5, rely=0.5, anchor='center')

            # Contenedor 2
            frame2 = ctk.CTkFrame(frame1, width=540, 
                            height=430, 
                            fg_color='gray22', 
                            corner_radius=20, 
                            bg_color='gray17')
        
            frame2.place(relx=0.5, rely=0.5, anchor='center')

            # Fondo 2
            fondo2 = ctk.CTkLabel(frame2, image=imagen_fondo_ctk, text='')
            fondo2.place(x=0, y=0, relwidth=1, relheight=1)

            # Label 1
            label1 = ctk.CTkLabel(frame2, text='Mesa de ayuda SRPP', 
                            font=ctk.CTkFont(32, weight='bold', size=25),
                            corner_radius=10,
                            fg_color='gray3',
                            text_color='snow',
                            bg_color='black')
        
            label1.place(relx=0.5, rely=0.15, anchor='center')

            # Boton de Registro
            Boton1 = ctk.CTkButton(frame2, text='Registrarse', font=ctk.CTkFont(32, weight='bold', size=20),
                            corner_radius=20,
                            fg_color='gray5',
                            text_color='snow',
                            bg_color='gray5',
                            hover_color='gray18',
                            command=self.enviar_a_registro)
        
            Boton1.place(relx=0.5, rely=0.4, anchor='center')

            # Boton de sesion
            Boton2 = ctk.CTkButton(frame2, text='Iniciar Sesion', font=ctk.CTkFont(32, weight='bold', size=20),
                            corner_radius=20,
                            fg_color='gray5',
                            text_color='snow',
                            bg_color='black',
                            hover_color='gray17',
                            command=self.enviar_a_sesion)
        
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
                            fg_color='gray5',
                            text_color='snow',
                            bg_color='gray5',
                            hover_color='gray17',
                            command=github)
        
            Boton4.place(relx=0.95, rely=0.85, anchor='se')

            # Boton salida segura
            Boton5 = ctk.CTkButton(self.root, text='Salida segura', font=ctk.CTkFont(32, weight='bold', size=12),
                                   corner_radius=20,
                                   fg_color='red3',
                                   bg_color='black',
                                   command=exit)
            Boton5.place(relx=0.95, rely=0.95, anchor='e')

if __name__ == "__main__":
    menu = ventana_menu()
    menu.iniciar_ventana()
