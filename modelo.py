import sqlite3
import re

#SOLO IMPLEMENTA CLASE EN VISTA
"""VISTA_MVC TIENE SEPARACION MVC. NO SE PASA TREE A MODELO, SOLO ITEM 
EL MODELO NO TIENE UNA CLASE ABMC"""

egb, cfi, superior, integracion = 0, 0, 0, 0
tamaño = [egb, cfi, superior, integracion]

graf= False

def conexion():
    con = sqlite3.connect("escuela.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS alumnos2
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre text, apellido text, curso text, documento text, domicilio text, telefono text, f_nac text)
    """
    cursor.execute(sql)
    con.commit()


conexion()
crear_tabla()


# alta de datos en SQL3
def alta(nombre, apellido, curso, documento, domicilio, telefono, nacimiento):
    resultado =[]
    global graf, tamaño    
    # controla que en todos los entries se hayan ingresado datos
    if (nombre.get() =="" or apellido.get() =="" or curso.get() =="" or documento.get() == "" or domicilio.get() == "" or telefono.get() == "" or nacimiento.get() == ""):
        return False, tamaño, "Por favor debe llenar todos los entries.", resultado
    
    # Expresión regular para exactamente 10 dígitos para telefono
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{10})$"
    if re.match(patron_num, telefono.get()):
        pass #("Validado el numero")
    else:
        print("Debe ser un numero de 10 digitos")
        return False, tamaño, "El telefono debe ser un numero de 10 digitos", resultado
    
    # Expresión regular para exactamente 8 dígitos para documento
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{8})$"
    if re.match(patron_num, documento.get()):
        pass #("Validado el numero")
    else:
        print("Debe ser un numero de 8 digitos")
        return False, tamaño, "El documento debe ser un numero de 8 digitos", resultado
    
    # Validar si la cadena coincide con el patrón: letras mayusculas, minusculas, con acento y ñ
    patron = "^[a-zA-ZáéíóúñÑ ]+$"
    if(re.match(patron, nombre.get()) and re.match(patron, apellido.get())):
                                
        print(nombre.get(), apellido.get(), curso.get(), documento.get(), domicilio.get(), telefono.get(), nacimiento.get())
        con=conexion()
        cursor=con.cursor()
        data=(nombre.get(), apellido.get(), curso.get(), documento.get(), domicilio.get(), telefono.get(), nacimiento.get())
        print(type(data), data)
            
        sql="INSERT INTO alumnos2(nombre, apellido, curso,documento, domicilio, telefono, f_nac) VALUES(?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print("Estoy en alta todo ok")
        graf, tamaño, resultado = alumnos_cursos()
        print(graf, tamaño)
        nombre.set("")
        apellido.set("")
        curso.set("")
        documento.set("")
        domicilio.set("")
        telefono.set("")
        nacimiento.set("")

        return True, tamaño,"ALTA OK", resultado
              
    # si se ingreso por error un caracter no valido con el nombre o apellido
    else:
        return False, tamaño, (nombre.get() + " " + apellido.get() + ": solo debe contener letras"), resultado
        

# borra un registro de la base de datos al seleccionarlo

def borrar(item):
    resultado=[]
    global graf, tamaño
    print("item:",item)     
    print(item['text'])
    print("values",item['values'])
    mi_id = item['text']

    con=conexion()
    cursor=con.cursor()
    data = (mi_id,)
    sql = "DELETE FROM alumnos2 WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    
    graf, tamaño, resultado =alumnos_cursos()
    return True, tamaño, "SE DIO DE BAJA AL ALUMNO", resultado

def modificar(nombre, apellido, curso, documento, domicilio, telefono, nacimiento, item):
    resultado = []
    global graf, tamaño  
        
    # controla que en todos los entries se hayan ingresado datos
    if (nombre.get() =="" or apellido.get() =="" or curso.get() =="" or documento.get() =="" or domicilio.get() == "" or telefono.get() == "" or nacimiento.get() == ""):
        mensaje = "Por favor debe llenar todos los entries."
        return False, tamaño, mensaje , resultado
    
    # Expresión regular para exactamente 10 dígitos para telefono
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{10})$"
    if re.match(patron_num, telefono.get()):
        pass #print("Validado")
    else:
        print("Debe ser un numero de 10 digitos")
        mensaje = "El telefono debe ser un numero de 10 digitos"
        return False, tamaño, mensaje, resultado
    
    # Expresión regular para exactamente 8 dígitos para documento
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{8})$"
    if re.match(patron_num, documento.get()):
        pass #print("Validado el numero")
    else:
        print("Debe ser un numero de 8 digitos")
        mensaje = "El documento debe ser un numero de 8 digitos"
        return False, tamaño, mensaje, resultado
    
    # Validar si la cadena coincide con el patrón: letras mayusculas, minusculas, con acento y ñ
    patron = "^[a-zA-ZáéíóúñÑ ]+$"
    if(re.match(patron, nombre.get()) and re.match(patron, apellido.get())):

        print("item:",item)     
        print(item['text'])
        con=conexion()
        cursor = con.cursor()
        mi_id = int(item['text'])
        data = (nombre.get(), apellido.get(), curso.get(), documento.get(), domicilio.get(), telefono.get(), nacimiento.get(), mi_id)
        print(data)
        sql = "UPDATE alumnos2 SET nombre=?, apellido=?, curso=?, documento=?, domicilio=?, telefono=?, f_nac=? WHERE id=?;"
        cursor.execute(sql, data)
        con.commit()

        graf, tamaño, resultado =alumnos_cursos()
        nombre.set("")
        apellido.set("")
        curso.set("")
        documento.set("")
        domicilio.set("")
        telefono.set("")
        nacimiento.set("")
        return graf, tamaño, "Se han modificado los datos", resultado


    # si se ingreso por error un caracter no valido con el nombre o apellido
    else:
        mensaje= nombre.get() + " " + apellido.get() + ": solo debe contener letras"
        return False, tamaño, mensaje, resultado

def consultar(nombre, apellido, curso, documento, domicilio, telefono, nacimiento, item):
    
    print("item:",item)     
    print(item['text'])
    con=conexion()
    nombre.set(item['values'][0])
    apellido.set(item['values'][1])
    curso.set(item['values'][2])
    documento.set(item['values'][3])
    domicilio.set(item['values'][4])
    telefono.set(item['values'][5])
    nacimiento.set(item['values'][6])
    return "SE CONSULTO"
    
   
# actualiza el treview al comenzar para llenarlo con los valores de la tabla
def alumnos_cursos():
    
    egb, cfi, superior, integracion = 0, 0, 0, 0

    sql = "SELECT * FROM alumnos2 ORDER BY id ASC"
    con=conexion()
    cursor=con.cursor()
    datos=cursor.execute(sql)
    resultado = datos.fetchall()
       
    for fila in resultado:
        print(fila)
        if (fila[3])=="egb":
            egb += 1
        if (fila[3])=="cfi":
            cfi += 1
        if (fila[3])=="superior":
            superior += 1
        if (fila[3])=="integracion":
            integracion += 1
        print("egb: ", egb, "cfi", cfi, "superior", superior, "integracion", integracion)

    return True, [egb, cfi, superior, integracion], resultado
