from .olb_algorithm import OLBLatencyCalculator
from .metrics_definitions import MetricsDefinitions


class PerformanceMetrics:
    """
    Enhanced performance metrics collection with standardized definitions
    """
    def __init__(self):
        self.overall_latency = 0
        self.network_usage = 0
        self.execution_time = 0
        self.energy_consumption = 0
        self.cost_of_execution = 0
        self.communication_latency = 0
        self.computing_latency = 0
        self.detailed_assignments = []
        self.load_balance_score = 0
        self.max_utilization = 0
        self.algorithm_name = "Unknown"

        print("[DEBUG] MetricsCollector initialized")
        
    def collect_metrics(self, digital_twin, placement, algorithm_name="Unknown"):

        """
        Collectes metrics for a given placement in the OLB algorithm
        """

        print("f[INFO] Collecting metrics for algorithm : {algorithm_name}")
        self.algorithm_name = algorithm_name
        calculator = OLBLatencyCalculator()
        
        total_comm_latency = 0
        total_comp_latency = 0
        total_energy = 0
        node_utilizations = []
        
        for node_id, assigned_sensors in placement.module_assignments.items():
            if node_id >= len(digital_twin.fog_nodes):
                continue
                
            fog_node = digital_twin.fog_nodes[node_id]
            node_load = len(assigned_sensors)
            node_utilizations.append(node_load)
            
            for sensor in assigned_sensors:
                other_sensors = [s for s in assigned_sensors if s != sensor]
                comm_lat = calculator.calculate_communication_latency(sensor, fog_node, other_sensors)
                comp_lat = calculator.calculate_computing_latency(sensor, fog_node, other_sensors)

                print(f"[TRACE] Sensor {sensor.device_id} -> Fog {fog_node.node_id}, "f"CommLat={comm_lat:.4f}, CompLat={comp_lat:.4f}, Energy={energy:.4f}")  

                
                if comm_lat == float('inf') or comp_lat == float('inf'):
                    comm_lat = 1000
                    comp_lat = 1000
                
                distance = calculator.calculate_distance(sensor.coordinates, fog_node.coordinates)
                energy = MetricsDefinitions.calculate_energy_consumption(sensor, fog_node, distance)
                
                total_comm_latency += comm_lat
                total_comp_latency += comp_lat
                total_energy += energy
                
                self.detailed_assignments.append({
                    'sensor_id': sensor.device_id,
                    'fog_node_id': fog_node.node_id,
                    'comm_latency': comm_lat,
                    'comp_latency': comp_lat,
                    'total_latency': comm_lat + comp_lat,
                    'energy': energy,
                    'distance': distance,
                    'sensor_coordinates': sensor.coordinates,
                    'fog_node_coordinates': fog_node.coordinates
                })
        
        self.overall_latency = total_comm_latency + total_comp_latency
        self.communication_latency = total_comm_latency
        self.computing_latency = total_comp_latency
        self.energy_consumption = total_energy
        
        self.network_usage = sum(sensor.averageFlowRate * sensor.flowTrafficSize 
                               for sensor in digital_twin.sensors)
        self.execution_time = self.overall_latency / len(digital_twin.sensors) if digital_twin.sensors else 0
        
        self.load_balance_score = MetricsDefinitions.calculate_load_balance_score(placement.module_assignments)
        self.max_utilization = max(node_utilizations) if node_utilizations else 0
        
        self.cost_of_execution = (self.overall_latency * 0.1 + 
                                self.network_usage * 0.05 + 
                                self.energy_consumption * 0.02)
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        report = f"""
        print("[INFO] Generating performance report...")
=== YAFS OLB SIMULATION PERFORMANCE REPORT ===

KEY PERFORMANCE INDICATORS (KPIs):
Overall Latency (L): {self.overall_latency:.4f}
  - Communication Latency: {self.communication_latency:.4f}
  - Computing Latency: {self.computing_latency:.4f}
Network Usage (Nusage): {self.network_usage:.4f} MB/s
Execution Time (Te): {self.execution_time:.4f} ms
Energy Consumption (Etotal): {self.energy_consumption:.4f} W
Cost of Execution (Ce): {self.cost_of_execution:.4f}

DETAILED ASSIGNMENT ANALYSIS:
"""
        
        # Group assignments by fog node
        node_assignments = {}
        for assignment in self.detailed_assignments:
            node_id = assignment['fog_node_id']
            if node_id not in node_assignments:
                node_assignments[node_id] = []
            node_assignments[node_id].append(assignment)
        
        for node_id, assignments in node_assignments.items():
            report += f"\nFog Node {node_id}: {len(assignments)} sensors assigned\n"
            for assignment in assignments:
                report += f"  Sensor {assignment['sensor_id']}: Total Latency = {assignment['total_latency']:.4f}\n"
                report += f"    - Communication Latency: {assignment['comm_latency']:.4f}\n"
                report += f"    - Computing Latency: {assignment['comp_latency']:.4f}\n"
                report += f"    - Sensor Position: {assignment['sensor_coordinates']}\n"
                report += f"    - Fog Node Position: {assignment['fog_node_coordinates']}\n"
        
        report += "\n========================================\n"
        return report
    
    def get_summary_dict(self):
        """Get comprehensive metrics as dictionary"""
        return {
            'algorithm': self.algorithm_name,
            'overall_latency': self.overall_latency,
            'communication_latency': self.communication_latency,
            'computing_latency': self.computing_latency,
            'network_usage': self.network_usage,
            'execution_time': self.execution_time,
            'energy_consumption': self.energy_consumption,
            'cost_of_execution': self.cost_of_execution,
            'load_balance_score': self.load_balance_score,
            'max_utilization': self.max_utilization,
            'num_assignments': len(self.detailed_assignments),
            'detailed_assignments': self.detailed_assignments
        }
