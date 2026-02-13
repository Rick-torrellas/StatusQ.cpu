from rich import print

from src.adapter import AppLogger
from src.domain import CPUStateCheck
from src.logs import setup_logging
from src.ports import Logger

#if len(sys.argv) > 1:

def main(logger: Logger, cpu_checker: CPUStateCheck):
    logger.info("Starting application")
    # Capture CPU state
    cpu_data = cpu_checker.capture()
    # logger.debug(cpu_data)
    # Muestra la información de la CPU en la consola con el formato de rich
    print(cpu_data)
    # Registra la información en el archivo de log como un string
    logger.info(f"CPU Data Captured: {cpu_data}")

if __name__ == "__main__":
    # Set up logging at the entry point of the application
    setup_logging()

    # --- Composition Root ---
    # Aquí es donde se "cablea" la aplicación.
    # Se crean las implementaciones concretas y se inyectan en las clases que las 
    # necesitan.

    # 1. Crear los loggers específicos usando la clase concreta AppLogger
    root_logger = AppLogger(__name__)
    cpu_checker_logger = AppLogger('src.domain.CPUStateCheck')

    # 2. Crear las instancias de los servicios del dominio, inyectando sus dependencias
    cpu_checker = CPUStateCheck(logger=cpu_checker_logger)

    argumentos  = {
        'logger': root_logger,
        'cpu_checker': cpu_checker
    }

    # 3. Ejecutar la lógica principal de la aplicación
    main(**argumentos)