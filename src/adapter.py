import psutil
import platform
from datetime import datetime
from src.domain import CPUStatus
from src.ports import StateCheck

# --- Implementation ---

class CPUStateCheck(StateCheck):
    def capture(self) -> CPUStatus:
        times = psutil.cpu_times()
        freq = psutil.cpu_freq()
        
        # Temperature Logic
        temp = None
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                sensor_name = list(temps.keys())[0]
                temp = temps[sensor_name][0].current
        except Exception:
            temp = None

        return CPUStatus(
            name=platform.processor(),
            architecture=platform.machine(),
            physical_cores=psutil.cpu_count(logical=False),
            logical_cores=psutil.cpu_count(logical=True),
            current_frequency=freq.current if freq else 0.0,
            timestamp=datetime.now(),
            min_frequency=freq.min if freq else 0.0,
            max_frequency=freq.max if freq else 0.0,
            total_usage_percentage=psutil.cpu_percent(interval=1),
            usage_per_core=psutil.cpu_percent(percpu=True),
            average_load=list(psutil.getloadavg()) if hasattr(psutil, "getloadavg") else None,
            user_time=times.user,
            system_time=times.system,
            idle_time=times.idle,
            current_temperature=temp
        )