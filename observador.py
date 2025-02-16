import os
from datetime import datetime

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ruta = os.path.join(BASE_DIR, "log.txt")


class Subject:
    """
    Clase Subject que mantiene una lista de observadores y notifica cambios.

    Attributes:
        observadores (list): Lista de observadores registrados.

    Methods:
        agregar(obj): Agrega un observador a la lista.
        quitar(obj): Elimina un observador de la lista.
        notificar(*args): Notifica a todos los observadores registrados.
    """

    observadores = []

    def agregar(self, obj):
        """
        Agrega un observador a la lista.

        Args:
            obj (Observador): El observador a agregar.

        Returns:
            None
        """
        self.observadores.append(obj)

    def quitar(self, obj):
        """
        Elimina un observador de la lista.

        Args:
            obj (Observador): El observador a eliminar.

        Returns:
            None
        """
        pass

    def notificar(self,*args):  
        """
        Notifica a todos los observadores registrados.

        Args:
            *args: Argumentos a pasar a los observadores.

        Returns:
            None
        """      
        
        for observador in self.observadores:
            observador.update(*args)


class Observador:
    """
    Clase abstracta Observador que define el método update.

    Methods:
        update(): Método abstracto que debe ser implementado por las subclases.
    """
    def update(self):
        """
        Método abstracto que debe ser implementado por las subclases.

        Raises:
            NotImplementedError: Si la subclase no implementa este método.
        """
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observador):
    """
    Clase ConcreteObserverA que implementa el método update.

    Args:
        obj (Subject): El sujeto al que se suscribe el observador.

    Attributes:
        observador_a (Subject): El sujeto al que se suscribe el observador.

    Methods:
        update(*args): Actualiza el observador con los argumentos proporcionados.
    """
    def __init__(self, obj):
        """
        Constructor de la clase ConcreteObserverA.

        Args:
            obj (Subject): El sujeto al que se suscribe el observador.

        Returns:
            None
        """
        self.observador_a = obj
        self.observador_a.agregar(self)
        print("OBJETO",type(obj), obj)

    def update(self, *args):
        """
        Actualiza el observador con los argumentos proporcionados.

        Args:
            *args: Argumentos a pasar al observador.

        Returns:
            None
        """
        with open(ruta, "a") as log:
             print("Actualización dentro de ObservadorConcretoA","Aqui estan los parametros: ", args, datetime.now(), file=log)   
        