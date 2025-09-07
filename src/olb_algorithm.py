import math
from yafs import Placement


class OLBLatencyCalculator:
    """
    Core OLB mathematical model implementation
    Implements all latency calculation formulas
    """
    def __init__(self):
        self.speed_of_light = 299792458  # m/s
    
    def calculate_distance(self, sensor_coords, fog_coords):
        """Calculate Euclidean distance between sensor and fog node"""
        dx = sensor_coords[0] - fog_coords[0]
        dy = sensor_coords[1] - fog_coords[1]
        return math.sqrt(dx**2 + dy**2)
    
    def calculate_channel_gain(self, distance, carrier_frequency):
        """Calculate Channel Gain (g(x))"""
        if distance == 0:
            distance = 1  # Avoid division by zero
        
        wavelength = self.speed_of_light / (carrier_frequency * 1e9)
        channel_gain = 10 * math.log10(wavelength**2 / (4 * math.pi * distance)**2)
        return channel_gain
    
    def calculate_snr(self, transmission_power, channel_gain, noise_power):
        """Calculate Signal-to-Noise Ratio (SNR(x))"""
        linear_gain = 10**(channel_gain/10)
        return (transmission_power * linear_gain) / noise_power
    
    def calculate_device_capacity(self, bandwidth, snr):
        """Calculate Device Capacity (cj(x))"""
        return bandwidth * (1 + snr)
    
    def calculate_individual_traffic_load(self, flow_rate, traffic_size, device_capacity):
        """Calculate Individual Traffic Load (eaj(x))"""
        if device_capacity == 0:
            return 1.0
        return (flow_rate * traffic_size) / device_capacity
    
    def calculate_individual_computing_load(self, flow_rate, flow_size, processing_power):
        """Calculate Individual Computing Load (ebj(x))"""
        if processing_power == 0:
            return 1.0
        return (flow_rate * flow_size) / processing_power
    
    def calculate_communication_latency(self, sensor, fog_node, assigned_sensors):
        """
        Task 3.1.1: Communication Latency Analysis (L_m(j))
        """
        try:
            # Calculate Distance (d)
            distance = self.calculate_distance(sensor.coordinates, fog_node.coordinates)
            
            # Calculate wavelength λ
            wavelength = self.speed_of_light / (fog_node.carrierFrequency * 1e9)
            
            # Calculate Channel Gain (g(x))
            channel_gain = 10 * math.log10(wavelength**2 / (4 * math.pi * distance)**2)
            
            # Calculate Signal-to-Noise Ratio (SNR(x))
            linear_gain = 10**(channel_gain/10)
            snr = (sensor.transmissionPower * linear_gain) / fog_node.noisePower
            
            # Calculate Device Capacity (cj(x))
            device_capacity = fog_node.bandwidth * (1 + snr)
            
            # Calculate Individual Traffic Load (eaj(x))
            individual_traffic_load = (sensor.averageFlowRate * sensor.flowTrafficSize) / device_capacity
            
            # Calculate Total Traffic Load (TLj)
            total_traffic_load = individual_traffic_load
            for assigned_sensor in assigned_sensors:
                assigned_load = (assigned_sensor.averageFlowRate * assigned_sensor.flowTrafficSize) / device_capacity
                total_traffic_load += assigned_load
            
            # Ensure total load doesn't exceed 1 (would cause infinite latency)
            if total_traffic_load >= 1:
                total_traffic_load = 0.99
            
            # Calculate Communication Latency Score (L_m(j))
            comm_latency = total_traffic_load / (1 - total_traffic_load)
            
            return comm_latency
            
        except (ZeroDivisionError, ValueError, OverflowError):
            return float('inf')
    
    def calculate_computing_latency(self, sensor, fog_node, assigned_sensors):
        """
        Task 3.1.2: Computing Latency Analysis (L_p(j))
        """
        try:
            # Calculate Individual Computing Load (ebj(x))
            individual_computing_load = (sensor.averageFlowRate * sensor.averageFlowSize) / fog_node.processingPower
            
            # Calculate Total Computing Load (CLj)
            total_computing_load = individual_computing_load
            for assigned_sensor in assigned_sensors:
                assigned_comp_load = (assigned_sensor.averageFlowRate * assigned_sensor.averageFlowSize) / fog_node.processingPower
                total_computing_load += assigned_comp_load
            
            # Ensure total load doesn't exceed 1 (would cause infinite latency)
            if total_computing_load >= 1:
                total_computing_load = 0.99
            
            # Calculate Computing Latency Score (L_p(j))
            comp_latency = total_computing_load / (1 - total_computing_load)
            
            return comp_latency
            
        except (ZeroDivisionError, ValueError, OverflowError):
            return float('inf')


