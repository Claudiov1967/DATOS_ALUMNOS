from tkinter import Label, Entry, Button, ttk, Frame, Tk, StringVar
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar
import tkinter as tk
from tkinter.messagebox import showinfo, showwarning
from datetime import datetime
import random
from modelo import Abmc#, Alumno2
from modelo import egb, cfi, superior, integracion



class Ventanita():

    # EL CONSTRUCTOR TIENE PARAMETROS DE LA VENTANA, Y LOS DEMAS SON PARA EL GRAFICO DE ALUMNOS
    def __init__(self, window, nombres, colores, tamano, graf=True):
        self.root = window
        self.nombres = nombres
        self.colores = colores
        self.tamano = tamano
        self.graf = graf

        self.root.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)
        self.root.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        pad_x = 10
        pad_y = 5
        self.root.title("SISTEMA DE GESTION DE DATOS")

        # color fondo de la grilla de la ventana root
        self.root.configure(bg="#2F4F4F", padx=pad_x, pady=pad_y)

        # Titulo principal de la ventana         
        self.titulo = Label(self.root, text="SISTEMA DE GESTION DE DATOS E INGRESOS DE ALUMNOS",
                        bg="green", fg="thistle1", height=1, width= 60,font=("Garamond", 15,"bold"))
        self.titulo.grid(row=0, column=0, columnspan=8, padx=pad_x, pady=pad_y, sticky='ew')

        ###################
        # GRAFICO ALUMNOS POR CURSO
        # crear un frame dentro de la ventana
        self.frame = Frame(self.root, bg='green')
        self.frame.grid(column=4, row=1, rowspan=5)

        # Crear la figura y los ejes
        self.fig, self.ax = plt.subplots(dpi=80, figsize=(6, 3), facecolor="green")

        # Crear un grafico de barras en el primer eje
        self.ax.bar(self.nombres, self.tamano, color= self.colores)
        self.ax.set_title('ALUMNOS POR CURSO')
        print("ax: ", self.ax)

        # Integrar la figura en tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=4, row=1, rowspan=5, columnspan=2)

        ######################################################################
        # widgets con los nombres de los campos a conpletar por cada registro
        self.nombre = Label(self.root, text="Nombre/s", font=("Candara",13), width=15)
        self.nombre.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky='w')
        self.apellido =Label(self.root, text="Apellido/s", font=("Candara",13),width=15)
        self.apellido.grid(row=2, column=0,padx=pad_x, pady=pad_y,  sticky='w')
        self.curso =Label(self.root, text="Curso      ", font=("Candara",13),width=15)
        self.curso.grid(row=3, column=0, padx=pad_x, pady=pad_y,  sticky='w')
        self.documento =Label(self.root, text="Documento", font=("Candara",13), width=15)
        self.documento.grid(row=4, column=0,padx=pad_x, pady=pad_y,  sticky='w')
        self.domicilio =Label(self.root, text="Domicilio", font=("Candara",13), width=15)
        self.domicilio.grid(row=5, column=0, padx=pad_x, pady=pad_y,  sticky='w')
        self.telefono =Label(self.root, text="Telefono", font=("Candara",13), width=15)
        self.telefono.grid(row=6, column=0,padx=pad_x, pady=pad_y, sticky='w')
        self.nacimiento = Label(self.root, text="F. Nac.", font=("Candara",13), width=15)
        self.nacimiento.grid(row=7, column=0,padx=pad_x, pady=pad_y, sticky='w')
        self.mail = Label(self.root, text="Email", font=("Candara",13), width=15)
        self.mail.grid(row=8, column=0, padx=pad_x, pady=pad_y, sticky="w")
        self.edad = Label(self.root, text="Edad", font=("Candara",13), width=15)
        self.edad.grid(row=9, column=0,padx=pad_x, pady=pad_y, sticky='w')
        self.edad2 = Label(self.root, text="xx", font=("Candara",13), width=25,bg="lightgreen")
        self.edad2.grid(row=9, column=1,padx=pad_x, pady=pad_y) 
        self.edad2 = Label(self.root, text="Desarrollado por Claudio Valko", font=("Candara",13), width=25,bg="white")
        self.edad2.grid(row=16, column=5,padx=pad_x, pady=pad_y) 

        ###  VARIABLES CAMPO DE ENTRADA TKINTER ##########################
        (
        self.nombre_val, 
        self.apellido_val, 
        self.curso_val, 
        self.documento_val, 
        self.domicilio_val, 
        self.tel_val, 
        self.nac_val,
        self.mail_val
        ) = (StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar())

        w_ancho = 25

        entrada1 = Entry(self.root, textvariable = self.nombre_val, width = w_ancho,font=("Candara",13)) 
        entrada1.grid(row = 1, column = 1,padx=pad_x, pady=pad_y)
        entrada2 = Entry(self.root, textvariable = self.apellido_val, width = w_ancho, font=("Candara",13)) 
        entrada2.grid(row = 2, column = 1, padx=pad_x, pady=pad_y)
        entrada3 = ttk.Combobox(self.root, textvariable = self.curso_val, width = w_ancho, font=("Candara",13)) 
        entrada3.grid(row = 3, column = 1, padx=pad_x, pady=pad_y)
        entrada3['values'] = ('egb',  
                                'cfi', 
                                'superior', 
                                'integracion', 
                                'ex'
                                ) 
        entrada4 = Entry(self.root, textvariable = self.documento_val, width = w_ancho, font=("Candara",13)) 
        entrada4.grid(row = 4, column = 1, padx=pad_x, pady=pad_y)
        entrada5 = Entry(self.root, textvariable = self.domicilio_val, width = w_ancho, font=("Candara",13)) 
        entrada5.grid(row = 5, column = 1, padx=pad_x, pady=pad_y)
        entrada6 = Entry(self.root, textvariable = self.tel_val, width = w_ancho, font=("Candara",13)) 
        entrada6.grid(row = 6, column = 1, padx=pad_x, pady=pad_y)
        entrada7 = Entry(self.root, textvariable = self.nac_val, width = w_ancho, font=("Candara",13)) 
        entrada7.grid(row = 7, column = 1, padx=pad_x, pady=pad_y)
        entrada8 = Entry(self.root, textvariable = self.mail_val, width = w_ancho, font=("Candara",13)) 
        entrada8.grid(row = 8, column = 1, padx=pad_x, pady=pad_y)


        ################################################
        # calendario
        self.calendario = Calendar(self.root, selectmode="day", background="green",selectbackground="black", normalbackground="#00ff40",
                                weekendbackground="#00ff40", othermonthbackground="#008040", othermonthwebackground="#008040",font=("Candara", 13) )
        self.calendario.grid(row=1, column=2, rowspan=6, padx=pad_x, pady=pad_y)
        ################################################
        ###############################################
        # IMAGEN:logo (DEBE ESTAR EN LA MISMA CARPETA)
        ##############################################
        image1 = Image.open("logo.png")
        image1 = image1.resize((100, 100))
        self.image1 = ImageTk.PhotoImage(image1)
        self.label1 = tk.Label(image=self.image1)
        self.label1.grid(row=1, column=5, rowspan=4, padx=pad_x, pady=pad_y)

        ##################################################
        # TREEVIEW
        ##################################################

        self.tree = ttk.Treeview(self.root)
        self.tree.columnconfigure
        # STYLE TREEVIEW
        self.style = ttk.Style()
        self.style.theme_use("alt")
        # Cambiar la fuente y tamaño  Cambiar 'Arial' y '12' 
        self.style.configure("Treeview",font=('Candara', 13), rowheight=30)
        self.style.configure("Treeview.Heading",font=('Candara', 13, 'bold'))
        
        self.tree["columns"]=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8")
        self.tree.column("#0", width=70, minwidth=50)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=120, minwidth=80)
        self.tree.column("col4", width=120, minwidth=80)
        self.tree.column("col5", width=300, minwidth=80)
        self.tree.column("col6", width=140, minwidth=80)
        self.tree.column("col7", width=120, minwidth=80)
        self.tree.column("col8", width=240, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="NOMBRE")
        self.tree.heading("col2", text="APELLIDO")
        self.tree.heading("col3", text="CURSO")
        self.tree.heading("col4", text="DOCUMENTO")
        self.tree.heading("col5", text="DOMICILIO")
        self.tree.heading("col6", text="TELEFONO")
        self.tree.heading("col7", text="F. NACIM.")
        self.tree.heading("col8", text="EMAIL")
        self.tree.grid(row=15, column=0, columnspan=6, padx=pad_x, pady=pad_y)

        
        
        ##################################
        # BOTONES DE CONTROL
        ##################################
        
        boton_alta =Button(self.root, text="ALTA", command=self.show_alta, font=("Candara",13), width=15)
        boton_alta.grid(row=12, column=0, padx=pad_x, pady=pad_y)
        
        boton_borrar =Button(self.root, text="BORRAR", command=self.show_borrar, font=("Candara",13), width=15)
        boton_borrar.grid(row=13, column=0, padx=pad_x, pady=pad_y)
        
        boton_modificar =Button(self.root, text="MODIFICAR", command=self.show_modificar, font=("Candara",13), width=15)
        boton_modificar.grid(row=13, column=1, padx=pad_x, pady=pad_y)
        
        boton_consultar =Button(self.root, text="CONSULTAR", command=self.show_consultar, font=("Candara",13), width=15)
        boton_consultar.grid(row=12, column=1, padx=pad_x, pady=pad_y)

        boton_fecha = Button(self.root, text="ACEPTAR", command=lambda: self.elegir_fecha(), bg="white", fg="black", font=("Candara",13), width=15)
        boton_fecha.grid(row=7, column=2, padx=pad_x, pady=pad_y)

        boton_sorpresa = Button(self.root, text="SORPRESA", command=lambda:self.cambiar_colores(), bg="white",
                                fg="black", font=("Candara",13), width=15)
        boton_sorpresa.grid(row=11, column=5, padx=pad_x, pady=pad_y)

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

    def elegir_fecha(self,):
        self.nac_val.set("")
        print("El dia elegido es: " + self.calendario.get_date())
        fecha = self.calendario.get_date()
        fecha_obj = datetime.strptime(fecha, "%m/%d/%y")
        fecha_formateada = fecha_obj.strftime("%d/%m/%y")
        self.nac_val.set(fecha_formateada)

    ## LLAMA A ALTA Y RETORNA LO QUE SE DEBE MOSTRAR EN CONSOLA Y UNA LISTA CON ITEMS PARA MODIFICAR EL TREEVIEW
    def show_alta(self,):  
        alumno = Abmc(
        self.nombre_val.get(), 
        self.apellido_val.get(), 
        self.curso_val.get(), 
        self.documento_val.get(), 
        self.domicilio_val.get(), 
        self.tel_val.get(), 
        self.nac_val.get(),
        self.mail_val.get()
        )
  
        retorno, resultado = alumno.alta(self)
        print(self.graf, self.tamano)
           
        if self.graf:
            self.actualizar_treeview(resultado)
            self.actualizar_grafico(self.tamano)
            self.nombre_val.set("")
            self.apellido_val.set("")
            self.curso_val.set("")
            self.documento_val.set("")
            self.domicilio_val.set("")
            self.tel_val.set("")
            self.nac_val.set("")
            self.edad2.config(text="") 
            self.mail_val.set("")
            showinfo("INFORMACION", retorno)
        else:
            showwarning("ADVERTENCIA",retorno )

    def actualizar_treeview(self,resultado):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        for fila in resultado:
            print(fila)
            self.tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7] ,fila[8]))

    def actualizar_grafico(self,tamaño):
        print("ax:",self.ax)
        print(self.tamano)
        # Limpiar el gráfico actual
        self.ax.clear()
        self.ax.bar(self.nombres, tamaño, color=self.colores)
        # Redibujar el gráfico
        self.canvas.draw()

    def actualizar(self,):
        alumno = Abmc(
            self.nombre_val.get(),
            self.apellido_val.get(),
            self.curso_val.get(),
            self.documento_val.get(),
            self.domicilio_val.get(),
            self.tel_val.get(),
            self.nac_val.get(),
            self.mail_val.get()
            )
        resultado, documentos= alumno.alumnos_cursos(self)
        self.actualizar_treeview(resultado)
        self.actualizar_grafico(self.tamano)
        print(self.graf)

    def show_borrar(self,):
        alumno = Abmc(
            self.nombre_val.get(),
            self.apellido_val.get(),
            self.curso_val.get(),
            self.documento_val.get(),
            self.domicilio_val.get(),
            self.tel_val.get(),
            self.nac_val.get(),
            self.mail_val.get()

            )
        retorno, resultado = alumno.borrar(self.tree, self)
        print(self.graf, self.tamano)
        if self.graf:
            self.actualizar_grafico(self.tamano)
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
        alumno = Abmc(
            self.nombre_val.get(),
            self.apellido_val.get(),
            self.curso_val.get(),
            self.documento_val.get(),
            self.domicilio_val.get(),
            self.tel_val.get(),
            self.nac_val.get(),
            self.mail_val.get()
            )
        retorno, resultado = alumno.modificar(item, self)  
        if self.graf:       
            self.actualizar_grafico(self.tamano)
            self.actualizar_treeview(resultado)
            self.nombre_val.set("")
            self.apellido_val.set("")
            self.curso_val.set("")
            self.documento_val.set("")
            self.domicilio_val.set("")
            self.tel_val.set("")
            self.nac_val.set("")
            self.mail_val.set("")
            self.edad2.config(text="") 
            showinfo("INFORMACION", retorno)
        else:
            showwarning("ADVERTENCIA",retorno )
    
    def show_consultar(self,):
        valor = self.tree.selection()
        if not valor:
            showwarning("ADVERTENCIA","Por favor seleccione una fila para consultar." )
        print("valor:",valor)   
        item = self.tree.item(valor)  
        alumno = Abmc(
            self.nombre_val.get(),
            self.apellido_val.get(),
            self.curso_val.get(),
            self.documento_val.get(),
            self.domicilio_val.get(),
            self.tel_val.get(),
            self.nac_val.get(),
            self.mail_val.get()
            )      
        retorno, edad = alumno.consultar(item, self) 
        print("WWWWWWWEDADWWWWWWWWWWWWWWWWWWW", edad)
        self.edad2.config(text="24dias")

        showinfo("INFORMACION", retorno)



