# ecu_simulator 数据更新维护

更新整车信号（arxml）
1. 将全量的 xxx.arxml 放入 sdk/data/arxml_file/  中，如 SDB22R02_220507_Release.arxml；dataid文件也放入其中，如"SDB22R04_FIPV065_DataIDList_220914_1708.xlsx"；
2. cls_path 为生成can_lin_fr_cls的文件路径如"sdk/data/mars1/can_lin_fr_cls/v_0_5_5" ；
3. work dir ： ecu_simulator/           cmd : python3 tools/arxml_tool/all_arxml_reader.py --arxml="SDB22R02_220507_Release.arxml" --dataid="SDB22R04_FIPV065_DataIDList_220914_1708.xlsx" --cls_path="sdk/data/mars1/can_lin_fr_cls/v_0_5_5"  
4. work dir ： ecu_simulator/           cmd : python3 tools/communication/generate_init_pdu_and_tx_cyc_json.py --cls_path="sdk/data/mars1/can_lin_fr_cls/v_0_5_5"
5. work dir ： ecu_simulator/           cmd : python3 tools/s2s_mcu_sim/signal2service_local.py --cls_path="sdk/data/mars1/can_lin_fr_cls/v_0_5_5"  --json_path="./tools/s2s_mcu_sim/config/sample.json"        若需要可以用此条命令本地测试验证
6. 删掉全量的 xxx.arxml 文件