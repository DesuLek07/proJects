import customtkinter as ctk
from tkinter import messagebox
from Backend.querys_conexion import registrar
from datetime import datetime

def lanzar_registro():

    ventana = ctk.CTk()
    ventana.title('SRPPM')
    ventana.geometry('800x500')
    ventana._set_appearance_mode('dark')
    ventana.minsize(800,500)
    ventana.maxsize(800,500)

    # Contenedor
    frame1 = ctk.CTkFrame(ventana, 
                        width=360, 
                        height=470, 
                        corner_radius=20, 
                        fg_color='gray19')

    frame1.place(relx=0.05, rely=0.5, anchor='w')


    # Titulo
    label1 = ctk.CTkLabel(frame1, text='Registrar Usuario', 
                        font=ctk.CTkFont(32, weight='bold'),
                        corner_radius=20,
                        fg_color='azure3',
                        text_color='black')

    label1.place(relx=0.5, rely=0.1, anchor='center')

    #Entrada nombre
    entrada_nombre = ctk.CTkEntry(frame1, placeholder_text='Nombre')
    entrada_nombre.place(relx = 0.5, rely = 0.25, anchor='center')

    # Entrada segundo nombre
    entrada_segnombre = ctk.CTkEntry(frame1, placeholder_text='Segundo Nombre')
    entrada_segnombre.place(relx=0.5, rely=0.35, anchor='center')

    # Entrada apellido
    entrada_apellido = ctk.CTkEntry(frame1, placeholder_text='Apellido')
    entrada_apellido.place(relx=0.5, rely=0.45, anchor='center')

    # Entrada segundo apellido
    entrada_segapellido = ctk.CTkEntry(frame1, placeholder_text='Segundo Apellido')
    entrada_segapellido.place(relx=0.5, rely=0.55, anchor='center')

    # Entrada tipo de identificacion
    tipos_id = ['Cedula de ciudadania', 'Tarjeta de Identidad', 'Cedula extranjeria', 'Pasaporte', 'NIT']
    opcion = ctk.StringVar(value=tipos_id[0])
    opcion_tipo_id = ctk.CTkOptionMenu(frame1, values=tipos_id, variable=opcion, fg_color='azure4', text_color='black')
    opcion_tipo_id.place(relx=0.5, rely=0.65, anchor='center')

    # Entrada identificacion
    entrada_identificacion = ctk.CTkEntry(frame1, placeholder_text='Numero identificacion')
    entrada_identificacion.place(relx=0.5, rely=0.75, anchor='center')

    # Segundo Contenedor
    frame2 = ctk.CTkFrame(ventana,
                        width=360,
                        height=470,
                        corner_radius=20,
                        fg_color='gray20')

    frame2.place(relx=0.52, rely=0.5, anchor='w')

    # Segundo titulo
    label2 = ctk.CTkLabel(frame2, text=f'Credenciales de registro',
                        font=ctk.CTkFont(32, weight='bold'),
                        corner_radius=20,
                        fg_color='azure3',
                        text_color='black')

    label2.place(relx=0.5, rely=0.1, anchor='center')

    # Entrada username
    entrada_username = ctk.CTkEntry(frame2, placeholder_text='Nombre de usuario')
    entrada_username.place(relx=0.5, rely=0.25, anchor='center')

    # Entrada correo
    entrada_correo = ctk.CTkEntry(frame2, placeholder_text='Correo electronico')
    entrada_correo.place(relx=0.5, rely=0.35, anchor='center')

    # Entrada telefono principal
    entrada_tel1 = ctk.CTkEntry(frame2, placeholder_text='Telefono principal')
    entrada_tel1.place(relx=0.5, rely=0.45, anchor='center')

    # Entrada telefono secundario
    entrada_tel2 = ctk.CTkEntry(frame2, placeholder_text='Telefono secundario')
    entrada_tel2.place(relx=0.5, rely=0.55, anchor='center')

    # Entrada contraseña
    entrada_contraseña = ctk.CTkEntry(frame2, placeholder_text='Contraseña', show='*')
    entrada_contraseña.place(relx=0.5, rely=0.65, anchor='center')

    # Comprobacion login
    def register():

        campos = [
            entrada_nombre.get(),
            entrada_segnombre.get(),
            entrada_apellido.get(),
            entrada_segapellido.get(),
            opcion_tipo_id.get(),
            entrada_identificacion.get(),
            entrada_username.get(),
            entrada_correo.get(),
            entrada_tel1.get(),
            entrada_tel2.get(),
            entrada_contraseña.get()
        ]

        if any(campo.strip() == '' for campo in campos):
            messagebox.showwarning('Campos incompletos', 'Debe rellenar todos los campos para registrarse')

        nombre = entrada_nombre.get()
        segundo_nombre = entrada_segnombre.get()
        apellido = entrada_apellido.get()
        segundo_apellido = entrada_segapellido.get()
        tipo_id = opcion_tipo_id.get()
        numero_identificacion = entrada_identificacion.get()
        fecha_registro = registrar_tiempo()
        nombre_usuario = entrada_username.get()
        correo = entrada_correo.get()
        telefono_principal = entrada_tel1.get()
        telefono_secundario = entrada_tel2.get()
        contraseña_hash = entrada_contraseña.get()
        fecha_actualizacion = registrar_tiempo()
        
        if len(contraseña_hash) < 8:
            messagebox.showwarning('Contraseña débil', 'La contraseña debe tener al menos 8 caracteres.')
            return
        else:
            if registrar(nombre, segundo_nombre, apellido, segundo_apellido, tipo_id, numero_identificacion, fecha_registro, correo, contraseña_hash, telefono_principal, telefono_secundario, fecha_actualizacion, nombre_usuario):
                messagebox.showinfo('Registro exitoso', 'Bienvenido al sistema')
            else:
                messagebox.showerror('Error', 'Error al hacer el registro')

    def registrar_tiempo():
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return fecha_actual

    # Boton de ingreso
    Boton_ingreso = ctk.CTkButton(frame1, text='Registrarse', command=register)
    Boton_ingreso.place(relx=0.5, rely=0.9, anchor='center')

    ventana.bind('<Return>', lambda event: register())

    ventana.mainloop()
