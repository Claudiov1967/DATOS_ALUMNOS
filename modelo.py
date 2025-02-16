"""
Modelo de la Aplicacion
Contiene la logica 
Interactua con la base de datos
"""
from peewee import *
import re
from datetime import datetime
import os
import sys 
from con_regex import validar_datos
from observador import Subject


"""
variables para el grafico
:egb: integer candidad de alumnos en el ciclo egb
:cfi: integer candidad de alumnos en el ciclo cfi
:superior: integer candidad de alumnos en el ciclo superior
:integracion: integer candidad de alumnos en el ciclo integracion
: graf: boolean True hay que actualizar el grafico
variables ruta archivo log
:BASE_DIR (str): Directorio base del archivo. 
:ruta (str): Ruta completa del archivo log.
"""
egb, cfi, superior, integracion = 0, 0, 0, 0
tamano = [egb, cfi, superior, integracion]
graf= False
BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ruta = os.path.join(BASE_DIR, "log.txt")

db = SqliteDatabase("escuela.db")
# Para conectar a una base de datos MySqL hasy que cambiar los comentarios
#db = MySQLDatabase(database="escuela", user="root", password="", host="localhost",port=3306)
#mysql_db = MySQLDatabase('escuela')


def ingreso(funcion):
    """ 
    Decorador que registra la información sobre el ingreso de datos 
    en un archivo log. 
    Args: 
        funcion (function): La función a decorar. 
    Returns: 
        function: La función decorada. 
    """
    def envoltura(*args, **kwargs):
        result = funcion(*args, **kwargs)
        cadena= result[0][:25]
        with open(ruta, "a") as log:
            
            if cadena =='Se ha ingresado el alumno':
                print(result[0], datetime.now(), file=log)
            elif result[0] == 'El DNI ya se encuentra  EN LA DB':
                print("Se intento ingresar un alumno con DNI ya existente en la base")
            else:
                print("Error: ",result[0],"Se intento ingresar el alumno: ",result[1][0]," ",result[1][1]," con DNI: ",result[1][3]," ", datetime.now(), file=log)
        return result
    return envoltura

def eliminacion(funcion):
    """ 
    Decorador que registra la información sobre la eliminación de datos
    en un archivo log. 
    Args: 
        funcion (function): La función a decorar. 
    Returns: 
        function: La función decorada. 
    """
    def envoltura(*args, **kwargs):
        result = funcion(*args, **kwargs)
        with open(ruta, "a") as log:
            print(result[0], datetime.now(), file=log)
        return result
    return envoltura

def actualizacion(funcion):
    """ 
    Decorador que registra la información sobre la actualización 
    de datos en un archivo log. 
    
    Args: 
        funcion (function): La función a decorar. 
    Returns: 
        function: La función decorada. 
    """
    def envoltura(*args, **kwargs):
        result = funcion(*args, **kwargs)
        cadena=result[0][:27]
        with open(ruta, "a") as log:
            if cadena =="Se han modificado los datos":
                print(result[0], datetime.now(), file=log)
            else:
                print("Error:  ",result[0],"Se intento modificar el alumno: ",result[1][0]," ",result[1][1]," con DNI: ",result[1][3], datetime.now(), file=log)
        return result
    return envoltura


class RegistroLog(Exception):
    """ 
    Clase para manejar excepciones de registro de logs. 
    Esta clase extiende la clase `Exception` para manejar los errores 
    relacionados con el registro de logs en el sistema.
 
    """

    def __init__(self, nombre, apellido, documento, fecha):
        """
        Constructor de la clase RegistroLog.
        Inicializa la clase RegistroLog con la información del alumno y la fecha.
        
        Args:
            nombre (str): Nombre del alumno. 
            apellido (str): Apellido del alumno. 
            documento (str): DNI del alumno. 
            fecha (str): Fecha y hora en que se registra el error.
        """
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.fecha = fecha

    def registrar_error(self):
        """
        Registra un error en el archivo log.

        Escribe un mensaje en el archivo log con la información del alumno 
        y la fecha del error.

        Returns:
            None
        """
        
        with open(ruta, "a") as log:
            print(f"Se ha intentado ingresar el documento que ya estaba en la base de datos {self.documento} correspondiente al alumno {self.nombre}  {self.apellido} el {self.fecha}", file=log)
 
    def ingresar_documento(self, documentos):
        """
        Verifica y registra el documento del alumno.

        Este método verifica si el documento del alumno ya está en la lista
        de documentos. Si el documento ya existe, lanza una excepción 
        `RegistroLogError` con la información del alumno y la fecha actual.
        
        Args:
            self: La instancia de la clase que llama al método. 
            documentos (list): Lista de documentos existentes.

        Raises:
            RegistroLogError: Si el documento del alumno ya existe en la lista.
        
        Returns:
            None: No retorna nada.        
        """
        
        if self.documento in documentos:
            raise RegistroLog( self.nombre,self.apellido,self.documento,datetime.now()) 
        else:
            return

   
