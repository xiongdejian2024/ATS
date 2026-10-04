# Vehicle Data Configuration

This directory contains the vehicle-specific configuration files for the SDK. It replaces the hardcoded configurations previously scattered across the codebase.

## Directory Structure

```
vehicle_data/
├── <vehicle_type>/           # e.g., mars1, venus
│   ├── <version>/            # e.g., v_3_0_0
│   │   ├── ecu_network.yaml  # Main ECU network topology and IDs
│   │   ├── ...               # Other signal/database files
│   └── ...
└── ...
```

## How to add a new vehicle type or version

1. Create a new directory under `vehicle_data` with the vehicle type name (e.g., `jupiter`).
2. Inside the vehicle type directory, create a version directory (e.g., `v_1_0_0`).
3. Add the required `ecu_network.yaml` file into the version directory.
   - The file should contain `ecu_map_id`, `positive_data`, `dtc_code_table`, etc., in the same format parsed by the `VehicleDataLoader`.
4. Add any CAN/LIN/FlexRay/CCP databases or JSONs required for the simulation.

The `VehicleRegistry` will automatically discover these directories when initialized.
