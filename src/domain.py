import platform
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import psutil

from src.ports import Logger

# --- Data Schemas ---


@dataclass
class CPUStatus:
    """Data transfer object representing a snapshot of CPU state and metrics."""

    name: str  # CPU model name/identifier
    architecture: str  # System architecture (e.g., x86_64, ARM)
    physical_cores: Optional[int]  # Number of physical CPU cores
    logical_cores: Optional[
        int
    ]  # Number of logical cores (including hyperthreading)  # noqa: E501
    current_frequency: float  # Current CPU frequency in MHz
    min_frequency: float  # Minimum supported CPU frequency in MHz
    max_frequency: float  # Maximum supported CPU frequency in MHz
    total_usage_percentage: float  # Overall CPU usage percentage across all cores
    usage_per_core: List[float]  # Individual usage percentage for each core
    average_load: Optional[List[float]]  # System load average over 1, 5, and 15 minutes
    user_time: float  # Time spent executing user processes
    system_time: float  # Time spent executing kernel processes
    idle_time: float  # Time spent idle
    current_temperature: Optional[
        float
    ]  # Current CPU temperature in Celsius (if available)  # noqa: E501
    timestamp: datetime  # Timestamp of the measurement


class CPUStateCheck:
    """Use case class responsible for capturing CPU state information."""

    def __init__(self, logger: Logger):
        # Initialize with a configured logger instance through dependency injection
        # The implementation follows the port-adapter pattern, accepting
        # any Logger port implementation
        self.logger = logger

    def capture(self) -> CPUStatus:
        """Captures the current CPU state and returns a CPUStatus object.

        Returns:
            CPUStatus: A dataclass instance containing comprehensive CPU metrics

        Note:
            Handles platform-specific variations and potential failures gracefully
            by providing fallback values and logging warnings when necessary.
        """
        self.logger.debug("Capturing CPU state...")

        # Frequency metrics - may not be available on all platforms
        freq = psutil.cpu_freq()
        if freq:
            current_freq, min_freq, max_freq = freq.current, freq.min, freq.max
        else:
            # Fallback values if frequency information is unavailable
            current_freq = min_freq = max_freq = 0.0

        # CPU time statistics
        times = psutil.cpu_times()

        # Average load - gracefully handle platforms that don't support this metric
        try:
            avg_load = list(psutil.getloadavg())
        except (AttributeError, OSError):
            # getloadavg is not available on Windows or may fail on some systems
            avg_load = None

        # Temperature sensors - handle potential failures or missing sensors
        temp = None
        try:
            temps = psutil.sensors_temperatures()
            # Take the first available temperature reading as reference
            if temps:
                first_sensor = next(iter(temps.values()))
                if first_sensor:
                    temp = first_sensor[0].current
        except Exception as e:
            # Log warning but don't fail the capture operation
            self.logger.warning(f"Could not retrieve temperature sensors: {e}")

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
            timestamp=datetime.now(),
        )
        return cpu_data
