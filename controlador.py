"""
Controlador de la Aplicacion
Este codigo tiene incluido una base de datos que se conecta a traves de peewee
Tiene tambien una programacion POO
Esta dividida en MVC
"""

from tkinter import Tk 
from modelo import egb, cfi, superior, integracion
from vista import Ventanita
import observador


class Controler:


    """ 
    Clase Controler
    La clase Controler actúa como intermediario entre la vista (Ventanita) 
    y la lógica del programa que interactúa con la base de datos. 
    También define las variables necesarias para generar gráficos. 
    
    Attributes: 
        nombres (list): Una lista de nombres de los cursos.
        colores (list): Una lista de colores asociados al grafico de barras. 
        tamano (list): Una lista de cantidad de alumnos por curso.
        ventana (Tk): La ventana principal de la aplicación.
        objeto_vista (Ventanita): La vista asociada a la ventana.
    """
    nombres = ['EGB', 'CFI', 'SUP', 'INTEG']
    colores = ['blue', 'red', 'green', 'yellow']
    tamano = [egb, cfi, superior, integracion]

    
    def __init__(self,ventana):
        """ 
        Constructor de la clase Controler 

        Args: 
            ventana (Tk): Instancia de la clase Ventanita que representa la ventana principal de la aplicación. 
        
        Attributes: 
            ventana (Tk): La ventana principal de la aplicación. 
            objeto_vista (Ventanita): Instancia de la clase Ventanita que administra la interfaz gráfica. 
            el_observador (ConcreteObserverA): Instancia de la clase ConcreteObserverA que implementa el patrón observador
        """

        self.ventana=ventana
        self.objeto_vista = Ventanita(self.ventana, self.nombres, self.colores, self.tamano)
        self.el_observador= observador.ConcreteObserverA(self.objeto_vista.objeto_base)
        
       
        
if __name__ == "__main__":
    
    """ 
    Inicializa la aplicación principal creando una instancia de TK 
    Este bloque de código inicializa una instancia de `Controler`, pasando window como parametro 
    Se llama al método 'actualizar' de la vista.
    Finalmente, inicia el bucle principal de la ventana. 
    
    Attributes: 
        window (tk.Tk): Instancia de la ventana principal de la aplicación. 
        aplicacion (Controler): Instancia de la clase `Controler` que administra la lógica de la aplicación. 
    """
    #theproc=""
    window = Tk()
    aplicacion=Controler(window)
    aplicacion.objeto_vista.actualizar()
   
    window.mainloop()
