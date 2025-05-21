import customtkinter as ctk
import webbrowser
from PIL import Image
from ventana_base import ventana_principal
from backend.querys_conexion import guardar_soporte
from tkinter import messagebox

# Ruta de la imagen
ruta_fondo = r'C:\Users\DesuLek\Desktop\SRPP\styles\wp.jpg'

# Cargar la imagen con PIL
imagen_fondo = Image.open(ruta_fondo)

# Crear el objeto CTkImage
imagen_fondo_ctk = ctk.CTkImage(light_image=imagen_fondo, dark_image=imagen_fondo, size=(1200, 650))

# Funciones de botones
def github():
    webbrowser.open('https://github.com/DesuLek07/proJects/tree/helpdesk#')

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
            Boton_salida = ctk.CTkButton(self.root, text='Salida segura', font=ctk.CTkFont(32, weight='bold', size=12),
                                   corner_radius=20,
                                   fg_color='red3',
                                   bg_color='black',
                                   command=exit)
            Boton_salida.place(relx=0.95, rely=0.95, anchor='e')

            Boton_soporte = ctk.CTkButton(frame2, text='Soporte',
                                          font=ctk.CTkFont(32, size=12, weight='bold'),
                                          corner_radius=20,
                                          fg_color='#1e1e2f',
                                          bg_color='black',
                                          border_color='#3a3a5f',
                                          border_width=1,
                                          command=soporte_helpdesk)
            Boton_soporte.place(relx=0.95, rely=0.95, anchor='se')

def soporte_helpdesk():
    ventana_soporte = ctk.CTkToplevel()
    ventana_soporte.title('Soporte')
    ventana_soporte.geometry('600x580')
    ventana_soporte.resizable(False, False)

    fuente_label = ctk.CTkFont(size=14, weight="bold")
    fg_color_entry = 'gray15'
    text_color_entry = 'white'

    # --- Encabezado ---
    ctk.CTkLabel(ventana_soporte, text='Soporte Técnico - Problemas de acceso', font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

    # ID usuario
    frame_id = ctk.CTkFrame(ventana_soporte)
    frame_id.pack(pady=5, fill='x', padx=20)

    ctk.CTkLabel(frame_id, text='Ingrese su ID de usuario (obligatorio):', font=fuente_label).grid(row=0, column=0, padx=10, pady=5, sticky='w')
    id_entry = ctk.CTkEntry(frame_id, placeholder_text='ID de usuario', placeholder_text_color='gray',
                            fg_color=fg_color_entry, text_color=text_color_entry, height=30, width=120)
    id_entry.grid(row=1, column=0, padx=10)

    # Afectación
    frame_afectacion = ctk.CTkFrame(ventana_soporte)
    frame_afectacion.pack(pady=10, fill='x', padx=20)

    ctk.CTkLabel(frame_afectacion, text='Seleccione su problema o ingrese otro:', font=fuente_label).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
    tipos_afectacion = ['Contraseña', 'Nombre de usuario']
    tipo_var = ctk.StringVar(value=tipos_afectacion[0])
    tipo_menu = ctk.CTkOptionMenu(frame_afectacion, values=tipos_afectacion, variable=tipo_var,
                                  fg_color=fg_color_entry, text_color=text_color_entry)
    tipo_menu.grid(row=1, column=0, padx=10)

    tipo_personalizado_entry = ctk.CTkEntry(frame_afectacion, placeholder_text='Otro tipo de problema (opcional)',
                                            placeholder_text_color='gray', fg_color=fg_color_entry,
                                            text_color=text_color_entry, height=30, width=200)
    tipo_personalizado_entry.grid(row=1, column=1, padx=10)

    # Medio y contacto
    frame_contacto = ctk.CTkFrame(ventana_soporte)
    frame_contacto.pack(pady=10, fill='x', padx=20)

    ctk.CTkLabel(frame_contacto, text='Seleccione medio de respuesta:', font=fuente_label).grid(row=0, column=0, padx=10, pady=5, sticky='w')
    medios = ['Correo', 'Telefono', 'Whatsapp']
    medio_var = ctk.StringVar(value=medios[0])
    medio_menu = ctk.CTkOptionMenu(frame_contacto, values=medios, variable=medio_var,
                                   fg_color=fg_color_entry, text_color=text_color_entry)
    medio_menu.grid(row=1, column=0, padx=10)

    ctk.CTkLabel(frame_contacto, text='Ingrese su medio de contacto (obligatorio):', font=fuente_label).grid(row=0, column=1, padx=10, pady=5, sticky='w')
    medio_info_entry = ctk.CTkEntry(frame_contacto, placeholder_text='Correo, Teléfono o WhatsApp',
                                    placeholder_text_color='gray', fg_color=fg_color_entry,
                                    text_color=text_color_entry, height=30, width=180)
    medio_info_entry.grid(row=1, column=1, padx=10)

    # Descripción del problema
    ctk.CTkLabel(ventana_soporte, text='Asunto / Descripción del problema (incluya nombre y documento):', font=fuente_label).pack(pady=(15, 5))
    descripcion_text = ctk.CTkTextbox(ventana_soporte, width=500, height=140, fg_color='gray13', text_color='white')
    descripcion_text.pack(pady=5)

    # Botón enviar
    def enviar_ticket():
        tipo_base = tipo_var.get()
        tipo_otro = tipo_personalizado_entry.get().strip()
        tipo_final = tipo_otro if tipo_otro else tipo_base

        medio = medio_var.get()
        medio_info = medio_info_entry.get().strip()
        descripcion = descripcion_text.get("1.0", "end").strip()
        entidad_atendio = "Soporte"

        # Validación del ID
        id_texto = id_entry.get().strip()
        if not id_texto.isdigit():
            messagebox.showerror(title="Error", message="El ID debe ser un número válido")
            return
        id_usuario = int(id_texto)

        # Validación general
        if not medio_info or not descripcion:
            messagebox.showerror(title="Error", message="Debe completar todos los campos obligatorios")
            return
        if len(descripcion.split()) < 4 or not any(c.isdigit() for c in descripcion):
            messagebox.showerror(title="Error", message="Debe incluir su nombre completo y número de documento en la descripción")
            return

        exito = guardar_soporte(id_usuario, descripcion, tipo_final, entidad_atendio, medio, medio_info)
        if exito:
            messagebox.showinfo(title="Éxito", message="Ticket enviado correctamente")
            ventana_soporte.destroy()
        else:
            messagebox.showerror(title="Error", message="Error al enviar el ticket")

    ctk.CTkButton(ventana_soporte, text='Enviar ticket', fg_color='#1e1e2f', corner_radius=20,
                  font=ctk.CTkFont(size=14, weight="bold"),
                  command=enviar_ticket).place(relx=0.5, rely=0.96, anchor='center')

if __name__ == "__main__":
    menu = ventana_menu()
    menu.iniciar_ventana()
