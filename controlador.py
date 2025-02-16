from tkinter import Label, Entry, Button, ttk, Frame, Tk, StringVar
import tkinter as tk
from modelo import egb, cfi, superior, integracion
from vista import Ventanita

class Controler:
    nombres = ['EGB', 'CFI', 'SUP', 'INTEG']
    colores = ['blue', 'red', 'green', 'yellow']
    tamaño = [egb, cfi, superior, integracion]

    def __init__(self,ventana):
        self.ventana=ventana
        app = Ventanita(self.ventana, self.nombres, self.colores, self.tamaño)
        app.actualizar()


if __name__ == "__main__":
    window = Tk()
    aplicacion=Controler(window)
        
    window.mainloop()
