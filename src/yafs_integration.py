import networkx as nx
from yafs import Application, Message, Topology


def create_smart_healthcare_application(digital_twin):
    """
    Phase 2: Application Architecture Definition
    Creates the YAFS application with proper DAG structure
    """
    print("Creating Smart Healthcare Application...")
    
    app = Application(name="SmartHealthcare")
    
    # Define application modules as per YAFS format
    modules = []
    
    # Task 2.1: Define Application Modules for each sensor
    for sensor in digital_twin.sensors:
        # Client Module (Source)
        client_module = f"Client_Module_Sensor_{sensor.device_id}"
        modules.append({
            client_module: {
                "Type": Application.TYPE_SOURCE,
                "RAM": 10,
                "IPT": 1000
            }
        })
        
        # Processing Module
        processing_module = f"Processing_Module_Sensor_{sensor.device_id}"
        modules.append({
            processing_module: {
                "Type": Application.TYPE_MODULE,
                "RAM": 50,
                "IPT": int(sensor.averageFlowSize)  # Use sensor's processing requirement
            }
        })
    
    # Storage Module (shared, sink)
    modules.append({
        "Storage_Module": {
            "Type": Application.TYPE_SINK,
            "RAM": 100,
            "IPT": 500
        }
    })
    
    # Set modules in YAFS application
    app.set_modules(modules)
    
    # Task 2.2: Define Application Edges and Data Flow
    messages = []
    
    for sensor in digital_twin.sensors:
        client_module = f"Client_Module_Sensor_{sensor.device_id}"
        processing_module = f"Processing_Module_Sensor_{sensor.device_id}"
        
        # Sensor data message: Client -> Processing
        sensor_msg = Message(
            name=f"sensor_msg_{sensor.device_id}",
            src=client_module,
            dst=processing_module,
            instructions=int(sensor.averageFlowSize),
            bytes=int(sensor.flowTrafficSize * 1000000)  # Convert MB to bytes
        )
        messages.append(sensor_msg)
        
        # Result message: Processing -> Storage
        result_msg = Message(
            name=f"result_msg_{sensor.device_id}",
            src=processing_module,
            dst="Storage_Module",
            instructions=100,
            bytes=1000
        )
        messages.append(result_msg)
    
    # Add source messages (from sensors)
    for sensor in digital_twin.sensors:
        client_module = f"Client_Module_Sensor_{sensor.device_id}"
        sensor_msg = f"sensor_msg_{sensor.device_id}"
        
        # Add source message with distribution
        msg = Message(
            name=sensor_msg,
            src=client_module,
            dst=f"Processing_Module_Sensor_{sensor.device_id}",
            instructions=int(sensor.averageFlowSize),
            bytes=int(sensor.flowTrafficSize * 1000000)
        )
        app.add_source_messages(msg)
    
    # Add service modules (processing logic)
    for sensor in digital_twin.sensors:
        processing_module = f"Processing_Module_Sensor_{sensor.device_id}"
        sensor_msg = f"sensor_msg_{sensor.device_id}"
        result_msg = f"result_msg_{sensor.device_id}"
        
        app.add_service_module(processing_module, sensor_msg, message_out=[result_msg])
    
    # Storage module handles all result messages
    for sensor in digital_twin.sensors:
        result_msg = f"result_msg_{sensor.device_id}"
        app.add_service_module("Storage_Module", result_msg, message_out=[])
    
    print(f"Application created with {len(modules)} modules")
    return app


def create_yafs_topology(digital_twin):
    """
    Create YAFS topology from digital twin environment
    Task 1.4: Model Tier 3 - Cloud Layer Entities
    """
    print("Creating YAFS topology...")
    
    # Create NetworkX graph first
    G = nx.Graph()
    
    # Add fog nodes (Tier 2)
    fog_node_names = []
    for i, fog_node in enumerate(digital_twin.fog_nodes):
        node_name = f"fog_{i}"
        fog_node_names.append(node_name)
    
    # Add cloud and proxy nodes (Tier 3)
    fog_node_names.extend(["proxy", "cloud"])
    
    # Add all nodes to NetworkX graph
    G.add_nodes_from(fog_node_names)
    
    # Add edges (connections) to NetworkX graph first
    # Fog nodes connect to proxy (4ms latency)
    for i in range(len(digital_twin.fog_nodes)):
        G.add_edge(f"fog_{i}", "proxy")
    
    # Proxy connects to cloud (100ms latency)
    G.add_edge("proxy", "cloud")
    
    # Create YAFS topology from NetworkX graph
    topology = Topology()
    topology.create_topology_from_graph(G)
    
    # Set node attributes using YAFS methods
    for i, fog_node in enumerate(digital_twin.fog_nodes):
        node_name = f"fog_{i}"
        # YAFS uses networkx graph internally
        topology.G.nodes[node_name]["IPT"] = int(fog_node.processingPower)
        topology.G.nodes[node_name]["RAM"] = 1000
        topology.G.nodes[node_name]["STORAGE"] = 10000
    
    # Set cloud and proxy attributes
    topology.G.nodes["proxy"]["IPT"] = 10000
    topology.G.nodes["proxy"]["RAM"] = 2000
    topology.G.nodes["proxy"]["STORAGE"] = 50000
    
    topology.G.nodes["cloud"]["IPT"] = 50000
    topology.G.nodes["cloud"]["RAM"] = 10000
    topology.G.nodes["cloud"]["STORAGE"] = 100000
    
    # Set edge attributes for latency and bandwidth
    # Fog nodes connect to proxy (4ms latency)
    for i in range(len(digital_twin.fog_nodes)):
        topology.G.edges[f"fog_{i}", "proxy"]["BW"] = 100
        topology.G.edges[f"fog_{i}", "proxy"]["PR"] = 4  # 4ms propagation delay
    
    # Proxy connects to cloud (100ms latency)
    topology.G.edges["proxy", "cloud"]["BW"] = 1000
    topology.G.edges["proxy", "cloud"]["PR"] = 100  # 100ms propagation delay
    
    print(f"Topology created with {len(fog_node_names)} nodes")
    return topology
