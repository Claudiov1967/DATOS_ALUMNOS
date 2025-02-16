from tkinter import Label, Entry, Button, ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame, Tk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import StringVar
from tkinter.messagebox import showinfo, showwarning
from datetime import datetime
import random
from modelo import alta, borrar ,modificar, consultar
from modelo import alumnos_cursos
from modelo import egb, cfi, superior, integracion, graf

#SOLO IMPLEMENTA CLASE EN VISTA
"""VISTA_MVC TIENE SEPARACION MVC. NO SE PASA TREE A MODELO, SOLO ITEM 
EL MODELO NO TIENE UNA CLASE ABMC"""

class Ventanita():

    def __init__(self, window):
        self.root = window

        # Datos para el grafico
        #egb, cfi, superior, integracion= 1,2,3,4
        self.nombres = ['EGB', 'CFI', 'SUP', 'INTEG']
        self.colores = ['blue', 'red', 'green', 'yellow']
        self.tamaño = [egb, cfi, superior, integracion]
    
        self.root.title("SISTEMA DE GESTION DE DATOS")

        # color fondo de la grilla de la ventana root
        self.root.configure(bg="#2F4F4F", padx=20, pady=20)
        # Titulo principal de la ventana         
        self.titulo = Label(self.root, text="SISTEMA DE GESTION DE DATOS E INGRESOS DE ALUMNOS",
                    bg="green", fg="thistle1", height=1, width= 60,font=("Garamond", 14,"bold"))
        self.titulo.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky='w')

                ###################

        # GRAFICO
        # crear un frame dentro de la ventana
        self.frame = Frame(self.root, bg='green')
        self.frame.grid(column=4, row=1, rowspan=5)

        # Crear la figura y los ejes
        self.fig, self.ax = plt.subplots(dpi=80, figsize=(4, 2), facecolor="green")

        # Crear un grafico de barras en el primer eje
        self.ax.bar(self.nombres, self.tamaño, color= self.colores)
        self.ax.set_title('ALUMNOS POR CURSO')
        
        print("ax: ", self.ax)

        # Integrar la figura en tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=4, row=1, rowspan=5, columnspan=2)

        #######################################
        # widgets con los nombres de los campos a conpletar por cada registro
        self.nombre = Label(self.root, text="Nombre/s", font=("Candara",12), width=15)
        self.nombre.grid(row=1, column=0, sticky='w')
        self.apellido=Label(self.root, text="Apellido/s", font=("Candara",12),width=15)
        self.apellido.grid(row=2, column=0, sticky='w')
        self.curso=Label(self.root, text="Curso      ", font=("Candara",12),width=15)
        self.curso.grid(row=3, column=0, sticky='w')
        self.documento=Label(self.root, text="Documento", font=("Candara",12), width=15)
        self.documento.grid(row=4, column=0, sticky='w')
        self.domicilio=Label(self.root, text="Domicilio", font=("Candara",12), width=15)
        self.domicilio.grid(row=5, column=0, sticky='w')
        self.telefono=Label(self.root, text="Telefono", font=("Candara",12), width=15)
        self.telefono.grid(row=6, column=0, sticky='w')
        self.nacimiento= Label(self.root, text="F. Nac.", font=("Candara",12), width=15)
        self.nacimiento.grid(row=7, column=0, sticky='w')

        # Variables campos de Entrada
        self.nombre_val, self.apellido_val, self.curso_val, self.documento_val, self.domicilio_val, self.tel_val, self.nac_val = StringVar(),StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        w_ancho = 20

        entrada1 = Entry(self.root, textvariable = self.nombre_val, width = w_ancho,font=("Candara",12)) 
        entrada1.grid(row = 1, column = 1)
        entrada2 = Entry(self.root, textvariable = self.apellido_val, width = w_ancho, font=("Candara",12)) 
        entrada2.grid(row = 2, column = 1)
        entrada3 = ttk.Combobox(self.root, textvariable = self.curso_val, width = w_ancho, font=("Candara",12)) 
        entrada3.grid(row = 3, column = 1)
        entrada3['values'] = ('egb',  
                                'cfi', 
                                'superior', 
                                'integracion', 
                                'ex'
                                ) 
        entrada4 = Entry(self.root, textvariable = self.documento_val, width = w_ancho, font=("Candara",12)) 
        entrada4.grid(row = 4, column = 1)
        entrada5 = Entry(self.root, textvariable = self.domicilio_val, width = w_ancho, font=("Candara",12)) 
        entrada5.grid(row = 5, column = 1)
        entrada6 = Entry(self.root, textvariable = self.tel_val, width = w_ancho, font=("Candara",12)) 
        entrada6.grid(row = 6, column = 1)
        entrada7 = Entry(self.root, textvariable = self.nac_val, width = w_ancho, font=("Candara",12)) 
        entrada7.grid(row = 7, column = 1)


        ################################################
        # calendario
        self.calendario = Calendar(self.root, selectmode="day", background="green",selectbackground="black", normalbackground="#00ff40",
                                weekendbackground="#00ff40", othermonthbackground="#008040", othermonthwebackground="#008040", )
        self.calendario.grid(row=1, column=2, rowspan=6)
        ################################################
        ###############################################
        # IMAGEN:logo (DEBE ESTAR EN LA MISMA CARPETA)
        ##############################################
        image1 = Image.open("logo.png")
        image1 = image1.resize((100, 100))
        self.image1 = ImageTk.PhotoImage(image1)
        self.label1 = tk.Label(image=self.image1)
        self.label1.grid(row=1, column=5, rowspan=4)

        ##################################################
        # TREEVIEW
        ##################################################

        self.tree = ttk.Treeview(self.root)
        # STYLE TREEVIEW
        self.style = ttk.Style()
        self.style.theme_use("alt")

        self.tree["columns"]=("col1", "col2", "col3", "col4", "col5", "col6", "col7")
        self.tree.column("#0", width=90, minwidth=50)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.column("col4", width=200, minwidth=80)
        self.tree.column("col5", width=200, minwidth=80)
        self.tree.column("col6", width=200, minwidth=80)
        self.tree.column("col7", width=200, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="NOMBRE")
        self.tree.heading("col2", text="APELLIDO")
        self.tree.heading("col3", text="CURSO")
        self.tree.heading("col4", text="DOCUMENTO")
        self.tree.heading("col5", text="DOMICILIO")
        self.tree.heading("col6", text="TELEFONO")
        self.tree.heading("col7", text="F. NACIMIENTO")
        self.tree.grid(row=13, column=0, columnspan=6)

        ##################################
        # BOTONES DE CONTROL
        ##################################

        boton_alta=Button(self.root, text="Alta", command=self.show_alta, font=("Candara",12), width=15)
        boton_alta.grid(row=10, column=0)

        boton_borrar=Button(self.root, text="Borrar", command=self.show_borrar, font=("Candara",12), width=15)
        boton_borrar.grid(row=11, column=0)

        boton_modificar=Button(self.root, text="Modificar", command=self.show_modificar, font=("Candara",12), width=15)
        boton_modificar.grid(row=11, column=1)

        boton_consultar=Button(self.root, text="Consultar", command=self.show_consultar, font=("Candara",12), width=15)
        boton_consultar.grid(row=10, column=1)

        boton_fecha = Button(self.root, text="ACEPTAR", command=lambda: self.elegir_fecha(), bg="black", fg="white", font=("Candara",12), width=15)
        boton_fecha.grid(row=10, column=2)

        boton_sorpresa = Button(self.root, text="SORPRESA", command=lambda:self.cambiar_colores(), bg="white",
                                fg="black", font=("Candara",12), width=15)
        boton_sorpresa.grid(row=9, column=5)


    
    def show_alta(self,):
        graf, tamaño,retorno, resultado = alta(self.nombre_val, self.apellido_val, self.curso_val, self.documento_val, self.domicilio_val, self.tel_val, self.nac_val)
        print(graf, tamaño)
        if graf == True:
            print("graf", graf)
            self.actualizar_treeview(resultado)
            self.actualizar_grafico(tamaño)
            showinfo("INFORMACION", retorno)
        else:
            showwarning("ADVERTENCIA",retorno)

    def show_consultar(self,):
        valor = self.tree.selection()
        if not valor:
            showwarning("ADVERTENCIA","Por favor seleccione una fila para consultar." )
        print("valor:",valor)   
        item = self.tree.item(valor)        
        retorno = consultar(self.nombre_val, self.apellido_val, self.curso_val, self.documento_val, self.domicilio_val, self.tel_val, self.nac_val, item)  
        showinfo("INFORMACION", retorno)

    def actualizar_treeview(self, resultado):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        for fila in resultado:
            print(fila)
            self.tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7]))
    
    def actualizar_grafico(self,tamaño): 
        print("ax:",self.ax)
        print(tamaño)
        # Limpiar el gráfico actual
        self.ax.clear()
        self.ax.bar(self.nombres, tamaño, color=self.colores)
        # Redibujar el gráfico
        self.canvas.draw()

    def elegir_fecha(self,):
        self.nac_val.set("")
        print("El dia elegido es: " + self.calendario.get_date())
        fecha = self.calendario.get_date()
        fecha_obj = datetime.strptime(fecha, "%m/%d/%y")
        fecha_formateada = fecha_obj.strftime("%d/%m/%y")
        self.nac_val.set(fecha_formateada)

    def show_borrar(self,):
        valor = self.tree.selection()
        if not valor:
             showwarning("ADVERTENCIA","Por favor seleccione una fila para consultar." )
        print("valor:",valor)   
        item = self.tree.item(valor)
        self.tree.delete(valor)
        graf, tamaño, retorno, resultado = borrar(item)
        print(graf, tamaño)
        if graf:
            #actualizar_grafico(tamaño)
            self.actualizar_treeview(resultado)
        showinfo("INFORMACION", retorno)

    def show_modificar(self,):
        valor = self.tree.selection()
        # si no se selecciona un registro para modificar informa error
        if not valor:
            showwarning("ADVERTENCIA","Por favor seleccione una fila para consultar." )
            exit
        print("valor:",valor)   
        item = self.tree.item(valor)
            
        graf, tamaño, retorno, resultado = modificar(self.nombre_val, self.apellido_val, self.curso_val, self.documento_val, self.domicilio_val, self.tel_val, self.nac_val, item)  
        if graf:       
            self.actualizar_grafico(tamaño)
            self.actualizar_treeview(resultado)
            showinfo("INFORMACION", retorno)
        else:
            showwarning("ADVERTENCIA",retorno )

    def cambiar_colores(self,):
        colores= ['snow', 'old lace', 'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque',
                'peach puff', 'alice blue','navajo white', 'lavender', 'misty rose', 'dark slate gray',
                'dim gray', 'light slate gray', 'gray', 'light gray', 'midnight blue', 'navy',
                'cornflower blue', 'dark slate blue', 'medium slate blue', 'light slate blue', 'medium blue',
                'royal blue', 'blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
                'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise','cyan',
                'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
                'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
                'lawn green', 'RosyBrown1','IndianRed3', 'burlywood2', 'tan2', 'tan4', 'firebrick3', 'medium spring green',
                'green yellow', 'lime green', 'yellow green', 'RosyBrown2', 'indianRed4', 'burlywood3', 'chocolate1',
                'firebrick4', 'RosyBrown3', 'siennal', 'burlywood4', 'chocolate2', 'RosyBrown4', 'IndianRed1',
                'IndianRed2', 'sienna2', 'sienna3', 'sienna4', 'burlywood1', 'wheat1', 'wheat2', 'wheat3', 'wheat4',
                'tan1', 'chocolate3', 'firebrick1', 'firebrick2', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1',
                'salmon2', 'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2', 'DarkOrange1',
                'DarkOrange2','coral1', 'tomato2', 'OrangeRed2']
        color = random.choice(colores)
        self.root.configure(background=color) 

    def actualizar(self,):
        graf, tamaño , resultado= alumnos_cursos()
        self.actualizar_treeview(resultado)
        self.actualizar_grafico(tamaño)
        print(graf)

if __name__ == "__main__":
    window = Tk()
    app = Ventanita(window)
    try:
        app.actualizar()
    except:
        print("FALLO DE TK")

    window.mainloop()
