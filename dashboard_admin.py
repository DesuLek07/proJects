import customtkinter as ctk
import tkinter as tk
from ventana_base import ventana_principal
from backend.querys_conexion import obtener_datos_usuario, obtener_tickets_pendientes, actualizar_estado_ticket, obtener_historial_tickets_usuario, obtener_usuarios_registrados, enviar_mensaje_chat, obtener_chat
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

        # Boton salida segura
        Boton_salida = ctk.CTkButton(self.root, text='Salida segura', font=ctk.CTkFont(32, weight='bold', size=12),
                                corner_radius=20,
                                fg_color='red3',
                                bg_color='#1e1e2f',
                                command=exit)
        Boton_salida.place(relx=0.95, rely=0.95, anchor='e')

        # Boton chat
        self.boton_chat = ctk.CTkButton(self.frame_barra_lateral,
                                text='💬', command=self.abrir_chat_con_soporte,
                                **estilo_boton)
        self.boton_chat.place(relx=0.5, rely=0.35, anchor='center')


    def abrir_chat_con_soporte(self):
        """
        Abre una ventana de chat donde el administrador puede comunicarse con el personal de soporte.
        """

        ventana_chat = ctk.CTkToplevel(self.root)
        ventana_chat.title("Chat con Soporte")
        ventana_chat.geometry("600x600")
        ventana_chat.resizable(False, False)
        ventana_chat.configure(fg_color="#202020")  # Fondo oscuro para mejor contraste

        # Título de la ventana
        ctk.CTkLabel(ventana_chat, text="Chat con Soporte", font=ctk.CTkFont(size=18, weight="bold"), text_color="light cyan").pack(pady=(20, 10))

        # Selector de soporte con descripción
        ctk.CTkLabel(ventana_chat, text="Escribe el ID del soporte destino para iniciar el chat:", font=ctk.CTkFont(size=12)).pack(pady=10)
        entrada_destinatario = ctk.CTkEntry(ventana_chat, width=350, height=30)
        entrada_destinatario.pack(pady=10)

        # Área de mensajes, configurada con una fuente y diseño más legible
        area_mensajes = ctk.CTkTextbox(ventana_chat, width=460, height=320, font=ctk.CTkFont(size=12), wrap="word")
        area_mensajes.pack(pady=(10, 15))
        area_mensajes.configure(state="disabled")  # Deshabilitar la edición directamente para evitar modificaciones no deseadas

        def cargar_chat():
            area_mensajes.configure(state="normal")
            area_mensajes.delete("1.0", "end")
            try:
                id_destino = int(entrada_destinatario.get())
                print(f"Obteniendo chat para el ID de soporte: {id_destino}")  # Verifica el ID ingresado
                mensajes = obtener_chat(self.id_usuario, id_destino)
                if mensajes:
                    for msg in mensajes:
                        emisor = "Tú" if msg[0] == self.id_usuario else "Soporte"
                        area_mensajes.insert("end", f"{emisor} ({msg[2]}):\n{msg[1]}\n\n")
                else:
                    area_mensajes.insert("end", "No se encontraron mensajes previos.\n\n")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el chat:\n{e}")
            area_mensajes.configure(state="disabled")

        def enviar_mensaje():
            try:
                id_destino = int(entrada_destinatario.get())
                texto = entrada_mensaje.get("1.0", "end").strip()
                if texto:
                    print(f"Enviando mensaje a soporte ID {id_destino}: {texto}")  # Depuración
                    enviar_mensaje_chat(self.id_usuario, id_destino, texto)
                    entrada_mensaje.delete("1.0", "end")
                    cargar_chat()
                else:
                    messagebox.showwarning("Advertencia", "El mensaje no puede estar vacío.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar el mensaje:\n{e}")

        # Botón para cargar el chat
        boton_cargar = ctk.CTkButton(ventana_chat, text="Cargar chat", command=cargar_chat, width=200, height=40)
        boton_cargar.pack(pady=(5, 15))

        # Etiqueta explicativa para el cuadro de mensaje
        ctk.CTkLabel(ventana_chat, text="Escribe tu mensaje aquí:", font=ctk.CTkFont(size=12)).pack(pady=5)

        # Entrada para el mensaje a enviar
        entrada_mensaje = ctk.CTkTextbox(ventana_chat, height=80, font=ctk.CTkFont(size=12), wrap="word")
        entrada_mensaje.pack(pady=10)

        # Botón para enviar el mensaje
        boton_enviar = ctk.CTkButton(ventana_chat, text="Enviar mensaje", command=enviar_mensaje, width=200, height=40, fg_color="#4caf50")
        boton_enviar.pack(pady=(5, 20))

        def actualizar_mensajes_periodicamente():
            """Función para actualizar el chat cada ciertos segundos."""
            cargar_chat()  # Llamamos a cargar_chat para actualizar el contenido
            ventana_chat.after(3000, actualizar_mensajes_periodicamente)  # Actualiza cada 3 segundos (3000 ms)

        # Iniciar el refresco automático de los mensajes
        actualizar_mensajes_periodicamente()

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
            
            # Si el ticket fue reenviado a admin
            texto_adicional = "⚠️ Reenviado por soporte" if ticket[7] else ""
            color_texto = "orange" if ticket[7] else "white"

            ctk.CTkLabel(
                frame,
                text=f"Usuario: {ticket[5]} {ticket[6]} | Prioridad: {ticket[4]} {texto_adicional}",
                font=ctk.CTkFont(size=12),
                text_color=color_texto
            ).pack(anchor="w", padx=10, pady=2)

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
        Permite al administrador visualizar todos los usuarios registrados y consultar
        el historial de tickets de un usuario específico seleccionando su ID.
        """

        # Ventana secundaria
        ventana = ctk.CTkToplevel()
        ventana.title("Gestión de Usuarios")
        ventana.geometry("600x400")

        # Etiqueta de título
        titulo = ctk.CTkLabel(ventana, text="Usuarios Registrados", font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        # Textbox para mostrar usuarios
        lista_usuarios = ctk.CTkTextbox(ventana, width=500, height=200, wrap="none")
        lista_usuarios.pack(pady=10)

        # Mostrar usuarios
        resultados = obtener_usuarios_registrados()
        if resultados:
            for usuario in resultados:
                id_usuario = usuario[0]
                nombre_usuario = usuario[1]
                lista_usuarios.insert("end", f"ID: {id_usuario} | Usuario: {nombre_usuario}\n")
        else:
            lista_usuarios.insert("end", "No hay usuarios registrados.")

        # Entrada para ingresar ID del usuario
        entrada_id = ctk.CTkEntry(ventana, placeholder_text="Ingrese ID del usuario")
        entrada_id.pack(pady=10)

        def mostrar_historial():
            id_usuario = entrada_id.get()
            if not id_usuario.isdigit():
                messagebox.showwarning("ID inválido", "Ingrese un ID numérico válido.")
                return

            historial = obtener_historial_tickets_usuario(int(id_usuario))

            if historial:
                historial_ventana = ctk.CTkToplevel(ventana)
                historial_ventana.title(f"Historial de Usuario {id_usuario}")
                historial_ventana.geometry("620x420")

                # Frame contenedor con scroll
                contenedor = ctk.CTkFrame(historial_ventana)
                contenedor.pack(fill="both", expand=True, padx=10, pady=10)

                canvas = tk.Canvas(contenedor, bg="#1a1a1a", highlightthickness=0)
                scrollbar = ctk.CTkScrollbar(contenedor, orientation="vertical", command=canvas.yview)
                scroll_frame = ctk.CTkFrame(canvas)

                scroll_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )

                canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                # Mostrar los tickets
                for ticket in historial:
                    frame_ticket = ctk.CTkFrame(scroll_frame, fg_color="#2c2c2c", corner_radius=10)
                    frame_ticket.pack(pady=10, fill="x", padx=10)

                    ctk.CTkLabel(frame_ticket, text=f"ID: {ticket[0]}", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=2)
                    ctk.CTkLabel(frame_ticket, text=f"Título: {ticket[1]}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)
                    ctk.CTkLabel(frame_ticket, text=f"Descripción: {ticket[2]}", font=ctk.CTkFont(size=12), wraplength=550).pack(anchor="w", padx=10, pady=2)
                    ctk.CTkLabel(frame_ticket, text=f"Fecha: {ticket[3]}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)
                    ctk.CTkLabel(frame_ticket, text=f"Estado: {ticket[4]}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)

                    ctk.CTkLabel(frame_ticket, text="------------------------------------------------------", font=ctk.CTkFont(size=10)).pack(pady=5, padx=10)

            else:
                messagebox.showinfo("Sin resultados", "Este usuario no tiene historial de tickets.")

            
        # Botón para consultar historial
        boton_historial = ctk.CTkButton(ventana, text="Ver historial de tickets", command=mostrar_historial)
        boton_historial.pack(pady=10)



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
