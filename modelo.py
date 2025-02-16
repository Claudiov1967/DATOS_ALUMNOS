import sqlite3
import re

# variables para el grafico
egb, cfi, superior, integracion = 0, 0, 0, 0
tamaño = [egb, cfi, superior, integracion]

#Boolean si es True hay que actualizar el grafico
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

class Abmc():
    def __init__(self, nombre, apellido, curso, documento, domicilio, telefono, nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.curso = curso
        self.documento = documento
        self.domicilio = domicilio
        self.telefono = telefono
        self.nacimiento = nacimiento

    # alta de datos en SQL3
    def alta(self,app):
        resultado =[]
        # controla que en todos los entries se hayan ingresado datos
        if (self.nombre == "" or self.apellido == " " or self.curso == "" or self.documento == "" or self.domicilio == "" or self.telefono == "" or self.nacimiento == ""):
            app.graf =False
            return "Por favor debe llenar todos los entries.", resultado
        
        # Expresión regular para exactamente 10 dígitos para telefono
        # Validar si la cadena coincide con el patrón
        patron_num = "^([0-9]{10})$"
        if re.match(patron_num, self.telefono):
            pass #("Validado el numero")
        else:
            print("Debe ser un numero de 10 digitos")
            app.graf =False
            return "El telefono debe ser un numero de 10 digitos", resultado
        
        # Expresión regular para exactamente 8 dígitos para documento
        # Validar si la cadena coincide con el patrón
        patron_num = "^([0-9]{8})$"
        if re.match(patron_num, self.documento):
            pass  #("Validado el numero")
        else:
            print("Debe ser un numero de 8 digitos")
            app.graf = False
            return "El documento debe ser un numero de 8 digitos", resultado
    
        # Validar si la cadena coincide con el patrón: letras mayusculas, minusculas, con acento y ñ
        patron = "^[a-zA-ZáéíóúñÑ ]+$"
        if (re.match(patron, self.nombre) and re.match(patron, self.apellido)):
                                    
            print(self.nombre, self.apellido, self.curso, self.documento, self.domicilio, self.telefono, self.nacimiento)
            con =conexion()
            cursor =con.cursor()
            data =(self.nombre, self.apellido, self.curso, self.documento, self.domicilio, self.telefono, self.nacimiento)
            print(type(data), data)
                
            sql ="INSERT INTO alumnos2(nombre, apellido, curso,documento, domicilio, telefono, f_nac) VALUES(?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            print("Estoy en alta todo ok")
            resultado = self.alumnos_cursos(app)
            print(type(resultado), resultado)
            app.graf =True
            print(app.graf, app.tamaño)
            return "ALTA OK", resultado
              
        # si se ingreso por error un caracter no valido con el nombre o apellido
        else:
            return (self.nombre + " " + self.apellido + ": solo debe contener letras"), resultado
        

    # borra un registro de la base de datos al seleccionarlo
    def borrar(self, tree, app):
        resultado =[]
        valor = tree.selection()
        if not valor:
            app.graf =False
            return "Por favor seleccione una fila para eliminar."
        print("valor:", valor)   
        item = tree.item(valor)
        
        print("item:", item)     
        print(item['text'])
        print("values", item['values'])
        mi_id = item['text']

        con = conexion()
        cursor = con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM alumnos2 WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        app.graf = True

        resultado = self.alumnos_cursos(app)
        return "SE DIO DE BAJA AL ALUMNO", resultado

    def modificar(self, item, app):
        resultado = []
                    
        # controla que en todos los entries se hayan ingresado datos
        if (self.nombre == "" or 
            self.apellido == "" or 
            self.curso == "" or 
            self.documento == "" or 
            self.domicilio == "" or 
            self.telefono == "" or 
            self.nacimiento == ""):

    # Código a ejecutar si alguna de las condiciones es verdadera

            mensaje = "Por favor debe llenar todos los entries."
            app.graf = False
            return mensaje, resultado
        
        # Expresión regular para exactamente 10 dígitos para telefono
        # Validar si la cadena coincide con el patrón
        patron_num = "^([0-9]{10})$"
        if re.match(patron_num, self.telefono):
            pass  #print("Validado")
        else:
            print("Debe ser un numero de 10 digitos")
            mensaje = "El telefono debe ser un numero de 10 digitos"
            app.graf = False
            return mensaje, resultado
    
        # Expresión regular para exactamente 8 dígitos para documento
        # Validar si la cadena coincide con el patrón
        patron_num = "^([0-9]{8})$"
        if re.match(patron_num, self.documento):
            pass  #print("Validado el numero")
        else:
            print("Debe ser un numero de 8 digitos")
            mensaje = "El documento debe ser un numero de 8 digitos"
            app.graf = False
            return mensaje, resultado
        
        # Validar si la cadena coincide con el patrón: letras mayusculas, minusculas, con acento y ñ
        patron = "^[a-zA-ZáéíóúñÑ ]+$"
        if (re.match(patron, self.nombre) and re.match(patron, self.apellido)):

            print("item:", item)     
            print(item['text'])
            con = conexion()
            cursor = con.cursor()
            mi_id = int(item['text'])
            data = (self.nombre,
                    self.apellido,
                    self.curso,
                    self.documento,
                    self.domicilio,
                    self.telefono,
                    self.nacimiento,
                    mi_id)
            print(data)
            sql = "UPDATE alumnos2 SET nombre=?, apellido=?, curso=?, documento=?, domicilio=?, telefono=?, f_nac=? WHERE id=?;"
            cursor.execute(sql, data)
            con.commit()
            resultado = self.alumnos_cursos(app)
            app.graf = True
            return "Se han modificado los datos", resultado


        # si se ingreso por error un caracter no valido con el nombre o apellido
        else:
            mensaje = self.nombre + " " + self.apellido + ": solo debe contener letras"
            app.graf = False
            return mensaje, resultado

    def consultar(self, item, app):
        
        print("item:",item)     
        print(item['text'])
        con = conexion()
        app.nombre_val.set(item['values'][0])
        app.apellido_val.set(item['values'][1])
        app.curso_val.set(item['values'][2])
        app.documento_val.set(item['values'][3])
        app.domicilio_val.set(item['values'][4])
        app.tel_val.set(item['values'][5])
        app.nac_val.set(item['values'][6])  
        app.graf=False    
        return "SE CONSULTO"
    
   
    # actualiza el treview al comenzar para llenarlo con los valores de la tabla
    def alumnos_cursos(self,app):
        
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
        app.graf=True
        app.tamaño= [egb, cfi, superior, integracion]

        return resultado
