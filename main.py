import os
import sys
import json
import logging
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.environment import DigitalTwinEnvironment
from src.olb_algorithm import OLBPlacement
from src.yafs_integration import create_smart_healthcare_application, create_yafs_topology
from src.metrics import PerformanceMetrics
from src.utils import create_placement_json, save_results, SimulationConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('olb_simulation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Main simulation entry point"""
    logger.info("Starting OLB Simulation with YAFS Framework")
    
    # Initialize configuration
    config = SimulationConfig()
    
    # Create digital twin environment
    logger.info("Creating digital twin environment...")
    environment = DigitalTwinEnvironment(
        width=config.environment_width,
        height=config.environment_height
    )
    environment.initialize_sensors(
        num_sensors=config.num_sensors,
        seed=config.random_seed
    )
    environment.initialize_fog_nodes(
        num_fog_nodes=config.num_fog_nodes,
        seed=config.random_seed
    )
    
    # Create YAFS application and topology
    logger.info("Setting up YAFS application and topology...")
    app = create_smart_healthcare_application(environment)
    topology = create_yafs_topology(environment)
    
    # Create placement JSON for YAFS
    logger.info("Creating placement configuration...")
    placement_json = create_placement_json()
    
    # Initialize OLB placement algorithm
    logger.info("Initializing OLB placement algorithm...")
    olb_placement = OLBPlacement(
        name="OLB_Healthcare",
        json_file=placement_json,
        digital_twin=environment
    )
    
    try:
        # Initialize YAFS simulator
        from yafs.core import Sim
        
        logger.info("Starting YAFS simulation...")
        
        # Create simulator instance
        s = Sim(topology, default_results_path="results/")
        
        # Deploy application (YAFS expects: app, placement, population)
        from yafs.population import Population
        population = Population(name="HealthcareSensors")
        s.deploy_app(app, olb_placement, population)
        
        # Run simulation
        s.run(until=config.simulation_time)
        
        # Get simulation time for metadata
        simulation_time = config.simulation_time
        
        # Collect and save results
        logger.info("Collecting simulation results...")
        
        # Initialize performance metrics
        metrics = PerformanceMetrics()
        
        # Use the correct metrics collection method
        metrics.collect_metrics(environment, olb_placement)
        
        # Generate performance report
        report = metrics.generate_report()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            'simulation_config': config.to_dict(),
            'environment_info': {
                'num_sensors': len(environment.sensors),
                'num_fog_nodes': len(environment.fog_nodes),
                'sensor_coordinates': [s.coordinates for s in environment.sensors],
                'fog_node_coordinates': [f.coordinates for f in environment.fog_nodes]
            },
            'performance_metrics': report,
            'simulation_metadata': {
                'timestamp': timestamp,
                'simulation_time': simulation_time,
                'framework': 'YAFS 1.0',
                'algorithm': 'Optimised Load Balancing (OLB)'
            }
        }
        
        # Save results to JSON file
        results_filename = f"olb_simulation_results_{timestamp}.json"
        with open(results_filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Also save text report
        save_results(metrics, olb_placement, f"olb_simulation_report_{timestamp}.txt")
        
        logger.info("Simulation completed successfully!")
        logger.info(f"Results saved with timestamp: {timestamp}")
        
        # Print summary
        print("\n" + "="*60)
        print("OLB SIMULATION SUMMARY")
        print("="*60)
        print(f"Simulation Time: {simulation_time} time units")
        print(f"Sensors: {len(environment.sensors)}")
        print(f"Fog Nodes: {len(environment.fog_nodes)}")
        print(f"Framework: YAFS 1.0")
        print(f"Algorithm: Optimised Load Balancing (OLB)")
        print("\nPerformance Metrics:")
        if 'average_latency' in report:
            print(f"  Average Latency: {report['average_latency']:.3f} ms")
        if 'average_energy' in report:
            print(f"  Average Energy: {report['average_energy']:.3f} J")
        if 'total_placements' in report:
            print(f"  Total Placements: {report['total_placements']}")
        print(f"Results saved to: olb_simulation_results_{timestamp}.json")
        print("="*60)
        
    except ImportError as e:
        logger.error(f"YAFS framework not properly installed: {e}")
        logger.error("Please install YAFS using: pip install yafs")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Run main simulation
    main()
