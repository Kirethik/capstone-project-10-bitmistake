from .olb_algorithm import OLBLatencyCalculator


class PerformanceMetrics:
    """
    Phase 4: Performance Reporting
    Collects and reports KPIs from YAFS simulation
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
        
    def collect_metrics(self, digital_twin, placement):
        """
        Collect performance metrics from YAFS simulation
        """
        print("Collecting performance metrics...")
        
        calculator = OLBLatencyCalculator()
        
        total_comm_latency = 0
        total_comp_latency = 0
        
        # Calculate OLB-specific metrics
        for node_id, assigned_sensors in placement.module_assignments.items():
            fog_node = digital_twin.fog_nodes[node_id]
            
            for sensor in assigned_sensors:
                other_sensors = [s for s in assigned_sensors if s != sensor]
                comm_lat = calculator.calculate_communication_latency(sensor, fog_node, other_sensors)
                comp_lat = calculator.calculate_computing_latency(sensor, fog_node, other_sensors)
                
                total_comm_latency += comm_lat
                total_comp_latency += comp_lat
                
                self.detailed_assignments.append({
                    'sensor_id': sensor.device_id,
                    'fog_node_id': fog_node.node_id,
                    'comm_latency': comm_lat,
                    'comp_latency': comp_lat,
                    'total_latency': comm_lat + comp_lat,
                    'sensor_coordinates': sensor.coordinates,
                    'fog_node_coordinates': fog_node.coordinates
                })
        
        self.overall_latency = total_comm_latency + total_comp_latency
        self.communication_latency = total_comm_latency
        self.computing_latency = total_comp_latency
        
        # Network Usage (Nusage)
        self.network_usage = sum(sensor.averageFlowRate * sensor.flowTrafficSize 
                               for sensor in digital_twin.sensors)
        
        # Execution Time (Te) - average latency per sensor
        self.execution_time = self.overall_latency / len(digital_twin.sensors) if digital_twin.sensors else 0
        
        # Energy Consumption (Etotal)
        self.energy_consumption = sum(fog_node.processingPower * 0.001  # Simple power model
                                    for fog_node in digital_twin.fog_nodes)
        
        # Cost of Execution (Ce)
        self.cost_of_execution = (self.overall_latency * 0.1 + 
                                self.network_usage * 0.05 + 
                                self.energy_consumption * 0.02)
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        report = f"""
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
        """Get metrics as dictionary for further processing"""
        return {
            'overall_latency': self.overall_latency,
            'communication_latency': self.communication_latency,
            'computing_latency': self.computing_latency,
            'network_usage': self.network_usage,
            'execution_time': self.execution_time,
            'energy_consumption': self.energy_consumption,
            'cost_of_execution': self.cost_of_execution,
            'detailed_assignments': self.detailed_assignments
        }