class BaseModel(Model):

    """
    Clase BaseModel
    
    Clase base para definir los modelos de la base de datos
    Todas las demás clases de modelos deben heredar de esta clase
    
    Attributes:
         Meta: Metaclase que define la base de datos a utilizar 
    """
    
    class Meta:
        database = db

class Alumno2(BaseModel):
    """
    Clase que representa a un alumno.

    Esta clase define los atributos de un alumno que serian registrados 
    en la base de datos

    Attributes:
        nombre (Charfield): Nombre del alumno
        apellido (Charfield): apellido del alumno
        curso (Charfield): curso que concurre el alumno
        documento (Charfield): DNI del alumno
        domicilio (Charfield): domicilio del alumno
        telefono (Charfield): teléfono del alumno
        nacimiento (Charfield): fecha de nacimiento del alumno
        mail (Charfield): correo electrónico del alumno    
    """
    nombre = CharField()
    apellido = CharField()
    curso = CharField()
    documento = CharField()
    domicilio = CharField()
    telefono = CharField()
    nacimiento = CharField()
    mail = CharField()

db.connect()
"""
Conecta con la Base de datos

Esta funcion establece una conexion con la base de datos especificada.

Args:
    None
Returns:
    None: No retorna nada.
"""
db.create_tables([Alumno2])
"""
Crea una tabla en la base de datos.

Esta funcion crea la tabla correspondiente al modelo Alumno2 en la base de datos.

Args:
    Alumno2 (BaseModel): La clase del modelo que se utilizara para crear la tabla
        
Returns:
    None: No retorna nada.
"""


