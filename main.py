
import machine
import time
import _thread
import ota  # Asegúrate de tener este módulo

# Constantes para la versión del firmware y la URL de actualización
FIRMWARE_VERSION = 1.0  # Debe ser un float
UPDATE_URL = "https://cloudidespacetechnologies.github.io/firmware_microPython.json"

# Aqui va las Variables para el Controlar los componentes
# Pines para los componentes
IR_SENSOR_PIN = 15  # Ejemplo, ajusta según tu conexión
RELAY_PIN = 4       # Ejemplo, ajusta según tu conexión
LED_PIN = 2         # Ejemplo, ajusta según tu conexión

# Configurar los pines
ir_sensor = machine.Pin(IR_SENSOR_PIN, machine.Pin.IN)
relay = machine.Pin(RELAY_PIN, machine.Pin.OUT)
led = machine.Pin(LED_PIN, machine.Pin.OUT)



def Devices_control():
    """
    Controla el funcionamiento del dispositivo.
    """
    while True:
        # Lógica para el sensor infrarrojo
        ir_value = ir_sensor.value()

        # Lógica para controlar el relé y el LED
        if ir_value == 1:  # Objeto detectado
            relay.value(1)  # Encender relé
            led.value(1)    # Encender LED
        else:
            relay.value(0)  # Apagar relé
            led.value(0)    # Apagar LED

        time.sleep(0.1)  # Ajusta según tus necesidades


def main():
    """
    Función principal que inicializa los hilos y procesos necesarios.
    """
    global stop_blinking

     # Configura el pin antiguo del LED a bajo para apagarlo si es necesario
   # Lista de pines del firmware anterior para apagarlos si es necesario
    old_pins = [18]  # Asegúrate de actualizar esta lista según sea necesario
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
