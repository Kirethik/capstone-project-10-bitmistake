"""
Comprehensive metrics definitions for OLB evaluation
"""

class MetricsDefinitions:
    """
    Standardized metrics definitions for fair algorithm comparison
    """
    
    @staticmethod
    def get_metrics_documentation():
        return {
            "latency_metrics": {
                "overall_latency": "Sum of communication and computing latencies across all sensors (ms)",
                "communication_latency": "Network transmission delays based on distance and SNR (ms)", 
                "computing_latency": "Processing delays based on fog node CPU utilization (ms)",
                "average_latency": "Mean latency per sensor assignment (ms)"
            },
            "energy_metrics": {
                "total_energy": "Sum of transmission and processing energy consumption (W)",
                "transmission_energy": "Energy used for wireless communication (W)",
                "processing_energy": "Energy used for computation at fog nodes (W)"
            },
            "cost_metrics": {
                "execution_cost": "Weighted combination of latency, energy, and network usage",
                "network_usage": "Total data transmission volume (MB/s)",
                "resource_utilization": "Average fog node CPU/memory utilization (%)"
            },
            "load_balance_metrics": {
                "load_variance": "Variance in fog node utilization levels",
                "max_utilization": "Highest fog node utilization percentage",
                "assignment_distribution": "Number of sensors per fog node"
            }
        }
    
    @staticmethod
    def calculate_energy_consumption(sensor, fog_node, distance):
        """Calculate energy consumption for sensor-fog assignment"""
        # Transmission energy: P_tx * t_tx
        transmission_time = sensor.flowTrafficSize / (fog_node.bandwidth * 1e-3)  # Convert MB to seconds
        transmission_energy = sensor.transmissionPower * transmission_time
        
        # Processing energy: P_cpu * t_proc  
        processing_time = sensor.averageFlowSize / fog_node.processingPower * 1e-3  # Convert MI to seconds
        processing_energy = fog_node.processingPower * 1e-6 * processing_time  # Assume 1W per 1000 MIPS
        
        return transmission_energy + processing_energy
    
    @staticmethod
    def calculate_load_balance_score(assignments):
        """Calculate load balance quality score"""
        if not assignments:
            return 0
        
        loads = [len(sensors) for sensors in assignments.values()]
        if len(loads) <= 1:
            return 1.0
            
        mean_load = sum(loads) / len(loads)
        variance = sum((load - mean_load)**2 for load in loads) / len(loads)
        
        # Lower variance = better balance (normalize to 0-1 scale)
        return 1.0 / (1.0 + variance)