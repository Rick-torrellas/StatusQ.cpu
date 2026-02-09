from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime


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