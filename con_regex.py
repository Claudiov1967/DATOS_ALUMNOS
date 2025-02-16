import re


def validar_datos(nombre, apellido, curso, documento, domicilio, telefono, nacimiento, mail,edad): 
   
    resultado =[]      
    values= ('egb','cfi','superior','integracion','ex')       
    ###############################  REGEX   ###################################
    # controla que en todos los entries se hayan ingresado datos
    if (nombre.get() == "" or apellido.get() == " " or curso.get() == "" or documento.get() == "" or domicilio.get() == "" or telefono.get() == "" or nacimiento.get() == "" or mail.get()==""):
        #app.graf =False
        return "Por favor debe llenar todos los entries.", [nombre.get(),apellido.get(),curso.get(),documento.get()]
    
    # Expresión regular para exactamente 10 dígitos para telefono
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{10})$"
    if not re.match(patron_num, telefono.get()):                
        print("Debe ser un numero de 10 digitos")
        #app.graf =False
        return "El telefono debe ser un numero de 10 digitos", [nombre.get(),apellido.get(),curso.get(),documento.get()]
    
    # Expresión regular para exactamente 8 dígitos para documento
    # Validar si la cadena coincide con el patrón
    patron_num = "^([0-9]{8})$"
    if not re.match(patron_num, documento.get()):                
        print("Debe ser un numero de 8 digitos")
        #app.graf = False
        return "El documento debe ser un numero de 8 digitos", [nombre.get(),apellido.get(),curso.get(),documento.get()]
    
    #validar el email
    patron_mail = re.compile(r"^[A-Za-z0-9._-]+@[A-Za-z0-9]+\.[A-Za-z]{2,3}(\.[a-zA-Z]{0,2})?$")
    if not re.match(patron_mail, mail.get()):                
        print("Debe ser un email valido")
        #app.graf = False
        return "Debe ser un email valido: (usuario@dominio.com)", [nombre.get(),apellido.get(),curso.get(),documento.get()]
    
    # Validar el nombre y el apellido: se permiten letras mayusculas, minusculas, con acento y ñ
    patron = "^[a-zA-ZáéíóúñÑ ]+$"
    if not (re.match(patron, nombre.get()) and re.match(patron, apellido.get())):
        return "El nombre y el apellido solo debe contener letras: ", [nombre.get(),apellido.get(),curso.get(),documento.get()]
    if curso.get() not in values:
        return "CURSO: Elija egb, cfi, superior, integracion o ex ", [nombre.get(),apellido.get(),curso.get(),documento.get()]
        print("Not in values")
    if edad <5:
        return "La edad debe ser mayor que 5 años",  [nombre.get(),apellido.get(),curso.get(),documento.get()]
    else:
        return None
    
 

