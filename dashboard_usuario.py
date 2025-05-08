import customtkinter as ctk
from ventana_base import ventana_principal
from backend.querys_conexion import obtener_datos_usuario, guardar_ticket, obtener_tickets, obtener_respuestas_usuario
from tkinter import messagebox, filedialog
import os

class ventana_dashboard(ventana_principal):

    """
    Clase que representa el panel principal para el usuario.
    Hereda de ventana_principal y carga la interfaz de usuario con sus datos,
    opciones para enviar PQR, ver historial de tickets y respuestas recibidas.
    """

    def __init__(self, id_usuario, menu_ref, imagen_fondo_ctk=None):

        """
        Inicializa el dashboard con la información del usuario.

        Args:
            id_usuario (int): ID del usuario autenticado.
            menu_ref (obj): Referencia al menú principal para mostrar/ocultar.
            imagen_fondo_ctk (obj, opcional): Imagen de fondo para el dashboard (no usada aún).
        """

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

        """
        Muestra nuevamente el menú principal desde el dashboard.
        """

        self.root.deiconify()
        if self.menu_ref:
            self.menu_ref.mostrar_ventana()

    def construir_interfaz(self):
        
        """
        Construye la interfaz gráfica del dashboard con los datos del usuario,
        botones de navegación y contenedores visuales.
        """

        # Fondo de la interfaz
        self.fondo = ctk.CTkFrame(self.root, width=1000, height=550, fg_color='#1e1e2f')
        self.fondo.pack()

        # Contenedor principal
        self.frame_inicio = ctk.CTkFrame(self.root, width=560, height=400,
                                 fg_color='#252540',
                                 bg_color='#1e1e2f',
                                 border_width=1,
                                 border_color='#3a3a5f',
                                 corner_radius=20)
        self.frame_inicio.place(relx=0.5, rely=0.55, anchor='center')

        # Título del contenedor
        self.titulo = ctk.CTkLabel(self.root, text='¡Bienvenido!',
                           font=ctk.CTkFont(size=26, weight='bold'),
                           fg_color='#1e1e2f',
                           bg_color='#1e1e2f',
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

        # Contenedor de la barra lateral
        self.frame_barra_lateral = ctk.CTkFrame(self.root,
                                        width=80, height=550,
                                        fg_color='#12121f',
                                        corner_radius=0)
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

        # Botón de las PQR
        self.boton_pqr = ctk.CTkButton(self.frame_barra_lateral,
                                       text='📩', command=self.abrir_pqr,
                                       **estilo_boton)
        self.boton_pqr.place(relx=0.5, rely=0.05, anchor='center')

        # Botón para ver el historial de tickets
        self.boton_historial = ctk.CTkButton(self.frame_barra_lateral,
                                             text='📜', command=self.abrir_historial,
                                             **estilo_boton)
        self.boton_historial.place(relx=0.5, rely=0.15, anchor='center')

        # Botón de mensajes recibidos
        self.boton_ver_respuestas = ctk.CTkButton(self.frame_barra_lateral,
                                          text='📬', command=self.ver_respuestas,
                                          **estilo_boton)
        self.boton_ver_respuestas.place(relx=0.5, rely=0.35, anchor='center')

        # Boton salida segura
        Boton_salida = ctk.CTkButton(self.root, text='Salida segura', font=ctk.CTkFont(32, weight='bold', size=12),
                                   corner_radius=20,
                                   fg_color='red3',
                                   bg_color='#1e1e2f',
                                   command=exit)
        Boton_salida.place(relx=0.95, rely=0.95, anchor='e')

    def abrir_pqr(self):

        """
        Abre una nueva ventana para que el usuario envíe una PQR (Petición, Queja o Reclamo).
        Permite adjuntar un archivo opcional (hasta 2MB).
        """

        ventana_pqr = ctk.CTkToplevel(self.root)
        ventana_pqr.title("Enviar PQR")
        ventana_pqr.geometry("420x550")
        ventana_pqr.resizable(False, False)

        ctk.CTkLabel(ventana_pqr, text="Asunto:", font=ctk.CTkFont(size=14)).pack(pady=8)
        entrada_asunto = ctk.CTkEntry(ventana_pqr, width=340)
        entrada_asunto.pack()

        ctk.CTkLabel(ventana_pqr, text="Mensaje:", font=ctk.CTkFont(size=14)).pack(pady=8)
        entrada_mensaje = ctk.CTkTextbox(ventana_pqr, width=340, height=150)
        entrada_mensaje.pack()

        archivo_seleccionado = ctk.StringVar(value="No se ha seleccionado archivo.")
        ruta_archivo = [None]

        def seleccionar_archivo():
            ruta = filedialog.askopenfilename(title="Seleccionar archivo")
            if ruta:
                tamaño = os.path.getsize(ruta)
                if tamaño > 2 * 1024 * 1024:
                    messagebox.showwarning("Archivo demasiado grande", "El archivo no debe superar los 2MB.")
                    return
                archivo_seleccionado.set(os.path.basename(ruta))
                ruta_archivo[0] = ruta

        ctk.CTkButton(ventana_pqr, text="Seleccionar archivo (opcional)", command=seleccionar_archivo).pack(pady=10)
        ctk.CTkLabel(ventana_pqr, text='', textvariable=archivo_seleccionado, wraplength=340,
                     font=ctk.CTkFont(size=10)).pack()

        def enviar_pqr():
            asunto = entrada_asunto.get().strip()
            mensaje = entrada_mensaje.get("1.0", "end").strip()

            if not asunto or not mensaje:
                messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos obligatorios.")
                return

            archivo_binario = None
            if ruta_archivo[0]:
                with open(ruta_archivo[0], 'rb') as file:
                    archivo_binario = file.read()

            exito = guardar_ticket(
                id_usuario=self.id_usuario,
                titulo=asunto,
                descripcion=mensaje,
                estado="Pendiente",
                prioridad="Media",
                id_categoria=None,
                id_asignado=None,
                archivo=archivo_binario
            )

            if exito:
                messagebox.showinfo("PQR enviada", "Tu PQR ha sido enviada exitosamente.")
                ventana_pqr.destroy()
            else:
                messagebox.showerror("Error", "No se pudo guardar la PQR.")

        ctk.CTkButton(ventana_pqr, text="Enviar PQR", command=enviar_pqr).pack(pady=20)

    def abrir_historial(self):

        """
        Muestra una ventana con el historial de tickets enviados por el usuario.
        Incluye opción para descargar archivos adjuntos si existen.
        """

        ventana_historial = ctk.CTkToplevel(self.root)
        ventana_historial.title("Historial de Tickets")
        ventana_historial.geometry("600x500")
        ventana_historial.resizable(False, False)

        tickets = obtener_tickets(self.id_usuario)

        if not tickets:
            ctk.CTkLabel(ventana_historial, text="No hay tickets registrados.",
                         font=ctk.CTkFont(size=14)).pack(pady=20)
            return

        for ticket in tickets:
            frame_ticket = ctk.CTkFrame(ventana_historial, fg_color="#2c2c2c", corner_radius=10)
            frame_ticket.pack(pady=10, padx=20, fill="x")

            ctk.CTkLabel(frame_ticket, text=f"Título: {ticket[1]}",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(frame_ticket, text=f"Descripción: {ticket[2][:100]}...",
                         font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(frame_ticket, text=f"Fecha: {ticket[3]}",
                         font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame_ticket, text=f"Estado: {ticket[4]} | Prioridad: {ticket[5]}",
                         font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=2)

            if ticket[8]:
                def descargar_archivo_con_closure(contenido, nombre):
                    def accion():
                        ruta = filedialog.asksaveasfilename(defaultextension=".bin", initialfile=nombre)
                        if ruta:
                            with open(ruta, 'wb') as f:
                                f.write(contenido)
                            messagebox.showinfo("Archivo guardado", f"Archivo guardado en {ruta}")
                    return accion

                boton_descargar = ctk.CTkButton(frame_ticket, text="Descargar archivo",
                                                command=descargar_archivo_con_closure(ticket[8], f"archivo_ticket_{ticket[0]}.bin"),
                                                width=150)
                boton_descargar.pack(anchor="e", padx=10, pady=5)

    def ver_respuestas(self):

        """
        Abre una ventana con las respuestas asociadas a los tickets enviados por el usuario.
        """

        respuestas = obtener_respuestas_usuario(self.id_usuario)

        ventana_respuestas = ctk.CTkToplevel(self.root)
        ventana_respuestas.title("Respuestas a tus PQR")
        ventana_respuestas.geometry("550x400")
        ventana_respuestas.resizable(False, False)

        if not respuestas:
            ctk.CTkLabel(ventana_respuestas, text="Aún no tienes respuestas disponibles.").pack(pady=20)
            return

        for r in respuestas:
            frame = ctk.CTkFrame(ventana_respuestas, fg_color="#2f2f3f", corner_radius=10)
            frame.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(frame, text=f"Ticket ID: {r[1]} - {r[3].strftime('%Y-%m-%d %H:%M')}", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=r[2], font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=2)


    def mostrar_info_usuario(self):

        """
        Muestra una ventana emergente con el ID del usuario actual.
        """

        messagebox.showinfo("Información del usuario", f"ID de usuario: {self.id_usuario}")

    def lanzar(self):

        """
        Inicia la ventana de dashboard y entra en el bucle principal.
        """

        self.iniciar_ventana()