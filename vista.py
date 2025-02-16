"""
Vista de la aplicacion
Muestra la información a los usuarios y maneja la interacción con ellos
"""
from tkinter import Label, Entry, Button, ttk, Frame, Tk, StringVar
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar
import tkinter as tk
from tkinter.messagebox import showinfo, showwarning
from datetime import datetime
import random
from modelo import Abmc 
from modelo import egb, cfi, superior, integracion
import os
from pathlib import Path
import threading
import subprocess
import sys
from icecream import ic



class Ventanita():
    """ 
    Clase que crea una ventana de gestión de datos e ingresos de alumnos.
     
    Args:      
        window (tkinter.Tk): Ventana principal de Tkinter. 
        nombres (list): Lista de nombres de alumnos. 
        colores (list): Lista de colores para cada barra en el gráfico. 
        tamano (list): Lista de tamaños para cada barra en el gráfico. 
        graf (bool): Determina si se actualizará el gráfico (default es True). 
        
    Attributes:
        root (tkinter.Tk): Ventana principal de Tkinter. 
        nombres (list): Lista de nombres de alumnos. 
        colores (list): Lista de colores para cada barra en el gráfico. 
        tamano (list): Lista de tamaños para cada barra en el gráfico. 
        graf (bool): Determina si se mostrará el gráfico. 
        nombre_val (tkinter.StringVar): Variable String para el nombre. 
        apellido_val (tkinter.StringVar): Variable String para el apellido. 
        curso_val (tkinter.StringVar): Variable String para el curso. 
        documento_val (tkinter.StringVar): Variable String para el documento. 
        domicilio_val (tkinter.StringVar): Variable String para el domicilio. 
        tel_val (tkinter.StringVar): Variable String para el teléfono. 
        nac_val (tkinter.StringVar): Variable String para la fecha de nacimiento. 
        mail_val (tkinter.StringVar): Variable String para el email. 
        edad_val (tkinter.StringVar): Variable String para la edad. 
        objeto_base (Abmc): Objeto base para la gestión de alumnos. 
        
    Méthods: 
        cambiar_colores(): 
            Cambia el color de fondo de la ventana a un color aleatorio. 
        elegir_fecha(): 
            Formatea y establece la fecha seleccionada en el calendario. 
        show_alta():
            Muestra el proceso de alta de un alumno. 
        actualizar_treeview(resultado): 
            Actualiza el treeview con los resultados proporcionados. 
        actualizar_grafico(tamano): 
            Actualiza el gráfico con los tamaños proporcionados. 
        actualizar(): 
            Actualiza el treeview y el gráfico con datos actuales. 
        show_borrar(): 
            Muestra el proceso de borrado de un alumno. 
        show_modificar(): 
            Muestra el proceso de modificación de datos de un alumno. 
        show_consultar(): 
            Muestra el proceso de consulta de datos de un alumno. 
        """
    def __init__(self, window, nombres, colores, tamano, graf=True):       
        """
        Constructor de la clase Ventanita.
        
        Args:
        window (Tk): La ventana gráfica.
        nombres (list): Lista con nombres de las barras del gráfico.
        colores (list): Lista con los colores de las barras del gráfico.
        tamano (list): Lista con la cantidad de alumnos en cada curso.
        graf (bool): Si es True se actualiza el gráfico. Por defecto es True.

    Attributes:
        root (Tk): La ventana principal de la aplicación.
        nombres (list): Lista con nombres de las barras del gráfico.
        colores (list): Lista con los colores de las barras del gráfico.
        tamano (list): Lista con la cantidad de alumnos en cada curso.
        graf (bool): Indica si se debe actualizar el gráfico.
        nombre_val (StringVar): Variable para el nombre del alumno.
        apellido_val (StringVar): Variable para el apellido del alumno.
        curso_val (StringVar): Variable para el curso del alumno.
        documento_val (StringVar): Variable para el documento del alumno.
        domicilio_val (StringVar): Variable para el domicilio del alumno.
        tel_val (StringVar): Variable para el teléfono del alumno.
        nac_val (StringVar): Variable para la fecha de nacimiento del alumno.
        mail_val (StringVar): Variable para el email del alumno.
        edad_val (StringVar): Variable para la edad del alumno.
        objeto_base (Abmc): Instancia de la clase Abmc.
        raiz (Path): Directorio base del archivo.
        ruta_server (str): Ruta completa del archivo del servidor.
        theproc (subprocess.Popen): Proceso del servidor
        titulo (Label): Instancia de la clase Label que muestra el título de la aplicación.
        frame (Frame): Instancia de la clase Frame que actúa como contenedor para otros widgets.
        canvas (FigureCanvasTkAgg): Instancia de la clase FigureCanvasTkAgg para mostrar gráficos.
        tree (ttk.Treeview): Instancia de la clase Treeview para mostrar datos en forma de tabla.
        style (ttk.Style): Instancia de la clase Style para personalizar la apariencia de los widgets.
        calendario (Calendar): Instancia de la clase Calendar para seleccionar fechas.
        boton_alta (Button): Botón para dar de alta un nuevo registro.
        boton_borrar (Button): Botón para borrar un registro existente.
        boton_modificar (Button): Botón para modificar un registro existente.
        boton_consultar (Button): Botón para consultar registros.
        boton_fecha (Button): Botón para aceptar la fecha seleccionada.
        boton_sorpresa (Button): Botón para cambiar colores de la interfaz.
        boton_lanzar (Button): Botón para lanzar el servidor.
        boton_apagar (Button): Botón para apagar el servidor.
        image1 (ImageTk.PhotoImage): Instancia de la clase PhotoImage para mostrar una imagen.
        label1 (Label): Instancia de la clase Label que muestra la imagen
                
        """
        self.root = window
        self.nombres = nombres
        self.colores = colores
        self.tamano = tamano
        self.graf = graf
        self.nombre_val= StringVar()
        self.apellido_val= StringVar()
        self.curso_val= StringVar()
        self.documento_val= StringVar()
        self.domicilio_val= StringVar()
        self.tel_val= StringVar()
        self.nac_val= StringVar()
        self.mail_val= StringVar()
        self.edad_val=StringVar()
        self.objeto_base = Abmc()

        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, 'servidor1.py')
        self.theproc = None

        # Configuracion de la ventana principal
        self.root.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)
        self.root.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        pad_x = 8
        pad_y = 3
        self.root.title("SISTEMA DE GESTION DE DATOS")
        self.root.configure(bg="#2F4F4F", padx=pad_x, pady=pad_y)

        # Titulo principal de la ventana         
        self.titulo = Label(self.root, text="SISTEMA DE GESTION DE DATOS E INGRESOS DE ALUMNOS",
                        bg="green", fg="thistle1", height=1, width= 60,font=("Garamond", 14,"bold"))
        self.titulo.grid(row=0, column=0, columnspan=8, padx=pad_x, pady=pad_y, sticky='ew')

        # Gráfico de alumnos por curso
        self.frame = Frame(self.root, bg='green')
        self.frame.grid(column=3, row=1, rowspan=5)

        self.fig, self.ax = plt.subplots(dpi=80, figsize=(4, 2), facecolor="green")
        self.ax.bar(self.nombres, self.tamano, color= self.colores)
        self.ax.set_title('ALUMNOS POR CURSO')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=4, row=1, rowspan=4, columnspan=2)

        # widgets con los nombres de los campos a conpletar por cada registro
        self.nombre = Label(self.root, text="Nombre/s", font=("Candara",12), width=15)
        self.nombre.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky='w')
        self.apellido =Label(self.root, text="Apellido/s", font=("Candara",12),width=15)
        self.apellido.grid(row=2, column=0,padx=pad_x, pady=pad_y,  sticky='w')
        self.curso =Label(self.root, text="Curso      ", font=("Candara",12),width=15)
        self.curso.grid(row=3, column=0, padx=pad_x, pady=pad_y,  sticky='w')
        self.documento =Label(self.root, text="Documento", font=("Candara",12), width=15)
        self.documento.grid(row=4, column=0,padx=pad_x, pady=pad_y,  sticky='w')
        self.domicilio =Label(self.root, text="Domicilio", font=("Candara",12), width=15)
        self.domicilio.grid(row=5, column=0, padx=pad_x, pady=pad_y,  sticky='w')
        self.telefono =Label(self.root, text="Telefono", font=("Candara",12), width=15)
        self.telefono.grid(row=6, column=0,padx=pad_x, pady=pad_y, sticky='w')
        self.nacimiento = Label(self.root, text="F. Nac.", font=("Candara",12), width=15)
        self.nacimiento.grid(row=7, column=0,padx=pad_x, pady=pad_y, sticky='w')
        self.mail = Label(self.root, text="Email", font=("Candara",12), width=15)
        self.mail.grid(row=8, column=0, padx=pad_x, pady=pad_y, sticky="w")
        self.edad = Label(self.root, text="Edad", font=("Candara",12), width=15)
        self.edad.grid(row=9, column=0,padx=pad_x, pady=pad_y, sticky='w')
        self.edad2 = Label(self.root, text="Desarrollado por Claudio Valko", font=("Candara",12), width=25,bg="white")
        self.edad2.grid(row=16, column=5,padx=pad_x, pady=pad_y) 

        # Entradas de datos
        w_ancho = 25
        entrada1 = Entry(self.root, textvariable = self.nombre_val, width = w_ancho,font=("Candara",12)) 
        entrada1.grid(row = 1, column = 1,padx=pad_x, pady=pad_y)
        entrada2 = Entry(self.root, textvariable = self.apellido_val, width = w_ancho, font=("Candara",12)) 
        entrada2.grid(row = 2, column = 1, padx=pad_x, pady=pad_y)
        entrada3 = ttk.Combobox(self.root, textvariable = self.curso_val, width = w_ancho, font=("Candara",12)) 
        entrada3.grid(row = 3, column = 1, padx=pad_x, pady=pad_y)
        entrada3['values'] = ('egb',  
                                'cfi', 
                                'superior', 
                                'integracion', 
                                'ex'
                                ) 
        entrada4 = Entry(self.root, textvariable = self.documento_val, width = w_ancho, font=("Candara",12)) 
        entrada4.grid(row = 4, column = 1, padx=pad_x, pady=pad_y)
        entrada5 = Entry(self.root, textvariable = self.domicilio_val, width = w_ancho, font=("Candara",12)) 
        entrada5.grid(row = 5, column = 1, padx=pad_x, pady=pad_y)
        entrada6 = Entry(self.root, textvariable = self.tel_val, width = w_ancho, font=("Candara",12)) 
        entrada6.grid(row = 6, column = 1, padx=pad_x, pady=pad_y)
        entrada7 = Entry(self.root, textvariable = self.nac_val, width = w_ancho, font=("Candara",12)) 
        entrada7.grid(row = 7, column = 1, padx=pad_x, pady=pad_y)
        entrada8 = Entry(self.root, textvariable = self.mail_val, width = w_ancho, font=("Candara",12)) 
        entrada8.grid(row = 8, column = 1, padx=pad_x, pady=pad_y)
        entrada9 = Entry(self.root, textvariable = self.edad_val, width = w_ancho,bg="lightgreen", font=("Candara",12)) 
        entrada9.grid(row = 9, column = 1, padx=pad_x, pady=pad_y)

        # Calendario
        self.calendario = Calendar(self.root, selectmode="day", background="green",selectbackground="black", normalbackground="#00ff40",
                                weekendbackground="#00ff40", othermonthbackground="#008040", othermonthwebackground="#008040",font=("Candara", 12) )
        self.calendario.grid(row=1, column=2, rowspan=7, padx=pad_x, pady=pad_y)
        ################################################
        ###############################################
        # Imagen:logo (debe estar en la misma carpeta)
        ##############################################
        image1 = Image.open("logo.png")
        image1 = image1.resize((100, 100))
        self.image1 = ImageTk.PhotoImage(image1)
        self.label1 = tk.Label(image=self.image1)
        self.label1.grid(row=1, column=5, rowspan=4, padx=pad_x, pady=pad_y)

        ##################################################
        # Treeview
        ##################################################

        self.tree = ttk.Treeview(self.root)
        self.tree.columnconfigure
        # Style treeview
        self.style = ttk.Style()
        self.style.theme_use("alt")
        # Cambiar la fuente y tamaño  Cambiar 'Arial' y '12' 
        self.style.configure("Treeview",font=('Candara', 11), rowheight=30)
        self.style.configure("Treeview.Heading",font=('Candara', 11, 'bold'))
        
        self.tree["columns"]=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8")
        self.tree.column("#0", width=70, minwidth=50)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=180, minwidth=80)
        self.tree.column("col3", width=120, minwidth=80)
        self.tree.column("col4", width=120, minwidth=80)
        self.tree.column("col5", width=270, minwidth=80)
        self.tree.column("col6", width=115, minwidth=80)
        self.tree.column("col7", width=110, minwidth=80)
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
        self.tree.grid(row=12, column=0, columnspan=6, padx=pad_x, pady=pad_y)
              
        ##################################
        # Botones de control
        ##################################
       
        
        boton_alta =Button(self.root, text="ALTA", command=self.show_alta, font=("Candara",12), width=15)
        boton_alta.grid(row=11, column=0, padx=pad_x, pady=pad_y)
        
        boton_borrar =Button(self.root, text="BORRAR", command=self.show_borrar, font=("Candara",12), width=15)
        boton_borrar.grid(row=11, column=1, padx=pad_x, pady=pad_y)
        
        boton_modificar =Button(self.root, text="MODIFICAR", command=self.show_modificar, font=("Candara",12), width=15)
        boton_modificar.grid(row=11, column=2, padx=pad_x, pady=pad_y)
        
        boton_consultar =Button(self.root, text="CONSULTAR", command=self.show_consultar, font=("Candara",12), width=15)
        boton_consultar.grid(row=11, column=3, padx=pad_x, pady=pad_y)
        
        boton_fecha = Button(self.root, text="ACEPTAR", command=lambda: self.elegir_fecha(), bg="white", fg="black", font=("Candara",12), width=15)
        boton_fecha.grid(row=9, column=2, padx=pad_x, pady=pad_y)
        
        boton_sorpresa = Button(self.root, text="SORPRESA", command=lambda:self.cambiar_colores(), bg="white",
                                fg="black", font=("Candara",12), width=15)
        boton_sorpresa.grid(row=11, column=5, padx=pad_x, pady=pad_y)

        boton_lanzar = Button(self.root, text="LANZAR", command=lambda: self.try_connection(), bg="white", fg="black", font=("Candara",12), width=15)
        boton_lanzar.grid(row=9, column=3, padx=pad_x, pady=pad_y)

        boton_apagar = Button(self.root, text="APAGAR", command=lambda: self.apagar_servidor(), bg="white", fg="black", font=("Candara",12), width=15)
        boton_apagar.grid(row=9, column=5, padx=pad_x, pady=pad_y)
        
    def cambiar_colores(self,):
        """
        Cambia el color de fondo de la ventana a un color aleatorio
        Se selecciona un color aleatorio de una lista predefinida de colores y
        se aplica como color de fondo de la ventana principal.

        Args:
            None
        
        Returns:
            None
        """

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

        """
        Llena el widget nac_val con la fecha seleccionada en el calendario
        La fecha esta en el formato dd/mm/yy
        Se establece en la variable `nac_val`

        Args:
            None
        
        Returns:
            None: No retorna nada.        
        """
        self.nac_val.set("")
        ic("El dia elegido es: " + self.calendario.get_date())
        fecha = self.calendario.get_date()
        fecha_obj = datetime.strptime(fecha, "%m/%d/%y")  
        fecha_formateada = fecha_obj.strftime("%d/%m/%y")
        self.nac_val.set(fecha_formateada)

    
    def show_alta(self,): 
        """
        Llama al metodo alta para hacer el alta de un alumno. 
        Este método recoge los datos de los campos de entrada y llama al método `alta` de `objeto_base`.
        Si hubo algun cambio (alta, baja o modificacion) graf es True,
        se actualiza el treeview y el gráfico con los datos resultantes,
        y restablece los campos de entrada. 
        Muestra un mensaje informativo si se procedio con el alta
        o de advertencia si hubo algun error de carga de datos

        Args:
            None
        
        Returns:
            None
        """ 
         
        retorno, resultado = self.objeto_base.alta(self.nombre_val, self.apellido_val, self.curso_val, self.documento_val, self.domicilio_val, self.tel_val, self.nac_val, self.mail_val, self)
                           
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
            self.edad_val.set("") 
            self.mail_val.set("")
            showinfo("INFORMACION", retorno)
        else:
            showwarning("ADVERTENCIA",retorno )

    def actualizar_treeview(self,resultado):
        
        """ 
        Actualiza el treeview con los resultados proporcionados. 
        Elimina todos los registros actuales en el treeview y luego inserta
        los nuevos registros desde los resultados.
         
        Args: 
            resultado (list): Lista de tuplas con los datos de los registros 
            a insertar en el treeview. 
            
        Returns: 
            None 
        """
    
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        for fila in resultado:
            self.tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7] ,fila[8]))

    def actualizar_grafico(self,tamano):
        
        """
        Actualiza el gráfico con los tamaños proporcionados. 
        Limpia el gráfico actual y dibuja un nuevo gráfico de barras 
        con los nombres y tamaños proporcionados. 
        Luego, redibuja el gráfico en el canvas. 
        
        Args: 
            tamano (list): Lista de tamaños para cada barra en el gráfico. 
            
        Returns: 
            None 
        """
        
        # Limpiar el gráfico actual
        self.ax.clear()
        self.ax.bar(self.nombres, tamano, color=self.colores)
        # Redibujar el gráfico
        self.canvas.draw()
    
    def actualizar(self,):
         
        """
        Actualiza el treeview y el gráfico con datos actuales. 
        Llama al método `alumnos_cursos` de `objeto_base` para obtener 
        los datos actuales de los alumnos y cursos. 
        Luego, actualiza el treeview y el gráfico con los resultados obtenidos. 
        
        Args: 
            None 
        Returns: 
            None 
        """

        resultado, documentos= self.objeto_base.alumnos_cursos(self)
        self.actualizar_treeview(resultado)
        self.actualizar_grafico(self.tamano)
        print(self.graf)
        
    def show_borrar(self,):

        """
        Elimina un alumno de la base de datos. 
        Este método llama al método `borrar` de `objeto_base` para eliminar 
        un registro seleccionado en el treeview. Si el gráfico está habilitado,
        actualiza el treeview y el gráfico con los datos resultantes. 
        Muestra un mensaje de informacion. 
        
        Args: 
            None 
        Returns: 
            None 
        """
        
        retorno, resultado = self.objeto_base.borrar(self.tree, self)
        print(self.graf, self.tamano)
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
            self.edad_val.set("") 
            self.mail_val.set("")

        showinfo("INFORMACION", retorno)
    
    def show_modificar(self,):

        """ 
        Llama al metodo modificar para actualizar los datos en la base de datos
          
        Este método recoge los datos del registro seleccionado en el treeview 
        y llama al método `modificar` de `objeto_base`. 
        Si hubo algun cambio (alta, baja o modificacion) graf es True,
        se actualiza el treeview y el gráfico con los datos resultantes,
        y restablece los campos de entrada. 
        Muestra un mensaje informativo si se procedio con la modificacion
        o de advertencia si hubo algun error de carga de datos. 
        
        Args: 
            None 
        Returns: 
            None 
        """

        valor = self.tree.selection()
        
        if not valor:
            showwarning("ADVERTENCIA", "Por favor seleccione una fila para consultar.")
            return
                
        item = self.tree.item(valor)
        retorno, resultado = self.objeto_base.modificar(item,self.nombre_val, self.apellido_val, self.curso_val, self.documento_val, self.domicilio_val, self.tel_val, self.nac_val, self.mail_val, self)
                      
           
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
            self.edad_val.set("")

            showinfo("INFORMACION", retorno)
        else:
            showwarning("ADVERTENCIA",retorno)

    def show_consultar(self,):      
    
        """ 
        Consulta y muestra la información de un alumno.
        Llama al método `consultar` de `objeto_base` para obtener la información de un alumno.
        Corrobora que se haya seleccionado una fila en el treeview. 
        El método `consultar` retorna un string con la información a ser desplegada en pantalla 
        y la edad del alumno. La edad se muestra en el widget correspondiente y se despliega la información en pantalla.
         
        Args: 
            None 
        Returns: 
            None
        """
        retorno, edad = self.objeto_base.consultar(self.tree, self)
        self.edad_val.set(f"{edad[0]} años, {edad[1]} meses, {edad[2]} días")
        showinfo("INFORMACION", retorno)
        return
    
    def lanzar_servidor(self,var):
        """
    Lanza el servidor.

    Llama al método `subprocess.Popen` para iniciar el servidor.
    Muestra un mensaje de información si el servidor se lanza correctamente.
    Muestra una advertencia si no se puede lanzar el servidor.

    Args:
        var (bool): Indica si se debe lanzar el servidor.

    Returns:
        None
    """        
        the_path =  self.ruta_server
        print("VAR",var)
        if var==True:
            
            self.theproc = subprocess.Popen([sys.executable, the_path])
            showinfo("INFORMACION","SERVIDOR LANZADO")
            ic("SERVIDOR LANZADO")
            self.theproc.communicate()
        else:
            showwarning("ADVERTENCIA","NO SE PUDO LANZAR EL SERVIDOR") 
            print("NO SE PUDO LANZAR EL SERVIDOR")    

    
    def apagar_servidor(self,):
        """
    Apaga el servidor.

    Llama al método `kill` del proceso del servidor para detenerlo.
    Muestra un mensaje de información si el servidor se apaga correctamente.

    Args:
        None

    Returns:
        None
    """
        if self.theproc is not None:
            self.theproc.kill()
            showinfo("INFORMACION","SERVIDOR APAGADO")
            ic("SERVIDOR APAGADO")        

    def try_connection(self, ): 
        """
    Intenta conectar y lanzar el servidor.

    Llama al método `lanzar_servidor` en un hilo separado.
    Si el servidor ya está en ejecución, lo detiene antes de intentar lanzarlo de nuevo.

    Args:
        None

    Returns:
        None
    """
        ic("lanzando servidor")
        if self.theproc is not None:
            self.theproc.kill()            
            threading.Thread(target=self.lanzar_servidor, args=(True,), daemon=True).start()
        else:
            threading.Thread(target=self.lanzar_servidor, args=(True,), daemon=True).start()

