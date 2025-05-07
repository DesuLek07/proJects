import customtkinter as ctk

class ventana_principal:
    def __init__(self, titulo='SRPP', tamaño=(1200, 650, 70, 25), tema='dark', minimo=(1200, 650), maximo=(1200, 650), ruta_fondo=None):
        # Atributos de la ventana
        self.root = ctk.CTk()
        self.root.title(titulo)
        self.root.geometry(f'{tamaño[0]}x{tamaño[1]}+{tamaño[2]}+{tamaño[3]}')
        self.root._set_appearance_mode(tema)
        self.root.minsize(*minimo)
        self.root.maxsize(*maximo)

        self.construir_interfaz()  # llamada al diseño de la interfaz

    # Métodos de la clase ventana
    def construir_interfaz(self):
        pass  # La clase base no tiene interfaz

    def iniciar_ventana(self):
        self.root.mainloop()

    def cerrar_ventana(self):
        self.root.destroy()

    def mostrar_ventana_principal(self):
        self.root.deiconify() 
        self.root.lift() 

    def ocultar_ventana(self):
        self.root.withdraw()  
