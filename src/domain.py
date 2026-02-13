import platform
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import psutil

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

        # Frecuencia
        freq = psutil.cpu_freq()
        if freq:
            current_freq, min_freq, max_freq = freq.current, freq.min, freq.max
        else:
            current_freq = min_freq = max_freq = 0.0

        # Tiempos de CPU
        times = psutil.cpu_times()

        # Carga promedio (Manejo seguro para Windows/Sistemas sin soporte)
        try:
            avg_load = list(psutil.getloadavg())
        except (AttributeError, OSError):
            avg_load = None

        # Temperatura (Manejo de errores si falla el sensor)
        temp = None
        try:
            temps = psutil.sensors_temperatures()
            # Tomamos la primera temperatura disponible como referencia
            if temps:
                first_sensor = next(iter(temps.values()))
                if first_sensor:
                    temp = first_sensor[0].current
        except Exception:
            self.logger.warning("Could not retrieve temperature sensors")

        cpu_data = CPUStatus(
            name=platform.processor(),
            architecture=platform.machine(),
            physical_cores=psutil.cpu_count(logical=False),
            logical_cores=psutil.cpu_count(logical=True),
            current_frequency=current_freq,
            min_frequency=min_freq,
            max_frequency=max_freq,
            total_usage_percentage=psutil.cpu_percent(interval=None),
            usage_per_core=psutil.cpu_percent(interval=None, percpu=True),
            average_load=avg_load,
            user_time=times.user,
            system_time=times.system,
            idle_time=times.idle,
            current_temperature=temp,
            timestamp=datetime.now()
        )
        return cpu_data