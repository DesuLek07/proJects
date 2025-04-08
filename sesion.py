import customtkinter as ctk
from tkinter import messagebox
from Backend.querys_conexion import verificar

def lanzar_inicio_sesion():

    ventana = ctk.CTk()
    ventana.title('SRPPM')
    ventana.geometry('400x300')
    ventana._set_appearance_mode('dark')
    ventana.minsize(400,300)
    ventana.maxsize(400,300)

    # Contenedor
    frame1 = ctk.CTkFrame(ventana, 
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

        campos = [entrada_usuario.get(),
                entrada_contraseña.get()]
        
        if any(campo.strip() == '' for campo in campos):
            messagebox.showerror('Campos incompletos', 'Recuerde completar todos los campos para iniciar sesion')

        usuario = entrada_usuario.get()
        contraseña = entrada_contraseña.get()
        
        if verificar(usuario, contraseña):
            messagebox.showinfo('Login exitoso', 'Bienvenido')
        else:
            messagebox.showerror('Error', 'Usuario o contraseña incorrectos')

    # Boton de ingreso
    Boton_ingreso = ctk.CTkButton(frame1, text='Ingresar', command=login)
    Boton_ingreso.place(relx=0.5, rely=0.75, anchor='center')

    ventana.bind('<Return>', lambda event: login())

    ventana.mainloop()
