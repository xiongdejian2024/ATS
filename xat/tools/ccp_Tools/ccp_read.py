import xlrd, json

class Read_Ccp_Xlsx_File:
    def __init__(self,filename):
        self.data = xlrd.open_workbook(filename)

    def read_xlsx_file(self):
        # 打开Excel文件
        # 读取第一个工作表
        table = self.data.sheets()[0]
        # 统计行数
        rows = table.nrows
        data = []  # 存放数据
        for i in range(1, rows):
            # if i >2:
            #     break
            # else:
                values = table.row_values(i)
                data.append(
                    (
                        {
                            "字节序号": str(int(values[0])),
                            "参数类型": values[1],
                            "CCP英文描述":values[2],
                            "CCP中文描述":values[3],
                            "CCP取值":values[4],
                            "相关ECU":values[5],
                            "MarsOne_Useful": values[6],
                            "原车CCP值": values[7],
                            "原车CCP解析": values[8],
                            "待写入CCP值":values[9]
                        }
                    )
                )
        return data

if __name__ == '__main__':
    file = Read_Ccp_Xlsx_File("ccp.xlsx")
    data=file.read_xlsx_file()
    # 字典中的数据都是单引号，但是标准的json需要双引号
    js = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
    #print(js)
    # 前面的数据只是数组，加上外面的json格式大括号
    #js = "{" + js + "}"
    # 可读可写，如果不存在则创建，如果有内容则覆盖
    jsFile = open("./ccp.json", "w+", encoding='utf-8')
    jsFile.write(js)
    jsFile.close()