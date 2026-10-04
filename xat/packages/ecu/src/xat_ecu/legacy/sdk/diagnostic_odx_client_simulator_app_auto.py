#!/usr/bin/python3

# Automatic generation by ecu_simulator/tools/odx/diagnostic_auto_generator.py


class Diagnostic_Odx_Client_Sim_App_Auto:
   def __init__(self):
       pass

   def rq_odx_ecu_variant_version_number_read_ecu_diagnostic_database_version_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x9e])

   def rq_ecu_identification_read_vehicle_manufacture_hardware_part_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x10])

   def rq_ecu_identification_read_vehicle_manufacture_hardware_baseline_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x11])

   def rq_ecu_identification_read_vehicle_manufacturer_software_part_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x18])

   def rq_ecu_identification_read_vehicle_manufacture_software_baseline_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x19])

   def rq_ecu_identification_read_vehicle_manufacturer_calibration_part_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x30])

   def rq_ecu_identification_read_vehicle_manufacture_calibration_baseline_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x31])

   def rq_ecu_identification_read_read_programming_fingerprint_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x5b])

   def rq_ecu_identification_read_read_active_diagnostic_session_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x86])

   def rq_ecu_identification_read_vehicle_manufacturer_spare_part_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x87])

   def rq_ecu_identification_read_ecu_diagnostic_database_version_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x9e])

   def rq_ecu_identification_read_bootloader_version_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x50])

   def rq_ecu_identification_read_system_supplier_identifier_data_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x8a])

   def rq_ecu_identification_read_ecu_manufacturing_date_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x8b])

   def rq_ecu_identification_read_ecu_serial_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x8c])

   def rq_ecu_identification_read_vehicle_identification_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x90])

   def rq_ecu_identification_read_system_name_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x97])

   def rq_ecu_identification_read_repair_shop_fingerprint_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x98])

   def rq_ecu_identification_read_ecu_programming_date_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x99])

   def rq_ecu_identification_read_system_supplier_hardware_part_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x92])

   def rq_ecu_identification_read_system_supplier_hardware_version_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x93])

   def rq_ecu_identification_read_system_supplier_software_part_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x94])

   def rq_ecu_identification_read_system_supplier_software_version_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x95])

   def rq_ecu_identification_read_system_supplier_calibration_version_number_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x51])

   def rq_ecu_identification_read_configuration_fingerprint_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x5c])

   def rq_ecu_identification_read_ecu_configuration_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x1])

   def rq_ecu_identification_read_vehicle_configuration_auto(self):
       self.client_sim.send_data([0x22, 0xf1, 0x0])

   def rq_ecu_identification_read_reprogramming_attempt_counter_auto(self):
       self.client_sim.send_data([0x22, 0xf0, 0x10])

   def rq_stored_data_read_backup_battery_boost_control_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x31])

   def rq_stored_data_read_ecall_control_state_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x30])

   def rq_stored_data_read_vehicle_location_information_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x1])

   def rq_stored_data_read_backup_battery_healthy_status_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x0])

   def rq_stored_data_read_imei_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x2])

   def rq_stored_data_read_iccid_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x3])

   def rq_stored_data_read_sim_card_status_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x4])

   def rq_stored_data_read_sim_card_airplane_mode_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x5])

   def rq_stored_data_read_cellular_network_signal_strength_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x6])

   def rq_stored_data_read_cellular_network_signal_level_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x7])

   def rq_stored_data_read_radio_technology_type_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x8])

   def rq_stored_data_read_backup_battery_temp_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x9])

   def rq_stored_data_read_ecall_official_number_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0xa])

   def rq_stored_data_read_reprogramming_result_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0xc])

   def rq_stored_data_read_imu_calibration_confidence_percent_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0xf])

   def rq_stored_data_read_ecall_enable_disable_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x10])

   def rq_stored_data_read_automatic_ecall_allowed_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x11])

   def rq_stored_data_read_manual_ecall_cancellation_allowed_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x12])

   def rq_stored_data_read_ecall_test_number_1_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x13])

   def rq_stored_data_read_dial_test_number_allowed_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x14])

   def rq_stored_data_read_test_mode_call_allowed_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x15])

   def rq_stored_data_read_ecall_max_attempts_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x16])

   def rq_stored_data_read_ecall_already_attempted_times_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x17])

   def rq_stored_data_read_ble_mac_address_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x19])

   def rq_stored_data_read_system_supplier_ecu_software_version_number_for_ecall_certificat_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x21])

   def rq_stored_data_read_system_supplier_ecu_hardware_version_number_for_ecall_certificat_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x20])

   def rq_stored_data_read_ble_version_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x1d])

   def rq_stored_data_read_test_mcc_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x1c])

   def rq_stored_data_read_test_mnc_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x1b])

   def rq_stored_data_read_mnc_mcc_allowed_auto(self):
       self.client_sim.send_data([0x22, 0x49, 0x1a])

   def rq_ecu_identification_write_write_programming_fingerprint_auto(self):
       self.client_sim.send_data([0x2e, 0xf1, 0x5a])

   def rq_ecu_identification_write_vehicle_manufacturer_spare_part_number_auto(self):
       self.client_sim.send_data([0x2e, 0xf1, 0x87])

   def rq_ecu_identification_write_vehicle_identification_number_auto(self):
       self.client_sim.send_data([0x2e, 0xf1, 0x90])

   def rq_ecu_identification_write_repair_shop_fingerprint_auto(self):
       self.client_sim.send_data([0x2e, 0xf1, 0x98])

   def rq_ecu_identification_write_configuration_fingerprint_auto(self):
       self.client_sim.send_data([0x2e, 0xf1, 0x5c])

   def rq_ecu_identification_write_ecu_configuration_auto(self):
       self.client_sim.send_data([0x2e, 0xf1, 0x1])

   def rq_ecu_identification_write_vehicle_configuration_auto(self):
       self.client_sim.send_data([0x2e, 0xf1, 0x0])

   def rq_stored_data_write_ecall_official_number_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0xa])

   def rq_stored_data_write_ecall_enable_disable_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x10])

   def rq_stored_data_write_automatic_ecall_allowed_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x11])

   def rq_stored_data_write_manual_ecall_cancellation_allowed_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x12])

   def rq_stored_data_write_ecall_test_number_1_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x13])

   def rq_stored_data_write_dial_test_number_allowed_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x14])

   def rq_stored_data_write_test_mode_call_allowed_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x15])

   def rq_stored_data_write_ecall_max_attempts_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x16])

   def rq_stored_data_write_mnc_mcc_allowed_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x1a])

   def rq_stored_data_write_test_mnc_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x1b])

   def rq_stored_data_write_test_mcc_auto(self):
       self.client_sim.send_data([0x2e, 0x49, 0x1c])

