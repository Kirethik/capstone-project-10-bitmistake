import random
import math

class WorkloadModel:
    def __init__(self, model_type="steady"):
        self.model_type = model_type
    
    def generate_workload(self, base_rate, time_step):
        if self.model_type == "steady":
            return base_rate
        elif self.model_type == "periodic":
            return base_rate * (1 + 0.3 * math.sin(time_step * 0.1))
        elif self.model_type == "bursty":
            if random.random() < 0.1:
                return base_rate * 3
            return base_rate * 0.5
        elif self.model_type == "random":
            return base_rate * random.uniform(0.5, 1.5)
        return base_rate

class HealthcareWorkloadModel(WorkloadModel):
    def __init__(self, scenario_type="icu"):
        super().__init__()
        self.scenario_type = scenario_type
    
    def generate_critical_workload(self, base_rate, time_step):
        if self.scenario_type == "icu":
            return base_rate * (1 + 0.1 * random.random())
        elif self.scenario_type == "emergency":
            return base_rate * random.uniform(1.5, 3.0)
        return base_rate