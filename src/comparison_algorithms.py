from yafs import Placement
import random

class RandomPlacement(Placement):
    """Random placement algorithm for comparison"""
    def __init__(self, name, json_file, digital_twin):
        super().__init__(name, json_file)
        self.digital_twin = digital_twin
        self.module_assignments = {}
        self.activation_dist = None
    
    def initial_allocation(self, sim, app_name):
        app = sim.apps[app_name]
        modules_to_place = [m for m in app.modules if "Processing_Module" in m]
        
        for module_name in modules_to_place:
            # Random fog node selection
            fog_node_id = random.randint(0, len(self.digital_twin.fog_nodes) - 1)
            node_name = f"fog_{fog_node_id}"
            sim.deploy_module(app_name, module_name, [], [node_name])
            
            if fog_node_id not in self.module_assignments:
                self.module_assignments[fog_node_id] = []
            sensor_id = int(module_name.split("_")[-1])
            sensor = next(s for s in self.digital_twin.sensors if s.device_id == sensor_id)
            self.module_assignments[fog_node_id].append(sensor)

class DistancePlacement(Placement):
    """Distance-based placement for comparison"""
    def __init__(self, name, json_file, digital_twin):
        super().__init__(name, json_file)
        self.digital_twin = digital_twin
        self.module_assignments = {}
        self.activation_dist = None
    
    def initial_allocation(self, sim, app_name):
        app = sim.apps[app_name]
        modules_to_place = [m for m in app.modules if "Processing_Module" in m]
        
        for module_name in modules_to_place:
            sensor_id = int(module_name.split("_")[-1])
            sensor = next(s for s in self.digital_twin.sensors if s.device_id == sensor_id)
            
            # Find closest fog node
            min_distance = float('inf')
            closest_node_id = 0
            
            for i, fog_node in enumerate(self.digital_twin.fog_nodes):
                dx = sensor.coordinates[0] - fog_node.coordinates[0]
                dy = sensor.coordinates[1] - fog_node.coordinates[1]
                distance = (dx**2 + dy**2)**0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_node_id = i
            
            node_name = f"fog_{closest_node_id}"
            sim.deploy_module(app_name, module_name, [], [node_name])
            
            if closest_node_id not in self.module_assignments:
                self.module_assignments[closest_node_id] = []
            self.module_assignments[closest_node_id].append(sensor)