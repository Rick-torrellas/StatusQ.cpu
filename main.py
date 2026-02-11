from src.adapter import AppLogger
from src.domain import CPUStateCheck
from src.ports import Logger
from src.logs import setup_logging

def main(logger: Logger, cpu_checker: CPUStateCheck):
    logger.info("Starting application")
    # Capture CPU state
    cpu_data = cpu_checker.capture()
    # logger.debug(cpu_data)
    # display cpy info
    logger.info(f"Checking hardware: {cpu_data.name}")
    logger.info(f"Current Temperature: {cpu_data.current_temperature}")
    logger.info(f"Current Usage: {cpu_data.total_usage_percentage}%")

if __name__ == "__main__":
    # Set up logging at the entry point of the application
    setup_logging()

    # --- Composition Root ---
    # Aquí es donde se "cablea" la aplicación.
    # Se crean las implementaciones concretas y se inyectan en las clases que las necesitan.

    # 1. Crear los loggers específicos usando la clase concreta AppLogger
    root_logger = AppLogger(__name__)
    cpu_checker_logger = AppLogger('src.domain.CPUStateCheck')

    # 2. Crear las instancias de los servicios del dominio, inyectando sus dependencias
    cpu_checker = CPUStateCheck(logger=cpu_checker_logger)

    # 3. Ejecutar la lógica principal de la aplicación
    main(logger=root_logger, cpu_checker=cpu_checker)