# La clase Abmc es la que la encargada de administrar la comunicacion con la base de datos
class Abmc(Subject):
          
        """
        Class para la gestion de alumnos en la base de datos

        Methods:
            alta(nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail, app): 
                Añade un nuevo alumno a la base de datos. 
            alumnos_cursos(app): 
                Recupera la lista de alumnos y sus documentos. 
            borrar(tree, app): 
                Elimina un alumno de la base de datos. 
            modificar(item, nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail, app):
              Modifica los datos de un alumno en la base de datos. 
            consultar(treeview, app): 
                Consulta los datos de un alumno específico. 
            calcular_edad(fecha): 
                Calcula la edad de una persona dada su fecha de nacimiento

        """
        
        @ingreso
        def alta(self, nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail,app):
                        
            """
            Da de alta un nuevo registro en la base de datos

            Se hace un regex para validar cada uno de los campos ingresados.
            Si alguno no valida, se retorna la información con el inconveniente 
            para ser desplegado en pantalla.

            Args:
                nombre (str): Nombre del alumno. 
                apellido (str): Apellido del alumno. 
                curso (str): Curso al que concurre el individuo. 
                documento (str): DNI del alumno. 
                domicilio (str): Dirección del alumno. 
                telefono (str): Teléfono del alumno. 
                nacimiento (str): Fecha de nacimiento del alumno. 
                mail (str): Email del alumno. 
                app (object): Instancia de la clase Ventanita.
            
            Returns:
                tuple: Un tuple que contiene un string y una lista:
                    - retorno (string): tiene la informacion para ser mostrada en pantalla en VISTA 
                    - resultado (list): Una lista con todos los datos en la DB para actualizar el treeview.                                             
            """
            resultado =[]  
            edad=self.calcular_edad(nacimiento.get())
            print(edad)
            print(edad[0], " años") 
            validacion = validar_datos(nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail, edad[0])
                       
            if validacion is not None: 
                app.graf=False
                print("VALIDACION",validacion) 
                return validacion 
            else:
                            
                ##################################### EXCEPTION ##############################################
                # busca todos los DNI en la base de datos y se fija si el ingresado esta en la base, informando un error
                # Resultado es una lista que contiene todos los datos de la base de datos, para pasar a vista
            
                resultado, documentos = self.alumnos_cursos(app)
                # La funcion ingresar_documento, en caso de que el documento ya este en la base de datos
                # dentro de la lista documentos, produce un RAISE y la cadena except lo registra en log
                try:
                    print("Intentando ingresar un documento...")
                    evento =RegistroLog(nombre.get(), apellido.get(), documento.get(), datetime.now())
                    evento.ingresar_documento(documentos)
                except RegistroLog as log:
                    print("Se ha producido un error al ingresar el documento.")
                    log.registrar_error()  
                    return "El DNI ya se encuentra  EN LA DB", resultado

                    
                # Alta en la base de datos. Crea una instancia, alumno2 que es guardada
                
                alumno = Alumno2()
                alumno.nombre = nombre.get()
                alumno.apellido = apellido.get()
                alumno.curso = curso.get()
                alumno.documento = documento.get()
                alumno.domicilio = domicilio.get()
                alumno.telefono = telefono.get()
                alumno.nacimiento = nacimiento.get()
                alumno.mail = mail.get()
                alumno.save()
                resultado, documentos = self.alumnos_cursos(app)
                app.graf =True
                self.notificar(nombre.get(), apellido.get(), documento.get())
                    
                return "Se ha ingresado el alumno: "+nombre.get()+" "+apellido.get()+",DNI "+documento.get(), resultado
                            
        
        def alumnos_cursos(self,app):
            """
            Crea dos listas
            Una con todos los datos de los alumnos de la base de datos para actualizar el treeview
            Otra lista de documentos (DNI) de los alumnos en la base de datos
            Calcula la cantidad de alumnos en cada curso y actualiza la lista tamaño

            Args:        
                app (object): la instancia de la clase Ventanita

            Returns:
                tuple: Un tuple que contiene un string y una lista:
                    - resultado (list): Una lista con todos los datos en la DB para actualizar el treeview.
                    - documentos (list): Una lista con todos los documentos (DNI) en la base de datos.                               
            """
            resultado=[]
            documentos=[]
            
            egb, cfi, superior, integracion = 0, 0, 0, 0

            for fila in Alumno2.select():
                resultado.append((fila.id, fila.nombre, fila.apellido, fila.curso, fila.documento, fila.domicilio, fila.telefono, fila.nacimiento, fila.mail))
                            
                documentos.append(fila.documento)
                if fila.curso =="egb":
                    egb += 1
                if fila.curso =="cfi":
                    cfi += 1
                if fila.curso =="superior":
                    superior += 1
                if fila.curso =="integracion":
                    integracion += 1
                print(type(fila),fila.apellido.lower())
            app.graf=True
            app.tamano= [egb, cfi, superior, integracion]
            return resultado, documentos
            

        @eliminacion
        def borrar(self, tree, app):
            """
            Elimina un alumno de la base de datos

            Recoge el registro seleccionado en el treeview y elimina la instancia 
            correspondiente en la base de datos. 
            Luego actualiza la lista de alumnos y los datos gráficos en la interfaz.

            Args:
                tree (object): El treeview de tkinter de los alumnos
                app (object): Instancia de la clase Ventanita

            Returns: 
                tuple: Un tuple que contiene un strings y una lista:
                    - retorno (string): tiene la informacion para ser mostrada en pantalla en VISTA 
                    - resultado (list): Una lista con todos los datos en la DB para actualizar el treeview.   
            """
            resultado =[]
            valor = tree.selection()
            if not valor:
                app.graf =False
                return "Por favor seleccione una fila para eliminar.",resultado
            item = tree.item(valor)
            mi_id = item['text']
            borrar = Alumno2.get(Alumno2.id==mi_id)
            borrar.delete_instance()

            app.graf = True
            
            resultado, documentos = self.alumnos_cursos(app)
            alumno=item['values'][0]+" "+item['values'][1]+" con DNI: "+str(item['values'][3])
                    
            return "SE DIO DE BAJA AL ALUMNO "+alumno, resultado
    
        
        @actualizacion
        def modificar(self, item, nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail, app):
            """
            Modifica un registro en la base de datos

            Recoge los datos del registro seleccionado en el treeview y actualiza los campos correspondientes 
            en la base de datos. Luego actualiza la lista de alumnos y los datos
            gráficos en la interfaz.

            Args:
                item (dict): Lista con los valores de una fila de un registro del treeview. 
                nombre (str): Entry widget para el nombre del alumno. 
                apellido (str): Entry widget para el apellido del alumno. 
                curso (str): Entry widget para el curso del alumno. 
                documento (str): Entry widget para el documento del alumno. 
                domicilio (str): Entry widget para el domicilio del alumno. 
                telefono (str): Entry widget para el teléfono del alumno. 
                nacimiento (str): Entry widget para la fecha de nacimiento del alumno. 
                mail (str): Entry widget para el email del alumno. 
                app (object): Instancia de la clase Ventanita.

            Returns: 
                tuple: Un tuple que contiene un string y una lista:
                    - retorno (string): tiene la informacion para ser mostrada en pantalla en VISTA 
                    - resultado (list): Una lista con todos los datos en la DB para actualizar el treeview.                
            """
            resultado =[]   
            edad=self.calcular_edad(nacimiento.get())
            print(edad)
            print(edad[0], " años")
            validacion = validar_datos(nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail, edad[0])
            #print("VALIDACION",validacion)
            
            
            if validacion is not None: 
                app.graf=False
                print("VALIDACION",validacion) 
                return validacion 
            

            # Modifica la base de datos
            mi_id = int(item['text'])
            actualizar = Alumno2.update(nombre=nombre.get(), apellido=apellido.get(), curso=curso.get(), documento=documento.get(),domicilio=domicilio.get(), telefono=telefono.get(), nacimiento=nacimiento.get(), mail=mail.get()).where(Alumno2.id== mi_id)
            actualizar.execute()
            resultado, documentos = self.alumnos_cursos(app)
            app.graf = True
                        
            return "Se han modificado los datos de: "+nombre.get()+" "+apellido.get()+",DNI "+documento.get(), resultado

       
        
        def consultar(self, treeview, app):
            """
            Consulta un registro en la base de datos y despliega los datos en los Entries

            Args:
                treeview (object): El treeview de tkinter de los alumnos
                app (object): Instancia de la clase Ventanita

            Returns:
                tuple: Un tuple que contiene dos strings:
                    - retorno (string): tiene la informacion para ser mostrada en pantalla en VISTA 
                    - edad (string): la edad del alumno en dias, meses y años                  
            """
            valor = treeview.selection()
            if not valor:
                app.graf=False
                return "Por favor selecciones una fila para consultar.", ""
             
            item= treeview.item(valor) 
             
            app.nombre_val.set(item['values'][0])
            app.apellido_val.set(item['values'][1])
            app.curso_val.set(item['values'][2])
            app.documento_val.set(item['values'][3])
            app.domicilio_val.set(item['values'][4])
            app.tel_val.set(item['values'][5])
            app.nac_val.set(item['values'][6])  
            app.mail_val.set(item['values'][7]) 
            app.graf=False   
            edad= self.calcular_edad(item['values'][6])
            print(edad)
            return "SE CONSULTO", edad
        
        def calcular_edad(self,fecha):
            
            """
            Calcula la edad del alumno

            Args:
                fecha (str): fecha de nacimiento del alumno en formato 'dd/mm/yy'
                
            Returns: 
                - edad (str): la edad del alumno en dias, meses y años                             
            """
            today = datetime.now()
            print(today, "   ", fecha)
            nac = datetime.strptime(fecha, "%d/%m/%y")
            edad_y= today.year-nac.year
            edad_m=today.month-nac.month
            edad_d=today.day-nac.day
            if (edad_d<0):
                edad_d+=30
                edad_m-=1
            if (edad_m<0):
                edad_m+=12
                edad_y-=1
            #edad= f"{edad_y} años, {edad_m} meses, {edad_d} días"
            edad= (edad_y, edad_m, edad_d)
            print("EDAD", fecha," ", edad)
            return edad

