# Optimised Load Balancing (OLB) Simulation for Smart Healthcare IoT

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/framework-YAFS-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A modularized, high-fidelity simulation of the **Optimised Load Balancing (OLB)** algorithm for IoT-enabled smart healthcare systems, built on the **YAFS (Yet Another Fog Simulator)** framework.

This project provides a complete digital twin to model, simulate, and analyze the performance of load balancing strategies in a fog computing environment.

---

## Table of Contents

- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Core Concepts: The OLB Algorithm](#core-concepts-the-olb-algorithm)
  - [Communication Latency Analysis](#communication-latency-analysis-l_mj)
  - [Computing Latency Analysis](#computing-latency-analysis-l_pj)
- [Simulation Output](#simulation-output)
- [License](#license)

---

## About The Project

This simulation implements the mathematical model of the OLB algorithm within a custom YAFS placement policy. It constructs a digital twin of a smart healthcare environment, complete with patient sensors (Tier 1) and fog computing nodes (Tier 2), to evaluate how well the OLB algorithm distributes computational workloads.

**Key Features:**
- **YAFS Integration**: Seamlessly integrated with the YAFS 1.0 simulation framework.
- **Digital Twin Environment**: Simulates a realistic IoT healthcare environment with geospatial awareness.
- **OLB Algorithm**: Implements the complete mathematical model for optimised load balancing.
- **Performance Metrics**: Provides comprehensive analysis of latency, energy consumption, and network usage.
- **Modular Design**: Clean, maintainable, and extensible code structure.

**Built With:**
*   [Python 3.8+](https://www.python.org/)
*   [YAFS (Yet Another Fog Simulator)](https://yafs.readthedocs.io/)
*   [NetworkX](https://networkx.org/)
*   [NumPy](https://numpy.org/)
*   [Matplotlib](https://matplotlib.org/)

---

## Getting Started

Follow these steps to get the simulation running on your local machine.

### Prerequisites

Ensure you have Python 3.8 or higher installed. You can check your version with:
```sh
python --version
```
### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/23CSE362-edge-computing-2025-26-odd/capstone-project-10-bitmistake.git
    cd capstone-project-10-bitmistake
    ```
2.  **Install the YAFS framework:**
    ```sh
    pip install yafs
    ```
3.  **Install additional dependencies:**
    ```sh
    pip install networkx numpy matplotlib
    ```
---

## Usage

To run the complete simulation, execute the main script from the root directory:
```sh
python main.py
```
The script will:
1.  Initialize the digital twin environment.
2.  Set up the YAFS topology and application.
3.  Apply the OLB placement algorithm to assign sensor workloads to fog nodes.
4.  Run the simulation for the configured duration.
5.  Generate and save performance reports in the `results/` and `data/` directories.

**Configuration:**
You can modify simulation parameters (e.g., number of sensors, simulation time) in the `src/utils.py` file within the `SimulationConfig` class.

---

## Project Structure

```
.
├── main.py                 # Main simulation entry point
├── config/                 # Configuration files for experiments and placement
├── data/                   # Raw simulation results (JSON)
├── docs/                   # Project documentation
├── experiments/            # Scripts for evaluation and plotting
├── plots/                  # Generated plots and visualizations
├── reports/                # Formatted simulation reports
├── src/                    # Source code
│   ├── __init__.py         # Package initializer
│   ├── comparison_algorithms.py # Additional load balancing algorithms
│   ├── devices.py          # Sensor and Fog Node models
│   ├── environment.py      # Digital Twin Environment setup
│   ├── healthcare_scenarios.py # Healthcare-specific simulation scenarios
│   ├── metrics.py          # Performance metrics collection
│   ├── metrics_definitions.py # Definitions for custom metrics
│   ├── olb_algorithm.py    # Core OLB algorithm implementation
│   ├── utils.py            # Configuration and utility functions
│   ├── visualization.py    # Plotting and visualization functions
│   ├── workload_models.py  # Workload generation models
│   └── yafs_integration.py # YAFS-specific integration code
└── README.md               # This file
```

---

## Core Concepts: The OLB Algorithm

The OLB algorithm dynamically assigns sensor workloads to the most optimal fog node by calculating a total latency score. The node with the minimum score is selected.

### Communication Latency Analysis (L_m(j))

This measures the time it takes to transmit data from a sensor to a fog node. It is calculated based on:
1.  **Distance**: Euclidean distance between the sensor and the fog node.
2.  **Channel Gain & SNR**: Signal strength and quality over the wireless channel.
3.  **Device Capacity**: The maximum data rate the fog node can handle from the sensor.
4.  **Total Traffic Load**: The cumulative traffic from all sensors assigned to the node.

### Computing Latency Analysis (L_p(j))

This measures the time it takes for a fog node to process the received data. It is calculated based on:
1.  **Individual Computing Load**: The computational demand of a single sensor's workload.
2.  **Total Computing Load**: The cumulative computational demand from all sensors assigned to the node.

The final placement decision is made by selecting the fog node `j` that minimizes `Total Latency = L_m(j) + L_p(j)`.

---

## Mathematical Model

The OLB algorithm implements:
- Communication latency calculation
- Computing latency estimation
- Energy consumption modeling
- Load balancing optimization

## Framework Integration

This implementation uses:
- **YAFS**: Core simulation framework
- **NetworkX**: Graph-based topology modeling
- **Digital Twin**: IoT environment simulation
- **OLB Placement Policy**: Custom YAFS placement algorithm

## Implementation Summary

### Phase 1: Environment Construction - The Digital Twin ✅
- **Geospatial Environment**: Created a 2D coordinate system of 3000x2000 units
- **IoT Layer Entities (Tier 1)**: Implemented 10 sensor devices with all required OLB parameters:
  - `coordinates`: (x, y) position tuple
  - `transmissionPower`: P(x) signal strength in Watts
  - `averageFlowRate`: fl(x) data generation frequency in Hz
  - `flowTrafficSize`: l(x) network packet size in megabits
  - `averageFlowSize`: ν(x) computational workload in MI
- **Fog Layer Entities (Tier 2)**: Implemented 6 fog nodes with parameters:
  - `coordinates`: (x, y) static position tuple
  - `processingPower`: Cj CPU capacity in MIPS
  - `bandwidth`: BWj network interface capacity in MHz
  - `carrierFrequency`: operational frequency in GHz
  - `noisePower`: σ² ambient noise level in Watts

### Phase 2: Application Architecture Definition ✅
- **YAFS Application**: Properly integrated with YAFS framework
- **Application Modules**: Defined three module types:
  - `Client_Module`: SOURCE type, handles sensor data ingestion
  - `Processing_Module`: MODULE type, performs data processing
  - `Storage_Module`: SINK type, stores processed results
- **Data Flow Topology**: Implemented DAG structure in YAFS:
  - Sensor → Client_Module → Processing_Module → Storage_Module

### Phase 3: OLB Algorithm Implementation ✅
Implemented complete mathematical model within YAFS Placement policy:

#### Communication Latency Analysis (L_m(j))
1. **Distance Calculation**: Euclidean distance between sensor and fog node
2. **Channel Gain**: `g(x) = 10 * log10(λ²/(4πd)²)` where λ = c/f
3. **Signal-to-Noise Ratio**: `SNR(x) = (P(x) * g(x))/σ²`
4. **Device Capacity**: `cj(x) = BWj * (1 + SNR(x))`
5. **Individual Traffic Load**: `eaj(x) = (fl(x) * l(x))/cj(x)`
6. **Total Traffic Load**: `TLj = Σ eaj(x)` for all assigned modules
7. **Communication Latency**: `L_m(j) = TLj/(1 - TLj)`

#### Computing Latency Analysis (L_p(j))
1. **Individual Computing Load**: `ebj(x) = (fl(x) * ν(x))/Cj`
2. **Total Computing Load**: `CLj = Σ ebj(x)` for all assigned modules
3. **Computing Latency**: `L_p(j) = CLj/(1 - CLj)`

#### Final Score Calculation
- **Total Latency**: `L_total = L_m(j) + L_p(j)`
- **Optimal Selection**: Node with minimum L_total score

### Phase 4: YAFS Execution and Performance Reporting ✅
Full YAFS simulation execution with comprehensive KPI collection:

#### Key Performance Indicators
- **Overall Latency (L)**: 4.1962 - Sum of all communication and computing latencies
- **Network Usage (Nusage)**: 5.0760 MB/s - Total data transmission volume
- **Execution Time (Te)**: 0.4196 ms - Average end-to-end task time
- **Energy Consumption (Etotal)**: 21.5153 W - Total device energy consumption
- **Cost of Execution (Ce)**: 1.1037 - Composite cost metric

## Technical Implementation Details

### Core Classes
1. **SensorDevice**: Encapsulates Tier 1 IoT sensor parameters
2. **FogNodeDevice**: Encapsulates Tier 2 fog node parameters
3. **OLBPlacement**: Custom YAFS Placement policy implementing OLB algorithm
4. **DigitalTwinEnvironment**: Manages the complete simulation environment

### YAFS Integration
- **Proper YAFS Topology**: NetworkX-based topology with fog nodes, proxy, and cloud
- **YAFS Application**: Correctly structured modules and message flows
- **YAFS Placement**: Custom placement policy integrating OLB mathematical model
- **YAFS Simulation**: Full simulation execution with module deployment

### Mathematical Model Validation
- All formulas implemented exactly as specified
- Proper handling of edge cases (division by zero, overflow)
- Load balancing ensures no node exceeds 99% utilization
- Distance-based channel gain calculations using speed of light constant

### Results Analysis
The YAFS simulation successfully assigned 10 sensors across 6 fog nodes:
- **Intelligent Load Distribution**: Fog Node 5 (3 sensors), Fog Nodes 0&4 (2 sensors each), others (1 sensor each)
- **Latency Optimization**: Total latency 4.1962 with Communication (0.1045) + Computing (4.0917)
- **Real-time Decision Making**: Each sensor evaluated against all fog nodes with dynamic load consideration

---

## Simulation Output

The simulation generates several output files:
- **`data/olb_simulation_results.json`**: A JSON file containing raw metrics and configuration details.
- **`results/reports/olb_simulation_report.txt`**: A human-readable report summarizing the performance and module assignments.
- **`results/plots/`**: Visualizations comparing algorithm performance (if generated via experiment scripts).

---

## License

Distributed under the MIT License.
