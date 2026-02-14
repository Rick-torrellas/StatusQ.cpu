from rich import print

from src.adapter import AppLogger
from src.domain import CPUStateCheck
from src.logs import setup_logging
from src.ports import Logger

# if len(sys.argv) > 1:  # Command-line argument handling (commented out)


def main(logger: Logger, cpu_checker: CPUStateCheck):
    """Application entry point that orchestrates the CPU monitoring workflow.

    Args:
        logger: Logger instance conforming to the Logger port interface
        cpu_checker: Domain service for capturing CPU state information
    """
    logger.info("Starting application")

    # Capture CPU state using the domain service
    cpu_data = cpu_checker.capture()

    # logger.debug(cpu_data)  # Detailed logging commented out for brevity

    # Display formatted CPU information in the console using rich's pretty-printing
    print(cpu_data)

    # Persist CPU data to log files as a structured string representation
    logger.info(f"CPU Data Captured: {cpu_data}")


if __name__ == "__main__":
    # Bootstrap the logging system at application startup
    # This configures all handlers, filters, and formatters defined in src.logs
    setup_logging()

    # --- Composition Root ---
    # Central location for dependency injection and object graph construction
    # Following the composition root pattern, all dependencies are wired here
    # Concrete implementations are instantiated and injected into dependent classes

    # 1. Create specific logger instances using the concrete AppLogger adapter
    #    The adapter implements the Logger port interface
    root_logger = AppLogger(__name__)  # Main application logger
    cpu_checker_logger = AppLogger("src.domain.CPUStateCheck")  # Domain-specific logger

    # 2. Instantiate domain services with their dependencies injected
    #    CPUStateCheck receives its logger through constructor injection
    cpu_checker = CPUStateCheck(logger=cpu_checker_logger)

    # Prepare arguments for the main function
    argumentos = {"logger": root_logger, "cpu_checker": cpu_checker}

    # 3. Execute the core application logic with fully constructed dependencies
    main(**argumentos)
