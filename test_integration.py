#!/usr/bin/env python3

import os
import sys
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_imports():
    print("Testing imports...")
    try:
        from src import (DigitalTwinEnvironment, DistancePlacement,
                         HealthcareScenarios, OLBPlacement, PerformanceMetrics,
                         RandomPlacement, SimulationConfig,
                         create_smart_healthcare_application,
                         create_yafs_topology)

        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_environment():
    print("\nTesting environment creation...")
    try:
        from src import DigitalTwinEnvironment

        env = DigitalTwinEnvironment(1000, 1000)
        env.initialize_sensors(5, 42)
        env.initialize_fog_nodes(3, 42)

        print(
            f"✓ Environment created with {len(env.sensors)} sensors and {len(env.fog_nodes)} fog nodes"
        )
        return True, env
    except Exception as e:
        print(f"✗ Environment creation failed: {e}")
        traceback.print_exc()
        return False, None


def test_yafs_integration(env):
    print("\nTesting YAFS integration...")
    try:
        from src import (create_smart_healthcare_application,
                         create_yafs_topology)

        app = create_smart_healthcare_application(env)
        topology = create_yafs_topology(env)

        print(f"✓ YAFS application created with {len(app.modules)} modules")
        print(f"✓ YAFS topology created with {len(topology.G.nodes)} nodes")
        return True, app, topology
    except Exception as e:
        print(f"✗ YAFS integration failed: {e}")
        traceback.print_exc()
        return False, None, None


def test_olb_algorithm(env):
    print("\nTesting OLB algorithm...")
    try:
        from src import OLBPlacement, create_placement_json

        placement_json = create_placement_json(".")
        olb = OLBPlacement("TestOLB", placement_json, env)

        print("✓ OLB placement algorithm initialized")
        return True, olb
    except Exception as e:
        print(f"✗ OLB algorithm failed: {e}")
        traceback.print_exc()
        return False, None


def test_metrics(env, placement):
    print("\nTesting metrics collection...")
    try:
        from src import PerformanceMetrics

        placement.module_assignments = {0: env.sensors[:2], 1: env.sensors[2:]}

        metrics = PerformanceMetrics()
        metrics.collect_metrics(env, placement, "TestOLB")

        print(f"✓ Metrics collected: latency={metrics.overall_latency:.2f}")
        return True
    except Exception as e:
        print(f"✗ Metrics collection failed: {e}")
        traceback.print_exc()
        return False


def test_healthcare_scenarios():
    print("\nTesting healthcare scenarios...")
    try:
        from src import DigitalTwinEnvironment, HealthcareScenarios

        env = DigitalTwinEnvironment(3000, 2000)
        num_sensors = HealthcareScenarios.create_icu_scenario(env, 3)

        print(f"✓ ICU scenario created with {num_sensors} sensors")
        return True
    except Exception as e:
        print(f"✗ Healthcare scenarios failed: {e}")
        traceback.print_exc()
        return False


def main():
    print("=== OLB CODEBASE INTEGRATION TEST ===\n")

    os.makedirs("results", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    success_count = 0
    total_tests = 6

    if test_imports():
        success_count += 1

    success, env = test_environment()
    if success:
        success_count += 1

    if env:
        success, app, topology = test_yafs_integration(env)
        if success:
            success_count += 1

        success, placement = test_olb_algorithm(env)
        if success:
            success_count += 1

        if placement and test_metrics(env, placement):
            success_count += 1

    if test_healthcare_scenarios():
        success_count += 1

    print(f"\n=== TEST RESULTS ===")
    print(f"Passed: {success_count}/{total_tests}")

    if success_count == total_tests:
        print("✓ All tests passed! Codebase is properly integrated.")
        return True
    else:
        print("✗ Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
