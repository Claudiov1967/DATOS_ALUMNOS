from peewee import *
import re
from datetime import datetime

# variables para el grafico
egb, cfi, superior, integracion = 0, 0, 0, 0
tamaño = [egb, cfi, superior, integracion]

#Boolean si es True hay que actualizar el grafico
graf= False

db = SqliteDatabase("escuela.db")
#db = MySQLDatabase(database="escuela", user="root", password="", host="localhost",port=3306)
#mysql_db = MySQLDatabase('escuela')


      
class BaseModel(Model):
    class Meta:
        database = db

class Alumno(BaseModel):
    nombre = CharField()
    apellido = CharField()
    curso = CharField()
    documento = CharField()
    domicilio = CharField()
    telefono = CharField()
    nacimiento = CharField()

db.connect()
db.create_tables([Alumno])
    


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
            alumno = Alumno()
            alumno.nombre = self.nombre
            alumno.apellido = self.apellido
            alumno.curso = self.curso
            alumno.documento = self.documento
            alumno.domicilio = self.domicilio
            alumno.telefono = self.telefono
            alumno.nacimiento = self.nacimiento
            alumno.save()

            print("Estoy en alta todo ok")
            resultado = self.alumnos_cursos(app)
            print(resultado)
            app.graf =True
            print(app.graf, app.tamaño)
            
            return "ALTA OK", resultado
              
        # si se ingreso por error un caracter no valido con el nombre o apellido
        else:
            return (self.nombre + " " + self.apellido + ": solo debe contener letras"), resultado

    # actualiza el treview al comenzar para llenarlo con los valores de la tabla    
    def alumnos_cursos(self,app):
        resultado=[]
        
        egb, cfi, superior, integracion = 0, 0, 0, 0

        for fila in Alumno.select():
            resultado.append((fila.id, fila.nombre, fila.apellido, fila.curso, fila.documento, fila.domicilio, fila.telefono, fila.nacimiento))
                           
            if fila.curso =="egb":
                egb += 1
            if fila.curso =="cfi":
                cfi += 1
            if fila.curso =="superior":
                superior += 1
            if fila.curso =="integracion":
                integracion += 1
        print("egb: ", egb, "cfi", cfi, "superior", superior, "integracion", integracion)
        app.graf=True
        app.tamaño= [egb, cfi, superior, integracion]
        return resultado
        
    # borra un registro de la base de datos al seleccionarlo
    def borrar(self, tree, app):
        resultado =[]
        valor = tree.selection()
        if not valor:
            app.graf =False
            return "Por favor seleccione una fila para eliminar."
        item = tree.item(valor)
        
        print("item:", item)     
        print(item['text'])
        print("values", item['values'])
        mi_id = item['text']
        borrar = Alumno.get(Alumno.id==mi_id)
        borrar.delete_instance()

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
            mi_id = int(item['text'])
            actualizar = Alumno.update(nombre=self.nombre,apellido=self.apellido,curso=self.curso, documento=self.documento,domicilio=self.domicilio, telefono=self.telefono, nacimiento=self.nacimiento).where(Alumno.id== mi_id)
            actualizar.execute()
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
        app.nombre_val.set(item['values'][0])
        app.apellido_val.set(item['values'][1])
        app.curso_val.set(item['values'][2])
        app.documento_val.set(item['values'][3])
        app.domicilio_val.set(item['values'][4])
        app.tel_val.set(item['values'][5])
        app.nac_val.set(item['values'][6])  
        app.graf=False   
        print("SSSSSSS",item['values'][6])
        edad= self.calcular_edad(item['values'][6])
        print(edad)
        return "SE CONSULTO", edad
    
    def calcular_edad(self,fecha):
        today = datetime.now()
        print(today, "   ", fecha)
        nac = datetime.strptime(fecha, "%d/%m/%y")
        print("-----------------------------")
        edad_y= today.year-nac.year
        edad_m=today.month-nac.month
        edad_d=today.day-nac.day
        if (edad_d<0):
            edad_d+=30
            edad_m-=1
        if (edad_m<0):
            edad_m+=12
            edad_y-=1
        edad= str(edad_y)+ " años,"+str(edad_m)+" meses,"+ str(edad_d)+" dias"
        print("EDAD", fecha," ", edad)
        return edad

