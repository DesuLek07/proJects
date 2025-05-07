import customtkinter as ctk

class ventana_principal:
    """
    Clase base para la ventana principal de la aplicación SRPP.
    Permite definir título, tamaño, tema visual y comportamientos básicos.
    """

    def __init__(self, titulo='SRPP', tamaño=(1200, 650, 70, 25), tema='dark',
                 minimo=(1200, 650), maximo=(1200, 650), ruta_fondo=None):
        """
        Inicializa la ventana principal con configuración personalizada.

        Args:
            titulo (str): Título de la ventana.
            tamaño (tuple): Dimensiones y posición de la ventana (ancho, alto, x, y).
            tema (str): Tema visual ('dark' o 'light').
            minimo (tuple): Tamaño mínimo de la ventana (ancho, alto).
            maximo (tuple): Tamaño máximo de la ventana (ancho, alto).
            ruta_fondo (str, opcional): Ruta a la imagen de fondo (actualmente no utilizada).
        """
        self.root = ctk.CTk()
        self.root.title(titulo)
        self.root.geometry(f'{tamaño[0]}x{tamaño[1]}+{tamaño[2]}+{tamaño[3]}')
        self.root._set_appearance_mode(tema)
        self.root.minsize(*minimo)
        self.root.maxsize(*maximo)

        self.construir_interfaz()

    def construir_interfaz(self):
        """
        Método para construir la interfaz gráfica.
        Se espera que las clases hijas sobrescriban este método.
        """
        pass

    def iniciar_ventana(self):
        """
        Inicia el bucle principal de la ventana.
        """
        self.root.mainloop()

    def cerrar_ventana(self):
        """
        Cierra la ventana y finaliza la aplicación.
        """
        self.root.destroy()

    def mostrar_ventana_principal(self):
        """
        Muestra la ventana si estaba oculta y la trae al frente.
        """
        self.root.deiconify()
        self.root.lift()

    def ocultar_ventana(self):
        """
        Oculta temporalmente la ventana principal.
        """
        self.root.withdraw()
