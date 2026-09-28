# -*- coding: utf-8 -*-
"""
Sistema para Control de Lavado (AutoLavado)
-------------------------------------------
Programa en consola que controla los autos que ingresan a un autolavado y
calcula el costo del servicio según el tiempo que permanecen en el proceso.

Conceptos de POO aplicados:
  - Clase con constructor (__init__)
  - Encapsulamiento: atributos privados (_placa, _hora_ingreso, _tarifa_hora)
  - Métodos de instancia y validaciones
"""

from datetime import datetime  # Para interpretar y comparar horas (formato HH:MM)

FORMATO_HORA = "%H:%M"  # Formato esperado, por ejemplo 08:30 o 14:05


class AutoLavado:
    """Representa un auto dentro del proceso de lavado."""

    def __init__(self, placa, tarifa_hora):
        """Constructor: crea el auto con su placa y la tarifa por hora.

        Los atributos inician con guion bajo (_) para indicar que son privados
        y solo deben modificarse mediante los métodos de la clase.
        """
        self._placa = placa.strip().upper()   # Placa normalizada en mayúsculas
        self._hora_ingreso = None             # Se asigna en registrar_ingreso()
        self._hora_salida = None              # Se asigna en registrar_salida()
        self._tarifa_hora = float(tarifa_hora)  # Valor cobrado por cada hora

    # ------------------------------------------------------------------
    # Método auxiliar de validación (uso interno de la clase)
    # ------------------------------------------------------------------
    @staticmethod
    def _convertir_hora(hora):
        """Convierte un texto 'HH:MM' en objeto datetime.

        Lanza ValueError si el formato no es válido (por ejemplo '25:70' o 'abc').
        """
        return datetime.strptime(hora.strip(), FORMATO_HORA)

    # ------------------------------------------------------------------
    # Métodos solicitados en el enunciado
    # ------------------------------------------------------------------
    def registrar_ingreso(self, hora):
        """Registra la hora de ingreso del auto (valida el formato)."""
        self._hora_ingreso = self._convertir_hora(hora)

    def registrar_salida(self, hora):
        """Registra la hora de salida del auto.

        Validaciones:
          - El auto debe tener una hora de ingreso previa.
          - La hora de salida debe ser posterior a la de ingreso.
        """
        if self._hora_ingreso is None:
            raise ValueError("El auto no tiene hora de ingreso registrada.")
        salida = self._convertir_hora(hora)
        if salida <= self._hora_ingreso:
            raise ValueError("La hora de salida debe ser posterior a la de ingreso.")
        self._hora_salida = salida

    def calcular_pago(self, hora_salida):
        """Calcula el costo del servicio según el tiempo transcurrido.

        Se cobra proporcionalmente por minuto: horas_totales * tarifa_hora.
        Reutiliza registrar_salida() para validar la hora ingresada.
        """
        self.registrar_salida(hora_salida)
        minutos = (self._hora_salida - self._hora_ingreso).total_seconds() / 60
        return (minutos / 60) * self._tarifa_hora

    def obtener_placa(self):
        """Devuelve la placa del auto (acceso controlado al atributo privado)."""
        return self._placa

    # Método extra de apoyo para mostrar información en el menú
    def obtener_hora_ingreso(self):
        """Devuelve la hora de ingreso en formato HH:MM."""
        return self._hora_ingreso.strftime(FORMATO_HORA)


# ----------------------------------------------------------------------
# Lógica del sistema (menú e interacción con el usuario)
# ----------------------------------------------------------------------
TARIFA_POR_HORA = 8000  # Tarifa en pesos colombianos (COP) por hora de lavado


def registrar_auto(autos):
    """Solicita placa y hora de ingreso, y agrega el auto a la lista interna."""
    placa = input("Placa del auto: ").strip()
    if not placa:
        print("  ✗ La placa no puede estar vacía.")
        return
    # Evita registrar dos veces un auto que aún está en el lavado
    if any(a.obtener_placa() == placa.upper() for a in autos):
        print("  ✗ Ese auto ya se encuentra en el lavado.")
        return
    auto = AutoLavado(placa, TARIFA_POR_HORA)
    try:
        auto.registrar_ingreso(input("Hora de ingreso (HH:MM): "))
    except ValueError:
        print("  ✗ Hora inválida. Use el formato HH:MM (ej. 08:30).")
        return
    autos.append(auto)
    print(f"  ✓ Auto {auto.obtener_placa()} registrado a las {auto.obtener_hora_ingreso()}.")


def listar_autos(autos):
    """Muestra los autos que están actualmente en el lavado."""
    if not autos:
        print("  No hay autos en el lavado.")
        return
    for i, auto in enumerate(autos, start=1):
        print(f"  {i}. {auto.obtener_placa()} - ingreso: {auto.obtener_hora_ingreso()}")


def registrar_salida_auto(autos):
    """Permite seleccionar un auto, valida la salida y calcula el pago."""
    if not autos:
        print("  No hay autos para registrar salida.")
        return
    listar_autos(autos)
    try:
        indice = int(input("Seleccione el número del auto: ")) - 1
        auto = autos[indice] if indice >= 0 else None
    except (ValueError, IndexError):
        auto = None
    if auto is None:
        print("  ✗ Selección inválida.")
        return
    try:
        pago = auto.calcular_pago(input("Hora de salida (HH:MM): "))
    except ValueError as error:
        print(f"  ✗ {error}")
        return
    print(f"  ✓ Auto {auto.obtener_placa()} - Total a pagar: ${pago:,.0f} COP")
    autos.remove(auto)  # El auto sale del lavado y se elimina de la lista


def main():
    """Ciclo principal del programa."""
    autos = []  # Lista interna de autos en proceso de lavado
    while True:
        print("\n=== AUTOLAVADO ===")
        print("1. Registrar ingreso")
        print("2. Registrar salida y calcular pago")
        print("3. Ver autos en el lavado")
        print("4. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            registrar_auto(autos)
        elif opcion == "2":
            registrar_salida_auto(autos)
        elif opcion == "3":
            listar_autos(autos)
        elif opcion == "4":
            print("Hasta luego.")
            break
        else:
            print("  ✗ Opción no válida.")


if __name__ == "__main__":
    main() 
