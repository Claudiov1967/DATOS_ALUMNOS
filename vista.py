from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter as tk
from tkcalendar import *
import random
import re
from tkinter import ttk, messagebox
from tkinter import Tk, Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ##############################################
# MODELO
# ##############################################

# conexion con base de datos y creamos la tabla si no fue creada

# variables para hacer el grafico de barras con maptolib
global egb, cfi, superior, integracion 
egb, cfi, superior, integracion = 0, 0, 0, 0

def conexion():
    con = sqlite3.connect("escuela.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS alumnos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre text, apellido text, curso text, domicilio text, telefono text, f_nac text)
    """
    cursor.execute(sql)
    con.commit()

# funcion que inserta una ventana solicitando la conformidad para ALT, BAJA Y MODIFICACION
def conformidad(accion):
    if askyesno('CONFORMIDAD',
    accion):
        showinfo('Si', 'SE REALIZA LA ACCION')
        return "si"
    else:
        showinfo('No', 'ESTA A PUNTO DE SALIR')
        return "no"

# funcion para limpiar los entries y la barra inferior 
def limpiar():
            
            nombre_val.set("")
            apellido_val.set("")
            curso_val.set("")
            domicilio_val.set("")
            tel_val.set("")
            nac_val.set("")
            Label(ventana, text="                                                                                               " , font=("Agency FB", 19)).place(x=40,y=50)

conexion()
crear_tabla()

# 
def actualizar_grafico():
    # Limpiar el gráfico actual
    ax.clear()
    
    tamaño = [egb, cfi, superior, integracion]
    ax.bar(nombres, tamaño, color=colores)
    
    # Redibujar el gráfico
    canvas.draw()

# alta de datos en SQL3
def alta(nombre, apellido, curso, domicilio, telefono ,nacimiento, tree):

    # controla que en todos los entries se hayan ingresado datos
    if (nombre=="" or apellido=="" or curso=="" or domicilio=="" or nacimiento==""):
        messagebox.showwarning("Advertencia", "Por favor debe llenar todos los entries.")
        return
    
    # Expresión regular para exactamente 10 dígitos para telefono
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{10})$"
    if re.match(patron_num, telefono):
        print("Validado")
    else:
        print("Debe ser un numero de 10 digitos")
        Label(ventana, text="El telefono debe ser un numero de 10 digitos" , font=("Agency FB", 19)).place(x=40,y=50)
        return
    
    # Validar si la cadena coincide con el patrón: letras mayusculas, minusculas, con acento y ñ
    patron = "^[a-zA-ZáéíóúñÑ ]+$"
    if(re.match(patron, nombre) and re.match(patron, apellido)):
        Label(ventana, text="Nombre válido: "+nombre+ " "+apellido , font=("Agency FB", 19)).place(x=40,y=50)
                
        if conformidad("DESEA DAR DE ALTA UN REGISTRO?")=="no":
            limpiar()
            return # si no desea dar de alta limpia los entries y vuelve
        else:    
            # carga un nuevo registro
            telefono= int(telefono)
            print(type(telefono), "telefono")        

            print(nombre, apellido, curso, domicilio, telefono, nacimiento)
            con=conexion()
            cursor=con.cursor()
            data=(nombre, apellido, curso, domicilio, telefono, nacimiento)
            print(type(data), data)
                
            sql="INSERT INTO alumnos(nombre, apellido, curso, domicilio, telefono, f_nac) VALUES(?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            print("Estoy en alta todo ok")
            actualizar_treeview(tree)

            # Limpiar los campos de entrada
            limpiar()       
    
    # si se ingreso por error un caracter no valido con el nombre o apellido
    else:
        Label(ventana, text= nombre+ " "+apellido+ ": solo debe contener letras", font=("Agency FB", 19)).place(x=40,y=50)
        

# borra un registro de la base de datos al seleccionarlo

def borrar(tree):
    valor = tree.selection()
    if not valor:
        messagebox.showwarning("Advertencia", "Por favor seleccione una fila para eliminar.")
        return
    if conformidad("Desea dar de baja?")=="no":
        limpiar()
        return
    else:
        print("valor:",valor)   
        item = tree.item(valor)
        print("item:",item)     
        print(item['text'])
        print("values",item['values'])
        mi_id = item['text']

        con=conexion()
        cursor=con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM alumnos WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)

def modificar(nombre, apellido, curso, domicilio, telefono, nacimiento, tree):
    valor = tree.selection()
    # si no se selecciona un registro para modificar informa error
    if not valor:
        messagebox.showwarning("Advertencia", "Por favor seleccione una fila para modificar.")
        return
    
    # Expresión regular para exactamente 10 dígitos para telefono
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{10})$"
    if re.match(patron_num, telefono):
        print("Validado")
    else:
        print("Debe ser un numero de 10 digitos")
        Label(ventana, text="El telefono debe ser un numero de 10 digitos" , font=("Agency FB", 19)).place(x=40,y=50)
        return
    # controla que en todos los entries se hayan ingresado datos
    if (nombre=="" or apellido=="" or curso=="" or domicilio=="" or nacimiento==""):
        messagebox.showwarning("Advertencia", "Por favor debe llenar todos los entries.")
        return
    if conformidad("DESEA MODIFICAR EL REGISTRO?")=="no":
        limpiar()
        return
    else:
        telefono=int(telefono)
        print(type(telefono), "telefono") 
        print("valor:",valor)   
        item = tree.item(valor)
        print("item:",item)     
        print(item['text'])
        con=conexion()
        cursor = con.cursor()
        mi_id = int(item['text'])
        data = (nombre, apellido, curso, domicilio, telefono, nacimiento, mi_id)
        print(data)
        sql = "UPDATE alumnos SET nombre=?, apellido=?, curso=?, domicilio=?, telefono=?, f_nac=? WHERE id=?;"
        cursor.execute(sql, data)
        con.commit()

        # Limpiar los campos de entrada
        limpiar()
        actualizar_treeview(tree)
    

def consultar(tree):
    valor = tree.selection()
    if not valor:
        messagebox.showwarning("Advertencia", "Por favor seleccione una fila para consultar.")
        return
    print("valor:",valor)   
    item = tree.item(valor)
    print("item:",item)     
    print(item['text'])
    con=conexion()
    cursor = con.cursor()
    mi_id = int(item['text'])
    entrada1.delete(0, 'end')
    entrada1.insert(0, item['values'][0])
    entrada2.delete(0, 'end')
    entrada2.insert(0, item['values'][1])
    entrada3.delete(0, 'end')
    entrada3.insert(0, item['values'][2])
    entrada4.delete(0, 'end')
    entrada4.insert(0, item['values'][3])
    entrada5.delete(0, 'end')
    entrada5.insert(0, item['values'][4])
    entrada6.delete(0, 'end')
    entrada6.insert(0, item['values'][5])
    Label(ventana, text="                                                        ", font=("Agency FB", 19)).place(x=40,y=50)
   
def cambiar_colores():
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
    root.configure(background=color)   
    

# actualiza el treview al comenzar para llenarlo con los valores de la tabla
def actualizar_treeview(mitreview):
    global egb, cfi, superior, integracion 
    egb, cfi, superior, integracion = 0, 0, 0, 0

    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM alumnos ORDER BY id ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
       

    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))
        if (fila[3])=="egb":
            egb += 1
        if (fila[3])=="cfi":
            cfi += 1
        if (fila[3])=="superior":
            superior += 1
        if (fila[3])=="integracion":
            integracion += 1
        print("egb: ", egb, "cfi", cfi, "superior", superior, "integracion", integracion)
    # Actualizar el gráfico después de actualizar el TreeView
    actualizar_grafico()

# esta funcion borra dd/mm/yy del entry
# y coloca la fecha elegida
# ademans la imprime en consola

def elegir_fecha():
    entrada6.delete(0, END)
    print("El dia elegido es: " + calendario.get_date())
    nac_val= calendario.get_date()
    entrada6.insert(0, calendario.get_date())

# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("SISTEMA DE GESTION DE DATOS")

# color fondo de la grilla de la ventana root
root.configure(bg="#2F4F4F", padx=20, pady=20)

# calendario y ventana
# de calendario se necesita calendario.get_date() en la otra funcion

# Titulo principal de ña ventana         
titulo = Label(root, text="SISTEMA DE GESTION DE DATOS E INGRESOS DE ALUMNOS", bg="green", fg="thistle1", height=1, width=60,font=("Garamond",14,"bold"))
titulo.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky=W+E)

###################


# crear un frame dentro de la ventana
frame = Frame(root, bg='green')
frame.grid(column=4, row=1, rowspan=5)

# Datos para el grafico
nombres = ['EGB', 'CFI', 'SUP', 'INTEG']
colores = ['blue', 'red', 'green', 'yellow']
tamaño = [egb, cfi, superior, integracion]

# Crear la figura y los ejes
fig, ax = plt.subplots(dpi=80, figsize=(4, 2), facecolor="green")

# Titulo de la figura
fig.suptitle('ALUMNOS POR CURSO')

# Crear un grafico de barras en el primer eje
ax.bar(nombres, tamaño, color= colores)

# Integrar la figura en tkinter
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().grid(column=4, row=1, rowspan=5, columnspan=2)


# widgets con los nombres de los campos a conpletar por cada registro
nombre = Label(root, text="Nombre/s", font=("Candara",12), width=15)
nombre.grid(row=1, column=0, sticky=W)
apellido=Label(root, text="Apellido/s", font=("Candara",12),width=15)
apellido.grid(row=2, column=0, sticky=W)
curso=Label(root, text="Curso      ", font=("Candara",12),width=15)
curso.grid(row=3, column=0, sticky=W)
domicilio=Label(root, text="Domicilio", font=("Candara",12), width=15)
domicilio.grid(row=4, column=0, sticky=W)
telefono=Label(root, text="Telefono", font=("Candara",12), width=15)
telefono.grid(row=5, column=0, sticky=W)
nacimiento= Label(root, text="F. Nac.", font=("Candara",12), width=15)
nacimiento.grid(row=6, column=0, sticky=W)


# Variables campos de Entrada
nombre_val, apellido_val, curso_val, domicilio_val, tel_val, nac_val = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
w_ancho = 20

entrada1 = Entry(root, textvariable = nombre_val, width = w_ancho,font=("Candara",12)) 
entrada1.grid(row = 1, column = 1)
entrada2 = Entry(root, textvariable = apellido_val, width = w_ancho, font=("Candara",12)) 
entrada2.grid(row = 2, column = 1)
#entrada3 = Entry(root, textvariable = curso_val, width = w_ancho, font=("Candara",12)) 
#entrada3.grid(row = 3, column = 1)
entrada3 = ttk.Combobox(root, textvariable = curso_val, width = w_ancho, font=("Candara",12)) 
entrada3.grid(row = 3, column = 1)
entrada3['values'] = ('egb',  
                          'cfi', 
                          'superior', 
                          'integracion', 
                          ) 
entrada4 = Entry(root, textvariable = domicilio_val, width = w_ancho, font=("Candara",12)) 
entrada4.grid(row = 4, column = 1)
entrada5 = Entry(root, textvariable = tel_val, width = w_ancho, font=("Candara",12)) 
entrada5.grid(row = 5, column = 1)
tel_val.set("")
entrada6 = Entry(root, textvariable = nac_val, width = w_ancho, font=("Candara",12)) 
entrada6.grid(row = 6, column = 1)
nac_val.set("")

################################################
# calendario
calendario = Calendar(root, selectmode="day", background="green",selectbackground="black", normalbackground="#00ff40",
                         weekendbackground="#00ff40", othermonthbackground="#008040", othermonthwebackground="#008040", )
calendario.grid(row=1, column=2, rowspan=6)
################################################
###############################################
# IMAGEN:logo (DEBE ESTAR EN LA MISMA CARPETA)
##############################################
image1 = Image.open("logo.png")
image1 = image1.resize((100, 100))
image1 = ImageTk.PhotoImage(image1)
label1 = tk.Label(image=image1)
label1.grid(row=1, column=5, rowspan=4)

##################################################
# TREEVIEW
##################################################

tree = ttk.Treeview(root)
# STYLE TREEVIEW
style = ttk.Style()
style.theme_use("alt")

tree["columns"]=("col1", "col2", "col3", "col4", "col5", "col6")
tree.column("#0", width=90, minwidth=50)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.column("col5", width=200, minwidth=80)
tree.column("col6", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="NOMBRE")
tree.heading("col2", text="APELLIDO")
tree.heading("col3", text="CURSO")
tree.heading("col4", text="DOMICILIO")
tree.heading("col5", text="TELEFONO")
tree.heading("col6", text="F. NACIMIENTO")
tree.grid(row=12, column=0, columnspan=6)

ventana = Frame(root, bg="#FF7F50", height= 122, borderwidth=2, relief=RAISED)
ventana.grid(row=13, column=0, columnspan=6, padx=1, pady=1, sticky=W+E)

actualizar_treeview(tree)
##################################
# BOTONES DE CONTROL
##################################

boton_alta=Button(root, text="Alta", command=lambda:alta(nombre_val.get(), apellido_val.get(), curso_val.get(),domicilio_val.get(), tel_val.get(),nac_val.get(), tree), font=("Candara",12), width=15)
boton_alta.grid(row=9, column=0)

boton_borrar=Button(root, text="Borrar", command=lambda:borrar(tree), font=("Candara",12), width=15)
boton_borrar.grid(row=10, column=0)

boton_modificar=Button(root, text="Modificar", command=lambda:modificar(nombre_val.get(), apellido_val.get(), curso_val.get(),domicilio_val.get(), tel_val.get(),nac_val.get(), tree), font=("Candara",12), width=15)
boton_modificar.grid(row=10, column=1)

boton_consultar=Button(root, text="Consultar", command=lambda:consultar(tree), font=("Candara",12), width=15)
boton_consultar.grid(row=9, column=1)

boton_fecha = Button(root, text="ACEPTAR", command=elegir_fecha, bg="black", fg="white", font=("Candara",12), width=15)
boton_fecha.grid(row=9, column=2)

boton_sorpresa = Button(root, text="SORPRESA", command=cambiar_colores, bg="white", fg="black", font=("Candara",12), width=15)
boton_sorpresa.grid(row=8, column=5)

root.mainloop()
