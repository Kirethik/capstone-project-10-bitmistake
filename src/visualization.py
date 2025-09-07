import matplotlib.pyplot as plt
import numpy as np
import json

class SimulationVisualizer:
    """Visualization tools for OLB simulation results"""
    
    def __init__(self):
        self.colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    def plot_environment(self, digital_twin, placement, save_path="environment_plot.png"):
        """Plot the digital twin environment with assignments"""
        plt.figure(figsize=(12, 8))
        
        # Plot fog nodes
        for i, fog_node in enumerate(digital_twin.fog_nodes):
            plt.scatter(fog_node.coordinates[0], fog_node.coordinates[1], 
                       c=self.colors[i % len(self.colors)], s=200, marker='s', 
                       label=f'Fog Node {i}', alpha=0.7)
        
        # Plot sensors with assignment colors
        for node_id, sensors in placement.module_assignments.items():
            for sensor in sensors:
                plt.scatter(sensor.coordinates[0], sensor.coordinates[1], 
                           c=self.colors[node_id % len(self.colors)], s=100, marker='o', alpha=0.8)
                # Draw connection line
                fog_node = digital_twin.fog_nodes[node_id]
                plt.plot([sensor.coordinates[0], fog_node.coordinates[0]], 
                        [sensor.coordinates[1], fog_node.coordinates[1]], 
                        c=self.colors[node_id % len(self.colors)], alpha=0.3, linewidth=1)
        
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('OLB Digital Twin Environment - Sensor-Fog Node Assignments')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_performance_comparison(self, results_dict, save_path="performance_comparison.png"):
        """Compare performance metrics across algorithms"""
        algorithms = list(results_dict.keys())
        metrics = ['overall_latency', 'energy_consumption', 'network_usage']
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        for i, metric in enumerate(metrics):
            values = [results_dict[alg][metric] for alg in algorithms]
            axes[i].bar(algorithms, values, color=['blue', 'red', 'green'])
            axes[i].set_title(f'{metric.replace("_", " ").title()}')
            axes[i].set_ylabel('Value')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_latency_distribution(self, metrics, save_path="latency_distribution.png"):
        """Plot latency distribution across sensors"""
        assignments = metrics.detailed_assignments
        
        comm_latencies = [a['comm_latency'] for a in assignments]
        comp_latencies = [a['comp_latency'] for a in assignments]
        
        plt.figure(figsize=(10, 6))
        x = range(len(assignments))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], comm_latencies, width, label='Communication Latency', alpha=0.8)
        plt.bar([i + width/2 for i in x], comp_latencies, width, label='Computing Latency', alpha=0.8)
        
        plt.xlabel('Sensor ID')
        plt.ylabel('Latency')
        plt.title('Latency Distribution Across Sensors')
        plt.legend()
        plt.xticks(x, [f"S{a['sensor_id']}" for a in assignments])
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()