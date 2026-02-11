from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime
from src.ports import Logger


# --- Data Schemas ---

@dataclass
class CPUStatus:
    name: str
    architecture: str
    physical_cores: Optional[int]
    logical_cores: Optional[int]
    current_frequency: float
    min_frequency: float
    max_frequency: float
    total_usage_percentage: float
    usage_per_core: List[float]
    average_load: Optional[List[float]]
    user_time: float
    system_time: float
    idle_time: float
    current_temperature: Optional[float]
    timestamp: datetime


class CPUStateCheck:
    def __init__(self, logger: Logger):
        # Recibe un logger ya configurado. No necesita saber cómo se creó.
        self.logger = logger

    def capture(self) -> CPUStatus:
        """Captura el estado actual de la CPU y devuelve un objeto CPUStatus."""
        self.logger.debug("Capturing CPU state...")

        # Aquí iría la lógica real para obtener los datos de la CPU (usando psutil, etc.)
        # Por ahora, simulamos la data creando una instancia de CPUStatus.
        cpu_data = CPUStatus(
            name="Simulated CPU",
            architecture="x86_64",
            physical_cores=4,
            logical_cores=8,
            current_frequency=3400.0,
            min_frequency=800.0,
            max_frequency=4200.0,
            total_usage_percentage=20.0,
            usage_per_core=[10.0, 30.0, 15.0, 25.0],
            average_load=None,
            user_time=1000.0,
            system_time=500.0,
            idle_time=8500.0,
            current_temperature=45.0,
            timestamp=datetime.now()
        )
        return cpu_data