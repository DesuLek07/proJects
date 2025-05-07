import customtkinter as ctk
from tkinter import messagebox
from backend.querys_conexion import verificar
from ventana_base import ventana_principal
from dashboard_usuario import ventana_dashboard 
from dashboard_admin import ventana_dashboard_admin

class ventana_sesion(ventana_principal):

    """
    Ventana de inicio de sesión para la aplicación SRPP.

    Esta clase maneja la interfaz de inicio de sesión, permitiendo a los usuarios 
    ingresar su nombre de usuario y contraseña, verificando su autenticidad y 
    redirigiéndolos a la pantalla correspondiente dependiendo de su rol (administrador o usuario).

    Args:
        menu_ref: Referencia a la ventana principal del menú.
        imagen_fondo_ctk: Imagen de fondo de la interfaz.

    Methods:
        volver_ventana_principal: Vuelve a la ventana principal.
        construir_interfaz: Construye y organiza los widgets de la interfaz gráfica.
        login: Realiza la verificación del usuario y contraseña, y redirige según el rol.
        lanzar: Inicia la ventana de inicio de sesión.
    """

    def __init__(self, menu_ref, imagen_fondo_ctk):

        """
        Inicializa la ventana de inicio de sesión.

        Args:
            menu_ref: Referencia a la ventana principal del menú.
            imagen_fondo_ctk: Imagen de fondo de la interfaz.
        """

        self.menu_ref = menu_ref
        self.imagen_fondo_ctk = imagen_fondo_ctk
        super().__init__(
            titulo='SRPP SESION',
            tamaño=(400, 300, 70, 25),
            tema='dark',
            minimo=(400, 300),
            maximo=(400, 300))
        self.construir_interfaz()

    def volver_ventana_principal(self):

        """
        Oculta la ventana de inicio de sesión y vuelve a mostrar la ventana principal.
        """

        self.root.withdraw()
        self.menu_ref.mostrar_ventana()

    def construir_interfaz(self):

        """
        Construye la interfaz gráfica de la ventana de inicio de sesión.

        Aquí se organizan los componentes como los campos de texto para el usuario y la contraseña,
        los botones y las etiquetas.
        """

        # Contenedor
        frame1 = ctk.CTkFrame(self.root, 
                              width=360, 
                              height=270, 
                              corner_radius=20, 
                              fg_color='gray17')
        frame1.place(relx=0.05, rely=0.5, anchor='w')

        # Titulo
        label1 = ctk.CTkLabel(frame1, text='Inicio de Sesion', 
                              font=ctk.CTkFont(32, weight='bold'),
                              corner_radius=20,
                              fg_color='azure3',
                              text_color='black')
        label1.place(relx=0.5, rely=0.15, anchor='center')

        # Entrada username
        entrada_usuario = ctk.CTkEntry(frame1, placeholder_text='Usuario')
        entrada_usuario.place(relx=0.5, rely=0.45, anchor='center')

        # Entrada contraseña
        entrada_contraseña = ctk.CTkEntry(frame1, placeholder_text='Contraseña', show='*')
        entrada_contraseña.place(relx=0.5, rely=0.6, anchor='center')

        # Comprobacion login
        def login():

            """
            Verifica el nombre de usuario y la contraseña ingresada.

            Si los campos están vacíos, muestra un error. Si la verificación es exitosa, 
            redirige a la ventana correspondiente según el rol del usuario.
            """

            campos = [entrada_usuario.get(), entrada_contraseña.get()]
    
            if any(campo.strip() == '' for campo in campos):
                messagebox.showerror('Campos incompletos', 'Recuerde completar todos los campos para iniciar sesión')
                return

            usuario = entrada_usuario.get()
            contraseña = entrada_contraseña.get()

            id_usuario, rol = verificar(usuario, contraseña)

            if id_usuario:
                messagebox.showinfo('Login exitoso', 'Bienvenido')

                self.root.withdraw()

                # Redirigir según el rol
                if rol == 'administrador':
                    # Pasar los tres parámetros necesarios
                    dashboard_administrador = ventana_dashboard_admin(id_usuario, menu_ref=self.menu_ref, imagen_fondo_ctk=self.imagen_fondo_ctk)
                    dashboard_administrador.lanzar()
                else:
                    dashboard_usuario = ventana_dashboard(id_usuario, menu_ref=self.menu_ref, imagen_fondo_ctk=self.imagen_fondo_ctk)
                    dashboard_usuario.lanzar()

            else:
                messagebox.showerror('Error', 'Usuario o contraseña incorrectos')

        # Boton de ingreso
        Boton_ingreso = ctk.CTkButton(frame1, text='Ingresar', command=login)
        Boton_ingreso.place(relx=0.5, rely=0.75, anchor='center')

        # Boton de regreso a menu
        boton1 = ctk.CTkButton(frame1, width=2, 
                               height=2, 
                               corner_radius=50, 
                               fg_color='gray19', 
                               text='Volver', text_color='black', 
                               font=ctk.CTkFont(32, weight='bold'), 
                               bg_color='gray17', command=lambda: self.volver_ventana_principal())
        boton1.place(relx=0.05, rely=0.85, anchor='nw')

        # Shortcut con tecla enter
        self.root.bind('<Return>', lambda event: login())

    def lanzar(self):

        """
        Inicia la ventana de inicio de sesión.
        """

        self.iniciar_ventana()
