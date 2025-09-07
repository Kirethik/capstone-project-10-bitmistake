class SensorDevice:
    """
    Tier 1 - IoT Layer Entity representing a patient sensor
    Contains all attributes required by OLB equations
    """
    def __init__(self, device_id, coordinates, transmission_power, 
                 average_flow_rate, flow_traffic_size, average_flow_size):
        self.device_id = device_id
        self.coordinates = coordinates  # (x, y) tuple
        self.transmissionPower = transmission_power  # P(x) in Watts
        self.averageFlowRate = average_flow_rate  # fl(x) in Hz
        self.flowTrafficSize = flow_traffic_size  # l(x) in megabits
        self.averageFlowSize = average_flow_size  # ν(x) in MI

    def __str__(self):
        return f"Sensor_{self.device_id} at {self.coordinates}"

    def __repr__(self):
        return self.__str__()


class FogNodeDevice:
    """
    Tier 2 - Fog Layer Entity representing fog computing nodes
    Contains all attributes required by OLB equations
    """
    def __init__(self, node_id, coordinates, processing_power, bandwidth, 
                 carrier_frequency, noise_power):
        self.node_id = node_id
        self.coordinates = coordinates  # (x, y) tuple
        self.processingPower = processing_power  # Cj in MIPS
        self.bandwidth = bandwidth  # BWj in MHz
        self.carrierFrequency = carrier_frequency  # in GHz
        self.noisePower = noise_power  # σ^2 in Watts
        self.assigned_modules = []  # Track assigned processing modules

    def __str__(self):
        return f"FogNode_{self.node_id} at {self.coordinates}"

    def __repr__(self):
        return self.__str__()
