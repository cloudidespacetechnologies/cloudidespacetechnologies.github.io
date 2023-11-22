import machine
import time
import _thread
import ota  # Asegúrate de tener este módulo

# Constantes para la versión del firmware y la URL de actualización
FIRMWARE_VERSION = 1.0  # Debe ser un float
UPDATE_URL = "https://nachobeta07.github.io/firmware_microPython.json"

# Variables para el LED
current_led_pin = 17  # GPIO para el LED actual
led = machine.Pin(current_led_pin, machine.Pin.OUT)

# Control para el bucle de parpadeo del LED
stop_blinking = False

def led_blinking_control():
    """
    Controla el parpadeo del LED. Si 'stop_blinking' es True, detiene el parpadeo.
    """
    global stop_blinking
    led.value(True)  # Enciende el LED inicialmente
    while not stop_blinking:
        led.value(not led.value())  # Cambia el estado del LED
        time.sleep(0.5)  # Parpadeo cada 0.5 segundos
    led.value(False)  # Asegura que el LED se apague al detener el parpadeo


def main():
    """
    Función principal que inicializa los hilos y procesos necesarios.
    """
    global stop_blinking
    global current_led_pin

     # Configura el pin antiguo del LED a bajo para apagarlo si es necesario
   # Lista de pines del firmware anterior para apagarlos si es necesario
    old_pins = [18]  # Asegúrate de actualizar esta lista según sea necesario
    for pin_number in old_pins:
        if current_led_pin != pin_number:  # Verifica si el pin actual es diferente al antiguo
            old_led = machine.Pin(pin_number, machine.Pin.OUT)
            old_led.value(False)  # Apaga el LED del pin antiguo

    # Iniciar el parpadeo del LED en un nuevo hilo
    _thread.start_new_thread(led_blinking_control, ())

    while True:
        # Verificar si hay actualizaciones disponibles
        update_available = ota.check_for_update()
        # Espera 60 segundos antes de la próxima verificación
        time.sleep(60)

# Punto de entrada del programa
if __name__ == '__main__':
    main()
