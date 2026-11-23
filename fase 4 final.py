# =====================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# CURSO: PROGRAMACIÓN (213023)
# FASE 4 - PRÁCTICAS SIMULADAS
# ESTUDIANTE: DIEGO ALBERTO PARRA ARIAS
# GRUPO: 213023_518
# TUTOR: JORGE EDUARDO OSPINA
# =====================================================
from abc import ABC, abstractmethod
import logging
# =====================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =====================================================
import os
import logging

RUTA_LOG = os.path.join(
    os.path.dirname(__file__),
    "logs_sistema.txt"
)

logging.basicConfig(
    filename=RUTA_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================
class ClienteInvalidoError(Exception):
    """Error relacionado con datos inválidos del cliente"""
    pass
class ServicioInvalidoError(Exception):
    """Error relacionado con servicios"""
    pass
class ReservaInvalidaError(Exception):
    """Error relacionado con reservas"""
    pass
class ArchivoLogError(Exception):
    """Error relacionado con el archivo de logs"""
    pass
# =====================================================
# CLASE ABSTRACTA ENTIDAD
# =====================================================
class Entidad(ABC):
    def __init__(self, id_entidad, nombre):
        self.id_entidad = id_entidad
        self.nombre = nombre
    @abstractmethod
    def mostrar_informacion(self):
        pass
# =====================================================
# CLASE CLIENTE
# =====================================================
class Cliente(Entidad):
    def __init__(self, id_entidad, nombre, identificacion, correo):
        super().__init__(id_entidad, nombre)
        self.__identificacion = None
        self.__correo = None
        self.identificacion = identificacion
        self.correo = correo
    @property
    def identificacion(self):
        return self.__identificacion
    @identificacion.setter
    def identificacion(self, valor):
        if not str(valor).isdigit():
            raise ClienteInvalidoError(
                "La identificación debe contener números."
            )
        self.__identificacion = valor
    @property
    def correo(self):
        return self.__correo
    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(
                "Correo electrónico inválido."
            )
        self.__correo = valor
    def mostrar_informacion(self):
        return (
            f"Cliente: {self.nombre} "
            f"- ID: {self.identificacion}"
        )
# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================
class Servicio(ABC):
    def __init__(self, nombre_servicio, costo_base):
        if costo_base <= 0:
            raise ServicioInvalidoError(
                "El costo debe ser positivo."
            )
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
    @abstractmethod
    def calcular_costo(self,
                        descuento=0,
                        impuesto=0):
        pass
    @abstractmethod
    def describir_servicio(self):
        pass
    @abstractmethod
    def validar_parametros(self):
        pass
# =====================================================
# RESERVA DE SALA
# =====================================================
class ReservaSala(Servicio):
    def __init__(self, horas, costo_hora):
        super().__init__("Reserva de Sala", costo_hora)
        self.horas = horas
        self.validar_parametros()
    def validar_parametros(self):
        if self.horas <= 0:
            raise ServicioInvalidoError(
                "Las horas deben ser mayores a cero."
            )
    def calcular_costo(self,
                        descuento=0,
                        impuesto=0):
        subtotal = self.horas * self.costo_base
        subtotal -= subtotal * descuento / 100
        subtotal += subtotal * impuesto / 100
        return subtotal
    def describir_servicio(self):
        return f"Sala reservada durante {self.horas} horas"
# =====================================================
# ALQUILER DE EQUIPOS
# =====================================================
class AlquilerEquipos(Servicio):
    def __init__(self,
                 equipo,
                 dias,
                 costo_dia):
        super().__init__("Alquiler de Equipos",
                         costo_dia)
        self.equipo = equipo
        self.dias = dias
        self.validar_parametros()
    def validar_parametros(self):
        if self.dias <= 0:
            raise ServicioInvalidoError(
                "Los días deben ser mayores a cero."
            )
    def calcular_costo(
            self,
            descuento=0,
            impuesto=0):
        subtotal = self.dias * self.costo_base
        subtotal -= subtotal * descuento / 100
        subtotal += subtotal * impuesto / 100
        return subtotal
    def describir_servicio(self):
        return f"{self.equipo} alquilado por {self.dias} días"
# =====================================================
# ASESORÍA ESPECIALIZADA
# =====================================================
class AsesoriaEspecializada(Servicio):
    def __init__(self,
                 especialidad,
                 sesiones,
                 costo_sesion):
        super().__init__("Asesoría Especializada",
                         costo_sesion)
        self.especialidad = especialidad
        self.sesiones = sesiones
        self.validar_parametros()
    def validar_parametros(self):
        if self.sesiones <= 0:
            raise ServicioInvalidoError(
                "Debe existir al menos una sesión."
            )
    def calcular_costo(
            self,
            descuento=0,
            impuesto=0):
        subtotal = self.sesiones * self.costo_base
        subtotal -= subtotal * descuento / 100
        subtotal += subtotal * impuesto / 100
        return subtotal
    def describir_servicio(self):
        return (
            f"Asesoría en "
            f"{self.especialidad}"
        )
# =====================================================
# CLASE RESERVA
# =====================================================
class Reserva:

    def __init__(
        self,
        cliente,
        servicio,
        duracion):

        if duracion <= 0:
            raise ReservaInvalidaError(
                "La duración debe ser positiva."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):

        self.estado = "Confirmada"

        logging.info(
            f"Reserva confirmada: {self.cliente.nombre}"
        )

    def cancelar(self):

        self.estado = "Cancelada"

        logging.warning(
            f"Reserva cancelada: {self.cliente.nombre}"
        )

    def procesar(
        self,
        descuento=0,
        impuesto=0):

        try:

            if self.estado == "Cancelada":

                raise ReservaInvalidaError(
                    "No se puede procesar una reserva cancelada."
                )

            costo = self.servicio.calcular_costo(
                descuento,
                impuesto
            )

        except Exception as e:

            logging.error(
                f"Error procesando reserva: {e}"
            )

            raise ReservaInvalidaError(
                "Error procesando reserva"
            ) from e

        else:

            self.estado = "Procesada"

            logging.info(
                f"Reserva procesada con éxito. "
                f"Costo: {costo}"
            )

            return costo

        finally:

            logging.info(
                "Finalizó intento de procesamiento."
            )
# =====================================================
# FUNCIONES DE APOYO
# =====================================================
def registrar_evento(mensaje):
    try:
        logging.info(mensaje)
    except Exception as e:
        raise ArchivoLogError(
            "Error registrando evento."
        ) from e
# =====================================================
# SIMULACIONES
# =====================================================
print("\nSIMULACIONES DEL SISTEMA\n")
# -----------------------------------------------------
# SIMULACIÓN 1
# Cliente válido
# -----------------------------------------------------
try:
    cliente1 = Cliente(
        1,
        "Diego Parra",
        "12345678",
        "diego@gmail.com"
    )
    print(cliente1.mostrar_informacion())
except Exception as e:
    print(e)
# -----------------------------------------------------
# SIMULACIÓN 2
# Correo inválido
# -----------------------------------------------------

try:

    cliente2 = Cliente(
        2,
        "Juan",
        "11111",
        "correo_invalido"
    )

except Exception as e:

    logging.error(
        f"Simulación 2: {e}"
    )

    print("Error:", e)
# -----------------------------------------------------
# SIMULACIÓN 3
# Identificación inválida
# -----------------------------------------------------

try:

    cliente3 = Cliente(
        3,
        "Pedro",
        "ABC123",
        "correo@gmail.com"
    )

except Exception as e:

    logging.error(
        f"Simulación 3: {e}"
    )

    print("Error:", e)
# -----------------------------------------------------
# SIMULACIÓN 4
# Servicio válido
# -----------------------------------------------------
try:
    servicio1 = ReservaSala(
        4,
        50000
    )
    print(servicio1.describir_servicio())
except Exception as e:
    print(e)
# -----------------------------------------------------
# SIMULACIÓN 5
# Servicio inválido
# -----------------------------------------------------

try:

    servicio2 = ReservaSala(
        2,
        -5000
    )

except Exception as e:

    logging.error(
        f"Simulación 5: {e}"
    )

    print("Error:", e)
# -----------------------------------------------------
# SIMULACIÓN 6
# Reserva exitosa
# -----------------------------------------------------
try:
    reserva1 = Reserva(
        cliente1,
        servicio1,
        4
    )
    reserva1.confirmar()
    costo = reserva1.procesar()
    print("Costo:", costo)
except Exception as e:
    print(e)
# -----------------------------------------------------
# SIMULACIÓN 7
# Reserva inválida
# -----------------------------------------------------

try:

    reserva2 = Reserva(
        cliente1,
        servicio1,
        -2
    )

except Exception as e:

    logging.error(
        f"Simulación 7: {e}"
    )

    print("Error:", e)
# -----------------------------------------------------
# SIMULACIÓN 8
# Cancelación
# -----------------------------------------------------
try:
    reserva3 = Reserva(
        cliente1,
        servicio1,
        2
    )
    reserva3.cancelar()
    print("Estado:", reserva3.estado)
except Exception as e:
    print(e)
# -----------------------------------------------------
# SIMULACIÓN 9
# POLIMORFISMO
# -----------------------------------------------------

try:

    servicios = [

        ReservaSala(
            2,
            30000
        ),

        AlquilerEquipos(
            "Portátil",
            3,
            40000
        ),

        AsesoriaEspecializada(
            "Python",
            5,
            60000
        )
    ]

    print(
        "\nSIMULACIÓN DE POLIMORFISMO"
    )

    for servicio in servicios:

        print(
            f"\nTipo: "
            f"{type(servicio).__name__}"
        )

        print(
            servicio.describir_servicio()
        )

        print(
            "Costo:",
            servicio.calcular_costo(
                descuento=10,
                impuesto=19
            )
        )

except Exception as e:

    logging.error(
        f"Simulación 9: {e}"
    )

    print(e)
# -----------------------------------------------------
# SIMULACIÓN 9.1
# SOBRECARGA DE MÉTODOS
# -----------------------------------------------------
try:

    print(
        "\nPRUEBA DE SOBRECARGA"
    )

    print(
        "Costo normal:",
        servicio1.calcular_costo()
    )

    print(
        "Costo con descuento:",
        servicio1.calcular_costo(
            descuento=10
        )
    )

    print(
        "Costo con descuento e impuesto:",
        servicio1.calcular_costo(
            descuento=10,
            impuesto=19
        )
    )

except Exception as e:

    logging.error(
        f"Simulación 9.1: {e}"
    )

    print(e)
# -----------------------------------------------------
# SIMULACIÓN 10
# Encadenamiento
# -----------------------------------------------------

try:

    try:

        servicio_error = ReservaSala(
            -5,
            10000
        )

    except Exception as error_original:

        raise ReservaInvalidaError(
            "Error generado mediante encadenamiento"
        ) from error_original

except Exception as e:

    logging.critical(
        f"Simulación 10: {e}"
    )

    print(
        "Error detectado:",
        e
    )
