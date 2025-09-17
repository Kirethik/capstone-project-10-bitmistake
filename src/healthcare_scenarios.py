"""
Real-world healthcare scenarios with realistic IoT device parameters
"""

import random

from .devices import FogNodeDevice, SensorDevice


class HealthcareScenarios:
    """Healthcare-specific simulation scenarios"""

    @staticmethod
    def create_icu_scenario(environment, num_beds=10):
        """ICU monitoring with high-priority sensors"""
        sensors = []

        # ICU bed layout (2x5 grid)
        bed_positions = [
            (x * 300 + 500, y * 400 + 600) for x in range(5) for y in range(2)
        ]

        for i in range(num_beds):
            pos = bed_positions[i % len(bed_positions)]

            # Critical monitoring sensors per bed
            sensors.extend(
                [
                    # ECG Monitor - continuous high-frequency
                    SensorDevice(
                        device_id=i * 4,
                        coordinates=pos,
                        transmission_power=0.8,  # High power for reliability
                        average_flow_rate=10.0,  # 10 Hz sampling
                        flow_traffic_size=2.0,  # 2MB ECG data
                        average_flow_size=1500,  # Complex processing
                    ),
                    # Vital Signs Monitor
                    SensorDevice(
                        device_id=i * 4 + 1,
                        coordinates=(pos[0] + 50, pos[1]),
                        transmission_power=0.6,
                        average_flow_rate=1.0,  # 1 Hz vitals
                        flow_traffic_size=0.5,  # 0.5MB
                        average_flow_size=800,
                    ),
                    # Ventilator Sensor
                    SensorDevice(
                        device_id=i * 4 + 2,
                        coordinates=(pos[0], pos[1] + 50),
                        transmission_power=0.9,  # Critical device
                        average_flow_rate=5.0,  # 5 Hz breathing data
                        flow_traffic_size=1.0,
                        average_flow_size=1200,
                    ),
                    # IV Pump Monitor
                    SensorDevice(
                        device_id=i * 4 + 3,
                        coordinates=(pos[0] + 50, pos[1] + 50),
                        transmission_power=0.4,
                        average_flow_rate=0.2,  # Low frequency
                        flow_traffic_size=0.1,
                        average_flow_size=300,
                    ),
                ]
            )

        # Add sensors to environment
        for sensor in sensors:
            environment.add_sensor(sensor)

        # ICU fog nodes (high-performance)
        fog_nodes = [
            FogNodeDevice(0, (800, 800), 8000, 200, 5.0, 1e-11),  # Central ICU server
            FogNodeDevice(1, (1200, 800), 6000, 150, 2.4, 1e-11),  # Backup server
            FogNodeDevice(2, (1000, 1200), 5000, 100, 2.4, 1e-10),  # Edge processor
        ]

        for fog_node in fog_nodes:
            environment.add_fog_node(fog_node)

        return len(sensors)

    @staticmethod
    def create_ambulatory_scenario(environment, num_patients=15):
        """Ambulatory care with mobile patients"""
        sensors = []

        # Random patient positions (mobile)
        for i in range(num_patients):
            # Patients move around clinic area
            pos = (random.uniform(200, 2800), random.uniform(200, 1800))

            # Wearable health monitors
            sensors.extend(
                [
                    # Fitness Tracker
                    SensorDevice(
                        device_id=i * 3,
                        coordinates=pos,
                        transmission_power=0.2,  # Low power wearable
                        average_flow_rate=0.1,  # Periodic updates
                        flow_traffic_size=0.05,  # Small data packets
                        average_flow_size=200,
                    ),
                    # Blood Glucose Monitor
                    SensorDevice(
                        device_id=i * 3 + 1,
                        coordinates=(pos[0] + 10, pos[1] + 10),
                        transmission_power=0.3,
                        average_flow_rate=0.05,  # Few times per day
                        flow_traffic_size=0.02,
                        average_flow_size=150,
                    ),
                    # Smart Inhaler
                    SensorDevice(
                        device_id=i * 3 + 2,
                        coordinates=(pos[0] - 10, pos[1] + 10),
                        transmission_power=0.25,
                        average_flow_rate=0.02,  # Usage events
                        flow_traffic_size=0.1,
                        average_flow_size=400,
                    ),
                ]
            )

        for sensor in sensors:
            environment.add_sensor(sensor)

        # Distributed fog nodes for coverage
        fog_nodes = [
            FogNodeDevice(0, (600, 600), 3000, 80, 2.4, 1e-10),  # Clinic entrance
            FogNodeDevice(1, (1500, 600), 3500, 90, 2.4, 1e-10),  # Waiting area
            FogNodeDevice(2, (2400, 600), 3000, 80, 2.4, 1e-10),  # Consultation rooms
            FogNodeDevice(3, (600, 1400), 2500, 70, 2.4, 1e-10),  # Pharmacy
            FogNodeDevice(4, (1500, 1400), 4000, 100, 5.0, 1e-11),  # Main server
            FogNodeDevice(5, (2400, 1400), 2500, 70, 2.4, 1e-10),  # Lab area
        ]

        for fog_node in fog_nodes:
            environment.add_fog_node(fog_node)

        return len(sensors)

    @staticmethod
    def create_emergency_scenario(environment, num_ambulances=5):
        """Emergency response with mobile units"""
        sensors = []

        # Ambulance positions (moving towards hospital)
        ambulance_positions = [
            (500, 300),
            (1200, 400),
            (2000, 600),
            (800, 1600),
            (2200, 1400),
        ]

        for i in range(num_ambulances):
            pos = ambulance_positions[i % len(ambulance_positions)]

            # Emergency monitoring equipment
            sensors.extend(
                [
                    # Portable ECG
                    SensorDevice(
                        device_id=i * 5,
                        coordinates=pos,
                        transmission_power=1.0,  # Maximum power for emergency
                        average_flow_rate=20.0,  # High frequency monitoring
                        flow_traffic_size=3.0,  # Large data for accuracy
                        average_flow_size=2000,
                    ),
                    # Pulse Oximeter
                    SensorDevice(
                        device_id=i * 5 + 1,
                        coordinates=(pos[0] + 20, pos[1]),
                        transmission_power=0.8,
                        average_flow_rate=5.0,
                        flow_traffic_size=0.8,
                        average_flow_size=600,
                    ),
                    # Blood Pressure Monitor
                    SensorDevice(
                        device_id=i * 5 + 2,
                        coordinates=(pos[0], pos[1] + 20),
                        transmission_power=0.7,
                        average_flow_rate=1.0,  # Periodic measurements
                        flow_traffic_size=0.3,
                        average_flow_size=400,
                    ),
                    # Temperature Sensor
                    SensorDevice(
                        device_id=i * 5 + 3,
                        coordinates=(pos[0] + 20, pos[1] + 20),
                        transmission_power=0.3,
                        average_flow_rate=0.5,
                        flow_traffic_size=0.1,
                        average_flow_size=200,
                    ),
                    # GPS/Location Tracker
                    SensorDevice(
                        device_id=i * 5 + 4,
                        coordinates=(pos[0] + 10, pos[1] + 10),
                        transmission_power=0.5,
                        average_flow_rate=2.0,  # Real-time tracking
                        flow_traffic_size=0.05,
                        average_flow_size=100,
                    ),
                ]
            )

        for sensor in sensors:
            environment.add_sensor(sensor)

        # Emergency response fog infrastructure
        fog_nodes = [
            FogNodeDevice(
                0, (1500, 1000), 10000, 300, 5.0, 1e-12
            ),  # Hospital main server
            FogNodeDevice(1, (800, 800), 6000, 200, 5.0, 1e-11),  # Emergency dispatch
            FogNodeDevice(2, (2200, 800), 6000, 200, 5.0, 1e-11),  # Backup dispatch
            FogNodeDevice(3, (1500, 400), 4000, 150, 2.4, 1e-10),  # Mobile relay
            FogNodeDevice(4, (1500, 1600), 4000, 150, 2.4, 1e-10),  # Mobile relay
        ]

        for fog_node in fog_nodes:
            environment.add_fog_node(fog_node)

        return len(sensors)

    @staticmethod
    def get_scenario_info():
        """Get information about available scenarios"""
        return {
            "icu": {
                "name": "Intensive Care Unit",
                "description": "High-priority continuous monitoring with ECG, vitals, ventilators",
                "sensors_per_bed": 4,
                "typical_beds": 10,
                "fog_nodes": 3,
                "characteristics": [
                    "High frequency",
                    "Critical reliability",
                    "Low latency",
                ],
            },
            "ambulatory": {
                "name": "Ambulatory Care",
                "description": "Mobile patients with wearable health monitors",
                "sensors_per_patient": 3,
                "typical_patients": 15,
                "fog_nodes": 6,
                "characteristics": ["Low power", "Periodic updates", "Wide coverage"],
            },
            "emergency": {
                "name": "Emergency Response",
                "description": "Mobile ambulances with emergency monitoring equipment",
                "sensors_per_ambulance": 5,
                "typical_ambulances": 5,
                "fog_nodes": 5,
                "characteristics": ["Maximum reliability", "Real-time", "Mobile units"],
            },
        }