class OLBPlacement(Placement):
    """
    Phase 3: OLB Algorithm Implementation
    Custom YAFS Placement policy implementing the core OLB algorithm
    """
    def __init__(self, name, json_file, digital_twin):
        super(OLBPlacement, self).__init__(name, json_file)
        self.digital_twin = digital_twin
        self.calculator = OLBLatencyCalculator()
        self.module_assignments = {}  # Track which modules are assigned to which nodes
        
        # Set activation distribution to None to avoid the error
        self.activation_dist = None
        
    def initial_allocation(self, sim, app_name):
        """
        Initial allocation of modules to devices using OLB algorithm
        This is the core YAFS method that gets called during simulation setup
        """
        app = sim.apps[app_name]
        
        # Get all modules that need placement (processing modules)
        modules_to_place = []
        for module_name in app.modules:
            if "Processing_Module" in module_name:
                modules_to_place.append(module_name)
        
        print(f"OLB: Placing {len(modules_to_place)} processing modules...")
        
        # Apply OLB algorithm for each processing module
        for module_name in modules_to_place:
            # Extract sensor ID from module name
            sensor_id = self._extract_sensor_id(module_name)
            sensor = self._find_sensor_by_id(sensor_id)
            
            if sensor:
                # Find optimal fog node using OLB algorithm
                optimal_node_id = self._find_optimal_fog_node(sensor)
                
                if optimal_node_id is not None:
                    # Deploy module to optimal node in YAFS
                    node_name = f"fog_{optimal_node_id}"
                    # For processing modules, we deploy with empty services list
                    sim.deploy_module(app_name, module_name, [], [node_name])
                    
                    # Track assignment in our digital twin
                    if optimal_node_id not in self.module_assignments:
                        self.module_assignments[optimal_node_id] = []
                    self.module_assignments[optimal_node_id].append(sensor)
                    
                    print(f"OLB: Deployed {module_name} (Sensor {sensor_id}) -> {node_name}")
                else:
                    # Fallback to first fog node if OLB fails
                    fallback_node = "fog_0"
                    sim.deploy_module(app_name, module_name, [], [fallback_node])
                    print(f"OLB: Fallback deployment {module_name} -> {fallback_node}")
    
    def _extract_sensor_id(self, module_name):
        """Extract sensor ID from module name"""
        # Assuming module names like "Processing_Module_Sensor_X"
        parts = module_name.split("_")
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
        return 0
    
    def _find_sensor_by_id(self, sensor_id):
        """Find sensor device by ID"""
        for sensor in self.digital_twin.sensors:
            if sensor.device_id == sensor_id:
                return sensor
        return None
    
    def _find_optimal_fog_node(self, sensor):
        """
        Core OLB Decision Logic
        Finds optimal fog node by calculating total latency score
        """
        min_latency = float('inf')
        optimal_node_id = None
        
        print(f"  OLB: Evaluating fog nodes for Sensor {sensor.device_id}...")
        
        # Iterate through all candidate Tier 2 Fog Nodes
        for i, fog_node in enumerate(self.digital_twin.fog_nodes):
            try:
                # Get currently assigned sensors to this node
                assigned_sensors = self.module_assignments.get(i, [])
                
                # Calculate communication latency L_m(j)
                comm_latency = self.calculator.calculate_communication_latency(sensor, fog_node, assigned_sensors)
                
                # Calculate computing latency L_p(j)
                comp_latency = self.calculator.calculate_computing_latency(sensor, fog_node, assigned_sensors)
                
                # Final score calculation
                total_latency = comm_latency + comp_latency
                
                print(f"    Fog Node {i}: Comm={comm_latency:.4f}, Comp={comp_latency:.4f}, Total={total_latency:.4f}")
                
                if total_latency < min_latency:
                    min_latency = total_latency
                    optimal_node_id = i
                    
            except (ZeroDivisionError, ValueError, OverflowError) as e:
                print(f"    Warning: Error calculating latency for fog node {i}: {e}")
                continue
        
        print(f"  OLB: Selected Fog Node {optimal_node_id} with latency {min_latency:.4f}")
        return optimal_node_id
