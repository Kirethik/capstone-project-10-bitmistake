"""
Workload models for realistic IoT healthcare scenarios
"""
import random
import math

class WorkloadModel:
    """Base class for workload generation"""
    
    def __init__(self, base_rate=1.0, base_size=500):
        self.base_rate = base_rate
        self.base_size = base_size
    
    def generate_workload(self, sensor_id, time_step):
        """Generate workload parameters for given sensor at time step"""
        raise NotImplementedError

class SteadyWorkload(WorkloadModel):
    """Steady workload with minimal variation"""
    
    def __init__(self, base_rate=1.0, base_size=500, variation=0.1):
        super().__init__(base_rate, base_size)
        self.variation = variation
    
    def generate_workload(self, sensor_id, time_step):
        # Small random variation around base values
        rate_factor = 1.0 + random.uniform(-self.variation, self.variation)
        size_factor = 1.0 + random.uniform(-self.variation, self.variation)
        
        return {
            'flow_rate': self.base_rate * rate_factor,
            'flow_size': self.base_size * size_factor,
            'traffic_size': 0.5 * size_factor  # MB
        }

class BurstyWorkload(WorkloadModel):
    """Bursty workload with periodic high-intensity periods"""
    
    def __init__(self, base_rate=1.0, base_size=500, burst_factor=3.0, burst_period=100):
        super().__init__(base_rate, base_size)
        self.burst_factor = burst_factor
        self.burst_period = burst_period
    
    def generate_workload(self, sensor_id, time_step):
        # Create burst pattern using sine wave
        burst_phase = (time_step + sensor_id * 10) % self.burst_period
        burst_intensity = 1.0 + (self.burst_factor - 1.0) * max(0, math.sin(2 * math.pi * burst_phase / self.burst_period))
        
        return {
            'flow_rate': self.base_rate * burst_intensity,
            'flow_size': self.base_size * burst_intensity,
            'traffic_size': 0.5 * burst_intensity
        }

class HealthcareWorkload(WorkloadModel):
    """Healthcare-specific workload patterns"""
    
    def __init__(self, device_type="vital_monitor"):
        self.device_type = device_type
        self.patterns = {
            "vital_monitor": {"rate": 1.0, "size": 100, "variation": 0.2},
            "ecg_sensor": {"rate": 2.0, "size": 800, "variation": 0.3},
            "emergency_alert": {"rate": 0.1, "size": 50, "variation": 0.1}
        }
        
        pattern = self.patterns.get(device_type, self.patterns["vital_monitor"])
        super().__init__(pattern["rate"], pattern["size"])
        self.variation = pattern["variation"]
    
    def generate_workload(self, sensor_id, time_step):
        # Healthcare devices have predictable patterns with occasional spikes
        base_factor = 1.0 + random.uniform(-self.variation, self.variation)
        
        # Simulate emergency spikes (1% chance)
        if random.random() < 0.01:
            emergency_factor = 5.0
        else:
            emergency_factor = 1.0
        
        return {
            'flow_rate': self.base_rate * base_factor * emergency_factor,
            'flow_size': self.base_size * base_factor * emergency_factor,
            'traffic_size': 0.5 * base_factor * emergency_factor
        }