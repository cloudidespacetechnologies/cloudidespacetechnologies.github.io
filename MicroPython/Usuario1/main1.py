
import machine
import time
import _thread
import ota  # Asegúrate de tener este módulo

# Constantes para la versión del firmware y la URL de actualización
FIRMWARE_VERSION = 1.1  # Debe ser un float
UPDATE_URL = "https://cloudidespacetechnologies.github.io/MicroPython/Usuario1/esp32_micropython_1.json"

# Aqui va las Variables para el Controlar los componentes
RELAY_PIN = 16  # Ejemplo, ajusta según tu conexión
# Configurar el pin del relé
relay = machine.Pin(RELAY_PIN, machine.Pin.OUT)



def Devices_control():
    """
    Controla el funcionamiento del dispositivo.
    """
    while True:
        # Lógica para controlar el relé
        relay.value(1)  # Encender relé
        time.sleep(5)   # Mantener encendido durante 5 segundos
        relay.value(0)  # Apagar relé
        time.sleep(5)   # Esperar  segundos antes de encender nuevamente


def main():
    """
    Función principal que inicializa los hilos y procesos necesarios.
    """
    global stop_blinking

     # Configura el pin antiguo del LED a bajo para apagarlo si es necesario
   # Lista de pines del firmware anterior para apagarlos si es necesario
    old_pins = [17]  # Asegúrate de actualizar esta lista según sea necesario
    for pin_number in old_pins:
      old_led = machine.Pin(pin_number, machine.Pin.OUT)
      old_led.value(False)  # Apaga el LED del pin antiguo

    # Iniciar el parpadeo del LED en un nuevo hilo
    _thread.start_new_thread(Devices_control, ())

    while True:
        # Verificar si hay actualizaciones disponibles
        update_available = ota.check_for_update()
        # Espera 60 segundos antes de la próxima verificación
        time.sleep(60)

# Punto de entrada del programa
if __name__ == '__main__':
    main()
