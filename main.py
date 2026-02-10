from src.adapter import CPUStateCheck, AppLogger
from src.ports import Logger
from src.logs import setup_logging

def main(logger: Logger):
    # Set up logging
    setup_logging()
    logger.info("Starting application")
    # Capture CPU state
    cpu_checker = CPUStateCheck()
    cpu_data = cpu_checker.capture()
    logger.debug(cpu_data)
    # display cpy info
    logger.info(f"Checking hardware: {cpu_data.name}")
    logger.info(f"Architecture: {cpu_data.current_temperature}")
    logger.info(f"Current Usage: {cpu_data.total_usage_percentage}%")

if __name__ == "__main__":
    logger = AppLogger(__name__)
    main(logger)