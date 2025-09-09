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
        logging.FileHandler('logs/olb_simulation.log')
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
    placement_json = create_placement_json('config')
    
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
                'simulation_time': simulation_time,
                'framework': 'YAFS 1.0',
                'algorithm': 'Optimised Load Balancing (OLB)'
            }
        }
        
        # Save results to JSON file
        results_filename = f"data/olb_simulation_results.json"
        with open(results_filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Also save text report
        save_results(metrics, olb_placement, f"reports/olb_simulation_report.txt")
        
        logger.info("Simulation completed successfully!")
        
        # Print summary
        # Log summary instead of printing
        logger.info("OLB SIMULATION SUMMARY")
        logger.info(f"Simulation Time: {simulation_time} time units")
        logger.info(f"Sensors: {len(environment.sensors)}")
        logger.info(f"Fog Nodes: {len(environment.fog_nodes)}")
        logger.info(f"Framework: YAFS 1.0")
        logger.info(f"Algorithm: Optimised Load Balancing (OLB)")
        logger.info(f"Results saved to: data/olb_simulation_results.json")
        
    except ImportError as e:
        logger.error(f"YAFS framework not properly installed: {e}")
        logger.error("Please install YAFS using: pip install yafs")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs("results", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Run main simulation
    main()
