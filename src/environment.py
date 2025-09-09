import random
from .devices import SensorDevice, FogNodeDevice


class DigitalTwinEnvironment:
    """
    Phase 1: Environment Construction - The Digital Twin
    Manages the 2D coordinate system and all physical entities
    """
    def __init__(self, width=3000, height=2000):
        self.width = width
        self.height = height
        self.sensors = []
        self.fog_nodes = []
        self.cloud_node = None
        self.proxy_node = None
        
    def add_sensor(self, sensor):
        """Add sensor to the environment"""
        if 0 <= sensor.coordinates[0] <= self.width and 0 <= sensor.coordinates[1] <= self.height:
            self.sensors.append(sensor)
        else:
            raise ValueError(f"Sensor coordinates {sensor.coordinates} outside environment bounds")
    
    def add_fog_node(self, fog_node):
        """Add fog node to the environment"""
        if 0 <= fog_node.coordinates[0] <= self.width and 0 <= fog_node.coordinates[1] <= self.height:
            self.fog_nodes.append(fog_node)
        else:
            raise ValueError(f"Fog node coordinates {fog_node.coordinates} outside environment bounds")

    def initialize_sensors(self, num_sensors=10, seed=None):
        """
        Task 1.2: Model Tier 1 - IoT Layer Entities
        Initialize sensors with random parameters
        """
        if seed is not None:
            random.seed(seed)
            
        # Initializing sensors silently
        for i in range(num_sensors):
            coordinates = (random.uniform(0, self.width), random.uniform(0, self.height))
            transmission_power = random.uniform(0.1, 1.0)  # Watts
            average_flow_rate = random.uniform(0.5, 2.0)   # Hz
            flow_traffic_size = random.uniform(0.1, 1.0)   # MB
            average_flow_size = random.uniform(100, 1000)  # MI
            
            sensor = SensorDevice(
                device_id=i,
                coordinates=coordinates,
                transmission_power=transmission_power,
                average_flow_rate=average_flow_rate,
                flow_traffic_size=flow_traffic_size,
                average_flow_size=average_flow_size
            )
            self.add_sensor(sensor)

    def initialize_fog_nodes(self, num_fog_nodes=6, seed=None):
        """
        Task 1.3: Model Tier 2 - Fog Layer Entities
        Initialize fog nodes with random parameters
        """
        if seed is not None:
            random.seed(seed + 100)  # Different seed offset for fog nodes
            
        # Initializing fog nodes silently
        for i in range(num_fog_nodes):
            coordinates = (random.uniform(500, 2500), random.uniform(500, 1500))
            processing_power = random.uniform(1000, 5000)  # MIPS
            bandwidth = random.uniform(10, 100)            # MHz
            carrier_frequency = random.uniform(2.4, 5.0)   # GHz
            noise_power = random.uniform(1e-12, 1e-10)     # Watts
            
            fog_node = FogNodeDevice(
                node_id=i,
                coordinates=coordinates,
                processing_power=processing_power,
                bandwidth=bandwidth,
                carrier_frequency=carrier_frequency,
                noise_power=noise_power
            )
            self.add_fog_node(fog_node)

    def get_summary(self):
        """Get summary of the environment"""
        return {
            'environment_size': (self.width, self.height),
            'num_sensors': len(self.sensors),
            'num_fog_nodes': len(self.fog_nodes),
            'sensor_positions': [s.coordinates for s in self.sensors],
            'fog_node_positions': [f.coordinates for f in self.fog_nodes]
        }
