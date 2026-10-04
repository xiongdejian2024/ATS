from ms_to_jama import *
import os
import sys
project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()


def get_jama_mapping(nodeIds, projectid):
    up = Upload()
    data, mapping, repeat = up.get_cases(nodeIds, projectid)
    return mapping, repeat

def split_repeat_mapping(repeat):
    """
    repeat: list
    eg: [
        {'id': 1919320, 'jamaid': '1724860'}, 
        {'id': 1919319, 'jamaid': '1724860'}, 
        {'id': 1919318, 'jamaid': '1724860'},
        {'id': 104912, 'jamaid': '1724861'},
        {'id': 104913, 'jamaid': '1724861'}
    ]
    return: [{'id': 1919318, 'jamaid': '1724860'},{'id': 104912, 'jamaid': '1724861'}]
    """
    jamaids = []
    num1 = []
    for i in range(len(repeat)) :
        jamaids.append(repeat[i].get("jamaid"))
    new_jamaids = list(set(jamaids))
    for j in range(len(new_jamaids)):
        isd = []
        for i in range(len(repeat)):
            if repeat[i].get('jamaid') == new_jamaids[j]:
                isd.append(repeat[i].get('id'))
        num1.append({"id": min(isd), "jamaid": new_jamaids[j]})
        
    return num1
    

def update_jamaid(nodeIds, projectid):
    base = os.path.join(project_root, "test_case/soa/test_function")
    mapping, repeat = get_jama_mapping(nodeIds, projectid)
    logger.info(mapping)
    logger.info(repeat)
    min_mapping = split_repeat_mapping(repeat=repeat)
    mapping = mapping + min_mapping
    for file in os.listdir(base):
        if os.path.isfile(file) and  file != "test_ClimateService.py":
            logger.info(f"开始更新文件{file}")  
            data = ""
            need_to_do = []
            _num = split_repeat_mapping(repeat)

            with open(os.path.join(base, file), "r", encoding="utf8") as fd:
                lines = fd.read().split("\n")
                for i in range(len(lines)):
                    if "caseid" and "(self)" in lines[i]:
                        jama = lines[i].split("_caseid_")[-1].split("(self)")[0]
                        jamaids = []
                        ids = []
                        for j in range(len(mapping)):
                            jamaids.append(mapping[j].get("jamaid"))
                            ids.append(int(mapping[j].get("id")))
                        #针对jama不重复的用例筛选出对应的id
                        if "X" in jama:
                            continue
                        elif "L" in jama:
                            continue
                        elif "o" in jama:
                            continue
                        elif "_" in jama:
                            split_jama = jama.split("_")
                            for n in split_jama:
                                if n in jamaids:
                                    for j in range(len(mapping)):
                                        if mapping[j].get("jamaid") != '' and int(n) == int(mapping[j].get("jamaid")):
                                            lines[i] = lines[i].replace(str(n), str(mapping[j].get("id")))
                            data += lines[i] + "\n"
                        else:
                            if jama in jamaids:
                                for j in range(len(mapping)):
                                    if mapping[j].get("jamaid") != '' and int(jama) == int(mapping[j].get("jamaid")):
                                        lines[i] = lines[i].replace(str(jama), str(mapping[j].get("id")))
                                        data += lines[i] + "\n"
                            elif int(jama) in ids:
                                data += lines[i] + "\n"
                            else:
                                data += lines[i] + "\n"
                                if int(jama) not in need_to_do:
                                    need_to_do.append(int(jama))
                                    
                        #针对jama重复的用例筛选重复次数num，匹配到id的去除，剩余一个即修改
                        # if len(repeat) != 0:
                        #     for x in range(len(_num)) :
                        #         for k,w in _num[x].items():
                        #             s = w
                        #             while s > 0:
                        #                 for a in range(w): 
                        #                     if int(jama) == int(repeat[a].get("id")):
                        #                         w -= 1
                        #                         repeat = [i for i in repeat if i.get("id") != int(jama)]
                        #                         continue
                        #                 s -= 1
                        #             else:
                        #                 if w == 1:
                        #                     for a in range(len(repeat)): 
                        #                         if int(jama) == k:
                        #                             lines[i] = lines[i].replace(str(jama), str(repeat[a].get("id")))
                        #                             data += lines[i] + "\n"
                        #                 else:
                        #                     need_to_do.append(int(jama))
                           
                    else:
                        data += lines[i] + "\n"
            print(f"文件{file}需要关注的用例id为: {_num}")
            with open(os.path.join(base, file), "w", encoding="utf8") as fs:      
                fs.write(data, )
            logger.info(f"文件{file}更新完毕")

           

if __name__ == '__main__':       
    nodeIds = ["caf30735-1d80-4308-9aaf-c8b91e403588", "1141fe38-edc3-46ff-a4bc-a7e3b2e18b87"]
    projectid = "52c062de-78ea-41b4-8307-bed834cef1a7"  

    update_jamaid([], projectid)
