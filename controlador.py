"""
Controlador de la Aplicacion
Este codigo tiene incluido una base de datos que se conecta a traves de peewee
Tiene tambien una programacion POO
Esta dividida en MVC
"""

from tkinter import Tk 
from modelo import egb, cfi, superior, integracion
from vista import Ventanita

class Controler:

    """ 
    Clase Controler
    La clase Controler actúa como intermediario entre la vista (Ventanita) 
    y la lógica del programa que interactúa con la base de datos. 
    También define las variables necesarias para generar gráficos. 
    
    Attributes: 
        nombres (list): Lista de nombres de las categorías para los gráficos. 
        colores (list): Lista de colores correspondientes a las categorías para los gráficos. 
        tamano (list): Lista de tamaños correspondientes a las categorías para los gráficos. 
    """
    
    nombres = ['EGB', 'CFI', 'SUP', 'INTEG']
    colores = ['blue', 'red', 'green', 'yellow']
    tamano = [egb, cfi, superior, integracion]

    # La clase Controler actúa como intermediario entre la vista (Ventanita) y los datos/models (importados desde modelo_mail)
    # ventana es una instancia de Tk, que representa la ventana principal de la aplicación.
    def __init__(self,ventana):
        """ 
        Constructor de la clase Controler 

        Args: ventana (tk.Tk): Instancia de la clase Ventanita que representa la ventana principal de la aplicación. 
        
        Attributes: 
            ventana (tk.Tk): La ventana principal de la aplicación. 
            objeto_vista (Ventanita): Instancia de la clase Ventanita que administra la interfaz gráfica. 
        """

        self.ventana=ventana
        self.objeto_vista = Ventanita(self.ventana, self.nombres, self.colores, self.tamano)
        

    # app Inicializa una instancia de Ventanita, pasando la ventana, los nombres,
    #  los colores y el tamaño para construir el grafico

if __name__ == "__main__":
    
    """ 
    Inicializa la aplicación principal. 
    
    Este bloque de código inicializa una instancia de `Controler`, pasando `window` (una instancia de `Tk`) 
    y llama al método `actualizar` de `objeto_vista`. Finalmente, inicia el bucle principal de la ventana. 
    Attributes: 
        window (tk.Tk): Instancia de la ventana principal de la aplicación. 
        aplicacion (Controler): Instancia de la clase `Controler` que administra la lógica de la aplicación. 
    """

    window = Tk()
    aplicacion=Controler(window)
    aplicacion.objeto_vista.actualizar()    
    window.mainloop()
