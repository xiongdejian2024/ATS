import xlrd
import json
import json
import os

def generate_json_from_excel(excel_path=''):
    excel_data = xlrd.open_workbook(excel_path)
    case_content = []  # 存放数据
    step_descirbe= []  #步骤描述
    except_result = [] #预期结果
    case_name= '' #用例名字
    case_module ='' #用例模块
    title='' #标签
    precondition='' #前置条件
    comment='' #备注
    case_grade='' #用例等级
    JamaReqID='' #jamaid
    id='' #ms id
    level='' #用例等级
    below_empty=False
    now_empty=False

    # 根据uds用例的excel文件生成对应的用例的json文件以及内容字典
    # 打开Excel文件
    # 读取第一个工作表
    table = excel_data.sheets()[0]
    # 统计行数
    rows = table.nrows
    print(f'rows nums={rows}')
    for i in range(1,rows):
        values = table.row_values(i)
        id=values[0]
        if id:
            pass
            case_name=values[1]
            case_module=values[2]
            precondition = values[3]
            comment = values[4]
            title=values[8]
            JamaReqID=values[11]
            level=values[15]        
            case_content.append(
                        (
                            {
                                "ID":id,
                                "用例名称": case_name,
                                "所属模块": case_module,
                                "标签": title,
                                "前置条件": precondition,
                                "备注": comment,
                                "用例等级": level,
                                "JamaReqID": JamaReqID
                            }
                        )
                    )
        else:
            pass    

    js = json.dumps(case_content,sort_keys=True,ensure_ascii=False,indent=4,separators=(',', ':'))
    json_path = excel_path.split('/')[-1].split('.')[0] + '.json'
    
    with open(json_path, "w+", encoding='utf-8') as jsFile:
        jsFile.write(js)
    print('Excel表对应Json文件创建成功')
    return json_path
    
def generate_case(excel_path=''):
    json_path=generate_json_from_excel(excel_path)   
    with open(json_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        json_data = json.loads(file_content)

    case_filename = json_path.split('.')[0] + '.txt'
    with open(case_filename,'w',encoding='utf-8') as f:
        for i in range(len(json_data)):
            comment = json_data[i]['备注'].replace('\n',"")
            module = json_data[i]['所属模块'].replace('\n',"")
            case_name = json_data[i]['用例名称'].replace('\n', "")
            # step_describe = json_data[i]['步骤描述']
            # except_result = json_data[i]['预期结果']
            ms_id = json_data[i]['ID']
            title = json_data[i]['标签']
            logical_addreds_list = title.split(",")

            if comment:
                f.write("    #"+comment+'\n')
            if title:
                f.write("    #"+title+ '\n')

            f.write(f'    @allure.story(\'{module[1:]}\')'+ '\n')
            f.write(f'    @allure.title(\'{case_name}\')'+'\n')
            f.write(f'    def test_caseid_{ms_id}(self):' + '\n')
            f.write(f'        pass' + '\n')
            f.write('\n')

    print(f'Json文件对应的{case_filename}创建成功')
    os.system(f'rm -rf {json_path}')
#cd /root/TestDev/sat/xat_cases/legacy/basetech/basetech_tools
#python3 generate_case_from_ms_excel.py
if __name__ == '__main__':
    generate_case('data/基础诊断服务.xlsx')
    generate_case('data/诊断DID.xlsx')
    generate_case('data/EOL.xlsx')

    