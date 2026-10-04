Usage for tools/scripts_generator/can+lin_routing_test_generator.py:
-------------------------------------------------------------------

cd ~/compass/tools/scripts_generator

python can+lin_routing_test_generator.py

can_routing/*.py & lin_routing/*.py files will be generated for all versions
of the .dbc and .ldf files for ES6 & ES8 that are present in:

    sdk/dut/cgw/pcan/dbc_ldf_config.yaml

This is done by calling:

    CgwCan.call_car_platform_dut_ver_bus_type_partial_paths_parent_dir_handler(
        generate_can_protections_test_file_helper)

This calls:

    CgwCan._get_dbc_ldf_config_helper()

to do the actual reading of dbc_ldf_config.yaml, then calls:

    generate_can_protections_test_file_helper()

in a loop to for each (car_platform, bus_file_version#)-pair read from dbc_ldf_config.yaml.
