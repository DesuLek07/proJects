import customtkinter as ctk
from ventana_base import ventana_principal
from backend.querys_conexion import obtener_datos_usuario
from tkinter import messagebox

class ventana_dashboard(ventana_principal):
    def __init__(self, id_usuario, menu_ref, imagen_fondo_ctk=None):
        self.id_usuario = id_usuario
        self.menu_ref = menu_ref  
        self.imagen_fondo_ctk = imagen_fondo_ctk

        super().__init__(
            titulo='Dashboard', 
            tamaño=(1000, 550, 70, 25), 
            tema='dark', 
            minimo=(1000, 550), 
            maximo=(1000, 500)
        )

        self.construir_interfaz()

    def volver_ventana_principal(self):
        self.root.deiconify()
        if self.menu_ref:
            self.menu_ref.mostrar_ventana()

    def construir_interfaz(self):
        # Fondo de la ventana
        #fondo = ctk.CTkLabel(self.root, image=self.imagen_fondo_ctk, text='')
        #fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Contenedor fondo
        self.fondo = ctk.CTkFrame(self.root, width=1000, height=550,
                                  fg_color='dark slate blue')
        self.fondo.pack()

        # Contenedor de bienvenida y datos del usuario
        self.frame_inicio = ctk.CTkFrame(self.root, width=560, height=400,
                                         fg_color='#1e1e1e',
                                         bg_color='dark slate blue',
                                         border_width=0,
                                         corner_radius=20)
        self.frame_inicio.place(relx=0.5, rely=0.55, anchor='center')

        # Titulo
        self.titulo = ctk.CTkLabel(self.root, text='¡Bienvenido!', 
                                   font=ctk.CTkFont(size=24, weight='bold'),
                                   fg_color='gray17',
                                   bg_color='dark slate blue',
                                   text_color='snow',
                                   corner_radius=20)
        self.titulo.place(relx=0.5, rely=0.1, anchor='center')

        # Datos del usuario
        datos = obtener_datos_usuario(self.id_usuario)
        if datos:
            etiquetas = [
                "Nombre", "Segundo Nombre", "Apellido", "Segundo Apellido",
                "Tipo ID", "Número ID", "Correo", "Teléfono 1", "Teléfono 2"
            ]
            
            for i, campo in enumerate(etiquetas):
                ctk.CTkLabel(self.frame_inicio,
                             text=f"{campo}: {datos[i] if datos[i] else 'N/A'}",
                             font=ctk.CTkFont(size=14),
                             text_color="white").pack(anchor="w", padx=20, pady=2)
        else:
            ctk.CTkLabel(self.frame_inicio, text="No se encontraron datos.",
                         font=ctk.CTkFont(size=14),
                         text_color="white").pack(anchor="w", padx=20, pady=10)

        # Contenedor barra lateral
        self.frame_barra_lateral = ctk.CTkFrame(self.root,
                                                width=80, height=550,
                                                fg_color='gray17',
                                                corner_radius=0)
        self.frame_barra_lateral.place(relx=0, rely=0, anchor='nw')
        
        # Boton ir al inicio de usuario
        self.info_usuario = ctk.CTkButton(self.frame_barra_lateral,
                                          text='👤', command=self.mostrar_info_usuario, width=40)
        self.info_usuario.place(relx=0.5, rely=0.05, anchor='center')

    def mostrar_info_usuario(self):
        messagebox.showinfo("Información del usuario", f"ID de usuario: {self.id_usuario}")

    def lanzar(self):
        self.iniciar_ventana()
