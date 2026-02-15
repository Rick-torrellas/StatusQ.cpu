import platform
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, cast

import psutil
from psutil._common import scpufreq, scputimes

from src.ports import Logger

# --- Data Schemas ---


@dataclass
class CPUStatus:
    """Data transfer object representing a snapshot of CPU state and metrics."""

    name: str  # CPU model name/identifier
    architecture: str  # System architecture (e.g., x86_64, ARM)
    physical_cores: Optional[int]  # Number of physical CPU cores
    logical_cores: Optional[int]  # Number of logical cores (including hyperthreading)
    current_frequency: float  # Current CPU frequency in MHz
    min_frequency: float  # Minimum supported CPU frequency in MHz
    max_frequency: float  # Maximum supported CPU frequency in MHz
    total_usage_percentage: float  # Overall CPU usage percentage across all cores
    usage_per_core: List[float]  # Individual usage percentage for each core
    average_load: Optional[List[float]]  # System load average over 1, 5, and 15 minutes
    user_time: float  # Time spent executing user processes
    system_time: float  # Time spent executing kernel processes
    idle_time: float  # Time spent idle
    current_temperature: Optional[float]  # Current CPU temperature in Celsius (if available)
    timestamp: datetime  # Timestamp of the measurement


class CPUStateCheck:
    """Use case class responsible for capturing CPU state information."""

    def __init__(self, logger: Logger) -> None:
        # Initialize with a configured logger instance through dependency injection
        # The implementation follows the port-adapter pattern, accepting
        # any Logger port implementation
        self.logger: Logger = logger

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
        freq: Optional[scpufreq] = psutil.cpu_freq()
        if freq is not None:
            current_freq: float = freq.current
            min_freq: float = freq.min
            max_freq: float = freq.max
        else:
            # Fallback values if frequency information is unavailable
            current_freq = min_freq = max_freq = 0.0

        # CPU time statistics
        times: scputimes = psutil.cpu_times()

        # Average load - gracefully handle platforms that don't support this metric
        avg_load: Optional[List[float]] = None
        try:
            load_avg_tuple = psutil.getloadavg()
            avg_load = list(load_avg_tuple)
        except (AttributeError, OSError):
            # getloadavg is not available on Windows or may fail on some systems
            pass

        # Temperature sensors - handle potential failures or missing sensors
        temp: Optional[float] = None
        try:
            temps_dict = psutil.sensors_temperatures()
            # Take the first available temperature reading as reference
            if temps_dict:
                # Get the first sensor readings list
                first_sensor_readings = next(iter(temps_dict.values()))
                if first_sensor_readings and len(first_sensor_readings) > 0:
                    # Get the current temperature from the first reading
                    temp = float(first_sensor_readings[0].current)
        except Exception as e:
            # Log warning but don't fail the capture operation
            self.logger.warning(f"Could not retrieve temperature sensors: {e}")

        # CPU core counts
        physical_cores: Optional[int] = psutil.cpu_count(logical=False)
        logical_cores: Optional[int] = psutil.cpu_count(logical=True)

        # CPU usage percentages
        total_usage: float = psutil.cpu_percent(interval=None)
        per_core_usage: List[float] = cast(List[float], psutil.cpu_percent(interval=None, percpu=True))

        cpu_data = CPUStatus(
            name=platform.processor() or "Unknown",
            architecture=platform.machine() or "Unknown",
            physical_cores=physical_cores,
            logical_cores=logical_cores,
            current_frequency=current_freq,
            min_frequency=min_freq,
            max_frequency=max_freq,
            total_usage_percentage=total_usage,
            usage_per_core=per_core_usage,
            average_load=avg_load,
            user_time=times.user,
            system_time=times.system,
            idle_time=times.idle,
            current_temperature=temp,
            timestamp=datetime.now(),
        )
        return cpu_data