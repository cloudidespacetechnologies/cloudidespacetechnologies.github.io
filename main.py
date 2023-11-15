import machine
import time
import _thread
import ota  # Asegúrate de tener este módulo

# Constantes para la versión del firmware y la URL de actualización
FIRMWARE_VERSION = 1.1  # Debe ser un float
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
    while not stop_blinking:
        led.value(not led.value())  # Cambia el estado del LED
        time.sleep(0.5)  # Parpadeo cada 0.5 segundos

def device_control_logic():
    """
    Lógica de control para dispositivos/actuadores (como LEDs, relés, etc.)
    """
    global stop_blinking
    global current_led_pin
    try:
        while True:
            # Encender el LED
            led.value(True)

            # Iniciar el parpadeo del LED
            stop_blinking = False
            _thread.start_new_thread(led_blinking_control, ())

            # Esperar 5 segundos
            time.sleep(5)

            # Detener el parpadeo del LED
            stop_blinking = True

            # Apagar el LED
            led.value(False)

            # Cambiar el pin del LED (simplemente cambia este valor)
            new_led_pin = 19  # Cambia este valor al nuevo pin que desees
            led.init(machine.Pin(new_led_pin, machine.Pin.OUT))
            current_led_pin = new_led_pin

            # Esperar 1 segundo antes de repetir el ciclo
            time.sleep(1)
    except KeyboardInterrupt:
        stop_blinking = True  # Asegurarse de que el parpadeo se detenga antes de salir

def main():
    """
    Función principal que inicializa los hilos y procesos necesarios.
    """
    global stop_blinking
    global current_led_pin

    # Iniciar el parpadeo del LED en un nuevo hilo
    _thread.start_new_thread(led_blinking_control, ())

    while True:
        # Verificar si hay actualizaciones disponibles
        update_available = ota.check_for_update()

        if update_available:
            print("Actualización disponible. Aplicando actualización...")
            stop_blinking = True  # Detener el parpadeo del LED

            # Apaga el LED anterior
            led.value(0)

            # Cambia el pin al nuevo valor
            new_led_pin = 19  # Cambia este valor al nuevo pin que desees
            led.init(machine.Pin(new_led_pin, machine.Pin.OUT))
            current_led_pin = new_led_pin

            # Reanuda el parpadeo en el nuevo LED
            stop_blinking = False

            print("LED cambiado a GPIO {}".format(new_led_pin))
        else:
            print("No hay actualizaciones disponibles.")

        # Espera 60 segundos antes de la próxima verificación
        time.sleep(60)

# Punto de entrada del programa
if __name__ == '__main__':
    main()
