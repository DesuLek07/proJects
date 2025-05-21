import customtkinter as ctk
from ventana_base import ventana_principal
from backend.querys_conexion import obtener_registros_soporte, obtener_administradores, actualizar_estado_ticket2, escalar_soporte_a_ticket
from tkinter import messagebox

class ventana_dashboard_soporte(ventana_principal):
    def __init__(self, id_usuario, menu_ref, imagen_fondo_ctk):
        self.id_usuario = id_usuario
        self.menu_ref = menu_ref
        self.imagen_fondo_ctk = imagen_fondo_ctk

        super().__init__(
            titulo='Panel de Soporte',
            tamaño=(1000, 580, 70, 25),
            tema='dark',
            minimo=(1000, 580),
            maximo=(1000, 580)
        )

        self.construir_layout()

    def construir_layout(self):
        # Frame lateral
        self.sidebar = ctk.CTkFrame(self.root, width=200, fg_color="#1f1f2e", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="Soporte", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        self.btn_inicio = ctk.CTkButton(self.sidebar, text="Inicio", command=self.mostrar_inicio)
        self.btn_inicio.pack(pady=10, fill="x", padx=15)

        self.btn_tickets = ctk.CTkButton(self.sidebar, text="Ver Tickets", command=self.mostrar_tickets)
        self.btn_tickets.pack(pady=10, fill="x", padx=15)

        self.btn_salir = ctk.CTkButton(self.sidebar, text="Volver", fg_color="red3", command=exit)
        self.btn_salir.pack(pady=(200, 20), fill="x", padx=15)

        # Frame principal dinámico
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#252540")
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.mostrar_inicio()

    def mostrar_inicio(self):
        # Limpiar frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Bienvenido, Usuario Soporte",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="light cyan").pack(pady=(30, 10))

        # Aquí podrías traer más datos si tienes una función como obtener_info_usuario(self.id_usuario)
        info_texto = f"""
🆔 ID Usuario: {self.id_usuario}
👤 Rol: Soporte Técnico
📅 Acceso concedido
"""
        ctk.CTkLabel(self.main_frame, text=info_texto,
                     font=ctk.CTkFont(size=16),
                     justify="left").pack(pady=10)

    def mostrar_tickets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text='Tickets Recibidos',
                     font=ctk.CTkFont(size=20, weight='bold'),
                     text_color='light cyan').pack(pady=(20, 10))

        contenedor = ctk.CTkScrollableFrame(self.main_frame, width=800, height=450,
                                            fg_color='#2a2a40', corner_radius=15)
        contenedor.pack(padx=10, pady=10, fill="both", expand=True)

        registros = obtener_registros_soporte()

        if not registros:
            ctk.CTkLabel(contenedor, text="No hay registros de soporte.",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="white").pack(anchor="center", pady=20)
            return

        for soporte in registros:
            frame = ctk.CTkFrame(contenedor, fg_color="#2f2f2f", corner_radius=12)
            frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"Ticket ID: {soporte[0]}", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(frame, text=f"Usuario: {soporte[2]} ({soporte[3]})", font=ctk.CTkFont(size=12), text_color="#cfcfcf").pack(anchor="w", padx=15, pady=(0, 8))

            detalles = [
                ("📌 Problema", soporte[4]),
                ("⚠️ Tipo Afectación", soporte[5]),
                ("🏢 Entidad que Atendió", soporte[6]),
                ("📨 Medio de Respuesta", soporte[7]),
                ("📝 Info. Medio", soporte[8]),
            ]

            for etiqueta, valor in detalles:
                ctk.CTkLabel(frame, text=f"{etiqueta}: {valor}", font=ctk.CTkFont(size=12), text_color="white").pack(anchor="w", padx=15)

            ctk.CTkButton(frame, text="Ver detalles", command=lambda soporte=soporte: self.expandir_soporte(soporte)).pack(pady=(5, 10))

    def expandir_soporte(self, soporte):
        ventana_expandida = ctk.CTkToplevel(self.root)
        ventana_expandida.title(f"Detalles de Soporte {soporte[0]}")
        ventana_expandida.geometry("550x600")
        ventana_expandida.resizable(False, False)
        ventana_expandida.configure(fg_color="#202020")

        ctk.CTkLabel(ventana_expandida, text=f"Detalles del Ticket #{soporte[0]}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

        detalles_expand = [
            f"👤 Enviado por: {soporte[2]} ({soporte[3]})",
            f"🆔 ID del Ticket: {soporte[0]}",
            f"📌 Problema: {soporte[4]}",
            f"⚠️ Tipo de Afectación: {soporte[5]}",
            f"🏢 Entidad que Atendió: {soporte[6]}",
            f"📨 Medio de Respuesta: {soporte[7]}",
            f"📝 Información Adicional: {soporte[8]}",
        ]

        for texto in detalles_expand:
            ctk.CTkLabel(ventana_expandida, text=texto, font=ctk.CTkFont(size=13), wraplength=460, justify="left").pack(anchor="w", padx=25, pady=6)

        boton_frame = ctk.CTkFrame(ventana_expandida)
        boton_frame.pack(pady=(20, 30))

        ctk.CTkButton(boton_frame, text="Marcar como Resuelto", command=lambda: self.cambiar_estado_ticket(soporte[0], ventana_expandida)).pack(side="left", padx=10)
        ctk.CTkButton(boton_frame, text="Escalar a Admin", command=lambda: self.escalar_soporte(soporte[0], ventana_expandida)).pack(side="left", padx=10)

    def cambiar_estado_ticket(self, id_soporte, ventana):
        try:
            if actualizar_estado_ticket2(id_soporte, 0):
                messagebox.showinfo("Éxito", "Estado del ticket actualizado a 'Resuelto'.")
                ventana.destroy()
                self.mostrar_tickets()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado del ticket.")
        except Exception as e:
            print(f"Error al cambiar estado: {e}")
            messagebox.showerror("Error", "Error al actualizar el estado del ticket.")

    def escalar_soporte(self, id_soporte, ventana_padre):
        administradores = obtener_administradores()
        if not administradores:
            messagebox.showerror("Error", "No hay administradores disponibles.")
            return

        ventana_admin = ctk.CTkToplevel(ventana_padre)
        ventana_admin.title("Seleccionar Administrador")
        ventana_admin.geometry("300x200")

        combo_admin = ctk.CTkComboBox(ventana_admin, values=[f"{admin[0]} - {admin[1]}" for admin in administradores])
        combo_admin.pack(pady=20)

        def confirmar():
            selected = combo_admin.get()
            if selected:
                id_admin = selected.split(" - ")[0]
                confirmado = messagebox.askyesno("Confirmar", f"¿Deseas escalar este soporte al administrador {selected}?")
                if confirmado:
                    exito = escalar_soporte_a_ticket(id_soporte, id_admin)
                    if exito:
                        messagebox.showinfo("Éxito", "Soporte escalado correctamente.")
                    else:
                        messagebox.showerror("Error", "No se pudo escalar el soporte.")
                ventana_admin.destroy()

        ctk.CTkButton(ventana_admin, text="Confirmar", command=confirmar).pack(pady=10)

    def lanzar(self):
        self.iniciar_ventana()
