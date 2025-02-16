class Subject:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        pass

    def notificar(self,*args):
        print("argumentos:",*args)
        for observador in self.observadores:
            observador.update(*args)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        self.observador_a = obj
        self.observador_a.agregar(self)

    def update(self, *args):
        print("Actualización dentro de ObservadorConcretoA")
        print("Aqui estan los parametros: ", args)
        

class ConcreteObserverB(Observador):
    def __init__(self, obj):
        self.observador_b = obj
        self.observador_b.agregar(self)

    def update(self):
        print("Actualización dentro de ObservadorConcretoB")
        self.estado = self.observador_b.get_estado()
        print("Estado = ", self.estado)

