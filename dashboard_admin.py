import customtkinter as ctk
from ventana_base import ventana_principal
from backend.querys_conexion import obtener_datos_usuario, obtener_tickets_pendientes, actualizar_estado_ticket
from tkinter import messagebox

class ventana_dashboard_admin(ventana_principal):

    """
    Panel administrativo para gestionar tickets y usuarios.
    Hereda de ventana_principal y ofrece funcionalidades específicas para administradores.
    """

    def __init__(self, id_usuario, menu_ref, imagen_fondo_ctk):

        """
        Inicializa el panel del administrador con la interfaz y funcionalidades.

        Args:
            id_usuario (int): ID del usuario administrador.
            menu_ref (obj): Referencia al menú principal para mostrar/ocultar.
            imagen_fondo_ctk (obj): Imagen de fondo (opcional, aún no usada).
        """

        self.id_usuario = id_usuario
        self.menu_ref = menu_ref
        self.imagen_fondo_ctk = imagen_fondo_ctk

        super().__init__(
            titulo='Panel Administrador',
            tamaño=(1000, 550, 70, 25),
            tema='dark',
            minimo=(1000, 550),
            maximo=(1000, 550)
        )

        self.construir_interfaz()

    def construir_interfaz(self):

        """
        Construye la interfaz gráfica del panel del administrador.
        Incluye datos del usuario, barra lateral de navegación y panel de bienvenida.
        """

        # Fondo general
        self.fondo = ctk.CTkFrame(self.root, width=1000, height=550, fg_color='#1e1e2f')
        self.fondo.pack()

        # Panel de bienvenida
        self.frame_inicio = ctk.CTkFrame(self.root, width=560, height=400,
                                          fg_color='#252540', bg_color='#1e1e2f',
                                          border_width=1, border_color='#3a3a5f',
                                          corner_radius=20)
        self.frame_inicio.place(relx=0.5, rely=0.55, anchor='center')

        self.titulo = ctk.CTkLabel(self.root, text='Panel del Administrador',
                                   font=ctk.CTkFont(size=26, weight='bold'),
                                   fg_color='#1e1e2f', bg_color='#1e1e2f',
                                   text_color='light cyan')
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

        # Barra lateral
        self.frame_barra_lateral = ctk.CTkFrame(self.root, width=80, height=550,
                                                fg_color='#12121f', corner_radius=0)
        self.frame_barra_lateral.place(relx=0, rely=0, anchor='nw')

        estilo_boton = {
            "width": 50,
            "height": 50,
            "fg_color": "#3e4a89",
            "hover_color": "#5065b1",
            "corner_radius": 15,
            "text_color": "white",
            "font": ctk.CTkFont(size=20, weight="bold")
        }

        # Botones barra lateral
        self.boton_ver_tickets = ctk.CTkButton(self.frame_barra_lateral,
                                               text='📂', command=self.abrir_tickets_pendientes,
                                               **estilo_boton)
        self.boton_ver_tickets.place(relx=0.5, rely=0.05, anchor='center')

        self.boton_gestionar_usuarios = ctk.CTkButton(self.frame_barra_lateral,
                                                      text='👥', command=self.gestionar_usuarios,
                                                      **estilo_boton)
        self.boton_gestionar_usuarios.place(relx=0.5, rely=0.15, anchor='center')

        self.boton_estadisticas = ctk.CTkButton(self.frame_barra_lateral,
                                                text='📊', command=self.mostrar_estadisticas,
                                                **estilo_boton)
        self.boton_estadisticas.place(relx=0.5, rely=0.25, anchor='center')

    def abrir_tickets_pendientes(self):

        """
        Abre una ventana emergente que muestra todos los tickets pendientes.
        Permite al administrador ver detalles y actualizar estado/prioridad/mensaje del ticket.
        """

        tickets = obtener_tickets_pendientes()

        ventana_tickets = ctk.CTkToplevel(self.root)
        ventana_tickets.title("Tickets Pendientes")
        ventana_tickets.geometry("650x500")
        ventana_tickets.resizable(False, False)

        if not tickets:
            ctk.CTkLabel(ventana_tickets, text="No hay tickets pendientes.",
                     font=ctk.CTkFont(size=14)).pack(pady=20)
            return

        for ticket in tickets:
            frame = ctk.CTkFrame(ventana_tickets, fg_color="#2c2c2c", corner_radius=10)
            frame.pack(pady=8, padx=20, fill="x")

            ctk.CTkLabel(frame, text=f"ID: {ticket[0]} | Título: {ticket[1]}",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(frame, text=f"Usuario: {ticket[5]} {ticket[6]} | Prioridad: {ticket[4]}",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(frame, text=f"Descripción: {ticket[2][:100]}...",
                     font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=2)

            # Botón para expandir
            def expandir_ticket(ticket=ticket):
                ventana_expandida = ctk.CTkToplevel(ventana_tickets)
                ventana_expandida.title(f"Detalles del Ticket {ticket[0]}")
                ventana_expandida.geometry("450x500")
                ventana_expandida.resizable(False, False)
                
                ctk.CTkLabel(ventana_expandida, text=f"Título: {ticket[1]}", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
                ctk.CTkLabel(ventana_expandida, text=f"Descripción: {ticket[2]}", font=ctk.CTkFont(size=12), wraplength=400).pack(pady=5)
                ctk.CTkLabel(ventana_expandida, text=f"Estado: {ticket[3]}", font=ctk.CTkFont(size=12)).pack(pady=5)
                ctk.CTkLabel(ventana_expandida, text=f"Prioridad: {ticket[4]}", font=ctk.CTkFont(size=12)).pack(pady=5)
                ctk.CTkLabel(ventana_expandida, text="Mensaje al usuario:", font=ctk.CTkFont(size=12)).pack()

                entrada_respuesta = ctk.CTkTextbox(ventana_expandida, height=80, width=300)
                entrada_respuesta.pack(pady=5)

                # Cambiar estado y prioridad
                estado_var = ctk.StringVar(value=ticket[3])
                prioridad_var = ctk.StringVar(value=ticket[4])

                estado_menu = ctk.CTkOptionMenu(ventana_expandida, variable=estado_var, values=["pendiente", "en proceso", "resuelto"])
                estado_menu.pack(pady=10)

                prioridad_menu = ctk.CTkOptionMenu(ventana_expandida, variable=prioridad_var, values=["baja", "media", "alta"])
                prioridad_menu.pack(pady=10)

                def actualizar_ticket():
                    nuevo_estado = estado_var.get()
                    nueva_prioridad = prioridad_var.get()
                    mensaje = entrada_respuesta.get("1.0", "end").strip()
                    resultado = actualizar_estado_ticket(ticket[0], nuevo_estado, nueva_prioridad)
                    if resultado:
                        if mensaje:
                            from backend.querys_conexion import guardar_respuesta_ticket
                            guardar_respuesta_ticket(ticket[0], self.id_usuario, mensaje)
                        messagebox.showinfo("Actualización exitosa", "Ticket actualizado y mensaje enviado.")
                        ventana_expandida.destroy()
                    else:
                        messagebox.showerror("Error", "Hubo un problema al actualizar el ticket.")

                # Botón para guardar cambios
                ctk.CTkButton(ventana_expandida, text="Actualizar", command=actualizar_ticket).pack(pady=10)

            ctk.CTkButton(frame, text="Ver detalles", command=expandir_ticket).pack(pady=5)

    def gestionar_usuarios(self):

        """
        Muestra un mensaje informando que la funcionalidad de gestión de usuarios
        está en desarrollo.
        """

        messagebox.showinfo("Gestión de usuarios", "Aquí se mostrará la gestión de usuarios (en desarrollo).")

    def mostrar_estadisticas(self):

        """
        Muestra un mensaje informando que la funcionalidad de estadísticas
        está en desarrollo.
        """

        messagebox.showinfo("Estadísticas", "Aquí se mostrarán estadísticas del sistema (en desarrollo).")

    def lanzar(self):

        """
        Inicia el bucle principal de la ventana del panel administrador.
        """

        self.iniciar_ventana()
