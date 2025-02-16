"""
Modelo de la Aplicacion
Contiene la logica 
Interactua con la base de datos
"""
from peewee import *
import re
from datetime import datetime
import os

"""
variables para el grafico
:egb: integer candidad de alumnos en el ciclo egb
:cfi: integer candidad de alumnos en el ciclo cfi
:superior: integer candidad de alumnos en el ciclo superior
:integracion: integer candidad de alumnos en el ciclo integracion
: graf: boolean True hay que actualizar el grafico
"""
egb, cfi, superior, integracion = 0, 0, 0, 0
tamano = [egb, cfi, superior, integracion]
graf= False

db = SqliteDatabase("escuela.db")
# Para conectar a una base de datos MySqL hasy que cambiar los comentarios
#db = MySQLDatabase(database="escuela", user="root", password="", host="localhost",port=3306)
#mysql_db = MySQLDatabase('escuela')

# esta clase es para registrar errores en un archivo log
# en el mismo se guardan los datos del alumno y fecha
class RegistroLog(Exception):
    """ 
    Clase RegistroLog 
    Registra eventos diversos en un archivo log.

    Attributes: 
        BASE_DIR (str): Directorio base del archivo. 
        ruta (str): Ruta completa del archivo log. 
    """

    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "log.txt")

    def __init__(self, nombre, apellido, documento, fecha):
        """
        Constructor de la clase RegistroLog.
        
        Args:
            nombre (str): Nombre del alumno. 
            apellido (str): Apellido del alumno. 
            documento (str): DNI del alumno. 
            fecha (datetime): Fecha y hora en que se registra el error.
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
                
        with open(self.ruta, "a") as log:
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
class Abmc():
        
            
        """
        Class Abmc.

        Esta clase administra la comunicacion con la base de datos

        Attributes:
            nombre (str): Nombre del alumno.
            apellido (str): Apellido del alumno.
            curso (str): Curso al que concurre el individuo.
            documento (str): DNI del alumno.
            domicilio (str): Direccion del alumno.
            telefono (str): Telefono del alumno.
            nacimiento (str): Fecha de nacimiento del alumno.
            mail (str): email del alumno.

        """
        #def __init__(self,): pass

         
        def alta(self, nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail,app):
                        
            """
            Da de alta un nuevo registro en la base de datos

            Se hace un regex para validar cada uno de los campos ingresados.
            Si alguno no valida, se retorna la información con el inconveniente 
            para ser desplegado en pantalla.

            Args:
                nombre (Entry): Nombre del alumno. 
                apellido (Entry): Apellido del alumno. 
                curso (Entry): Curso al que concurre el individuo. 
                documento (Entry): DNI del alumno. 
                domicilio (Entry): Dirección del alumno. 
                telefono (Entry): Teléfono del alumno. 
                nacimiento (Entry): Fecha de nacimiento del alumno. 
                mail (Entry): Email del alumno. 
                app: Instancia de la clase Ventanita.
            
            Returns:
                tuple: Un tuple que contiene un string y una lista:
                    - retorno (string): tiene la informacion para ser mostrada en pantalla en VISTA 
                    - resultado (list): Una lista con todos los datos en la DB para actualizar el treeview.                                             
            """
            resultado =[]
            ###############################  REGEX   ###################################
            # controla que en todos los entries se hayan ingresado datos
            if (nombre.get() == "" or apellido.get() == " " or curso.get() == "" or documento.get() == "" or domicilio.get() == "" or telefono.get() == "" or nacimiento.get() == "" or mail.get()==""):
                app.graf =False
                return "Por favor debe llenar todos los entries.", resultado
            
            # Expresión regular para exactamente 10 dígitos para telefono
            # Validar si la cadena coincide con el patrón
            patron_num = "^([0-9]{10})$"
            if re.match(patron_num, telefono.get()):
                pass #("Validado el numero")
            else:
                print("Debe ser un numero de 10 digitos")
                app.graf =False
                return "El telefono debe ser un numero de 10 digitos", resultado
            
            # Expresión regular para exactamente 8 dígitos para documento
            # Validar si la cadena coincide con el patrón
            patron_num = "^([0-9]{8})$"
            if re.match(patron_num, documento.get()):
                pass  #("Validado el numero")
            else:
                print("Debe ser un numero de 8 digitos")
                app.graf = False
                return "El documento debe ser un numero de 8 digitos", resultado
            
            #validar el email
            patron_mail = re.compile(r"^[A-Za-z0-9._-]+@[A-Za-z0-9]+\.[A-Za-z]{2,3}(\.[a-zA-Z]{0,2})?$")
            if re.match(patron_mail, mail.get()):
                pass  #("Validado el mail")
            else:
                print("Debe ser un email valido")
                app.graf = False
                return "El documento debe ser un mail valido", resultado
        
            # Validar el nombre y el apellido: se permiten letras mayusculas, minusculas, con acento y ñ
            patron = "^[a-zA-ZáéíóúñÑ ]+$"
            if (re.match(patron, nombre.get()) and re.match(patron, apellido.get())):
                
                
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
                
                #print(self.nombre, self.apellido, self.curso, self.documento, self.domicilio, self.telefono, self.nacimiento, self.mail)
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
                print("Estoy en alta todo ok")
                resultado, documentos = self.alumnos_cursos(app)
                print(" documentos###########################",documentos)
                app.graf =True
                print(app.graf, app.tamano)
                
                return "ALTA OK", resultado
                
                # si se ingreso por error un caracter no valido con el nombre o apellido
            else:
                app.graf=False
                return (nombre.get() + " " + apellido.get() + ": solo debe contener letras"), resultado

        # actualiza el treview al comenzar para llenarlo con los valores de la tabla    
        # También cuenta el número de alumnos en pada curso para realizar el gráfico

        def alumnos_cursos(self,app):
            """
            Crea dos listas
            Una con todos los datos de la base de datos
            Otra lista de documentos (DNI) de los alumnos en la base de datos

            Args:        
                app: la instancia de la clase Ventanita

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
            print("egb: ", egb, "cfi", cfi, "superior", superior, "integracion", integracion)
            app.graf=True
            app.tamano= [egb, cfi, superior, integracion]
            return resultado, documentos
            
        # borra un registro de la base de datos al seleccionarlo
        # luego retorna la informacion para ser desplegada en pantalla 
        # y la lista para actualizar el treeview
        def borrar(self, tree, app):
            """
            Borra un registro de la base de datos

            Args:
                tree: El treeview de tkinter
                app: Instancia de la clase Ventanita

            Returns: 
                tuple: Un tuple que contiene un strings y una lista:
                    - retorno (string): tiene la informacion para ser mostrada en pantalla en VISTA 
                    - resultado (list): Una lista con todos los datos en la DB para actualizar el treeview.   
            """
            resultado =[]
            valor = tree.selection()
            if not valor:
                app.graf =False
                return "Por favor seleccione una fila para eliminar."
            item = tree.item(valor)
            mi_id = item['text']
            borrar = Alumno2.get(Alumno2.id==mi_id)
            borrar.delete_instance()

            app.graf = True

            resultado, documentos = self.alumnos_cursos(app)
            return "SE DIO DE BAJA AL ALUMNO", resultado
    
        # Modificar un registro en la base de datos
        # se hace un regex para validar cada uno de los campor ingresados
        # Si alguno no valida se retorna la informacion con el inconveniente
        # para ser desplegado en pantalla
        
        def modificar(self, item, nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail, app):
            """
            Modifica un registro en la base de datos

            Args:
                self (Abmc): La instancia de la clase Abmc. 
                item (dict): Lista con los valores de una fila de un registro del treeview. 
                nombre (Entry): Entry widget para el nombre del alumno. 
                apellido (Entry): Entry widget para el apellido del alumno. 
                curso (Entry): Entry widget para el curso del alumno. 
                documento (Entry): Entry widget para el documento del alumno. 
                domicilio (Entry): Entry widget para el domicilio del alumno. 
                telefono (Entry): Entry widget para el teléfono del alumno. 
                nacimiento (Entry): Entry widget para la fecha de nacimiento del alumno. 
                mail (Entry): Entry widget para el email del alumno. 
                app: Instancia de la clase Ventanita.

            Returns: 
                tuple: Un tuple que contiene un string y una lista:
                    - retorno (string): tiene la informacion para ser mostrada en pantalla en VISTA 
                    - resultado (list): Una lista con todos los datos en la DB para actualizar el treeview.                
            """
            resultado = []
            
            # controla que en todos los entries se hayan ingresado datos
            if (nombre.get() == "" or 
                apellido.get() == "" or 
                curso.get() == "" or 
                documento.get() == "" or 
                domicilio.get() == "" or 
                telefono.get() == "" or 
                nacimiento.get() == "" or mail.get() ==""):

                mensaje = "Por favor debe llenar todos los entries."
                app.graf = False
                return mensaje, resultado
            
            # Expresión regular para exactamente 10 dígitos para telefono
            # Validar si la cadena coincide con el patrón
            patron_num = "^([0-9]{10})$"
            if re.match(patron_num, telefono.get()):
                pass  #print("Validado")
            else:
                print("Debe ser un numero de 10 digitos")
                mensaje = "El telefono debe ser un numero de 10 digitos"
                app.graf = False
                return mensaje, resultado
        
            # Expresión regular para exactamente 8 dígitos para documento
            # Validar si la cadena coincide con el patrón
            patron_num = "^([0-9]{8})$"
            if re.match(patron_num, documento.get()):
                pass  #print("Validado el numero")
            else:
                print("Debe ser un numero de 8 digitos")
                mensaje = "El documento debe ser un numero de 8 digitos"
                app.graf = False
                return mensaje, resultado
            
            #validar el email
            patron_mail = re.compile("^[A-Za-z0-9\\.\\-_]+@[A-Za-z0-9]+\\.{1}[A-Za-z]{2,3}(\\.{0,1}[a-zA-Z]{0,2})?$")
            if re.match(patron_mail, mail.get()):
                pass  #("Validado el mail")
            else:
                print("Debe ser un email valido")
                app.graf = False
                return "El documento debe ser un mail valido", resultado
            
            # Validar el nombrte y apellido: letras mayusculas, minusculas, con acento y ñ
            patron = "^[a-zA-ZáéíóúñÑ ]+$"
            if (re.match(patron, nombre.get()) and re.match(patron, apellido.get())):

                # Modifica la base de datos
                mi_id = int(item['text'])
                actualizar = Alumno2.update(nombre=nombre.get(), apellido=apellido.get(), curso=curso.get(), documento=documento.get(),domicilio=domicilio.get(), telefono=telefono.get(), nacimiento=nacimiento.get(), mail=mail.get()).where(Alumno2.id== mi_id)
                actualizar.execute()
                resultado, documentos = self.alumnos_cursos(app)
                app.graf = True
                return "Se han modificado los datos", resultado


            # si se ingreso por error un caracter no valido con el nombre o apellido
            else:
                mensaje = nombre.get() + " " + apellido.get() + ": solo debe contener letras"
                app.graf = False
                return mensaje, resultado
            
        
        def consultar(self, treeview, app):
            """
            Consulta un registro en la base de datos y despliega los datos en los Entries

            Args:
                self (Abmc): la instancia de la clase Ambc.
                treeview (Treeview): El treeview de tkinter
                app: Instancia de la clase Ventanita

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
                self (Abmc): la instancia de la clase Ambc.
                fecha (str): fecha de nacimiento del alumno en formato 'dd/mm/yy'
                
            Returns: 
                - edad (string): la edad del alumno en dias, meses y años                             
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
            edad= f"{edad_y} años, {edad_m} meses, {edad_d} días"
            print("EDAD", fecha," ", edad)
            return edad

