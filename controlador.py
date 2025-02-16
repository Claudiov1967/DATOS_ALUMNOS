# Este codigo tiene incluido una base de datos que se conecta a traves de peewee
# Tiene tambien una programacion POO
# y esta dividida en MVC

from tkinter import Tk 
from modelo import egb, cfi, superior, integracion
from vista import Ventanita

class Controler:
    nombres = ['EGB', 'CFI', 'SUP', 'INTEG']
    colores = ['blue', 'red', 'green', 'yellow']
    tamano = [egb, cfi, superior, integracion]

    def __init__(self,ventana):
        self.ventana=ventana
        app = Ventanita(self.ventana, self.nombres, self.colores, self.tamano)
        app.actualizar()


if __name__ == "__main__":
    window = Tk()
    aplicacion=Controler(window)
        
    window.mainloop()
