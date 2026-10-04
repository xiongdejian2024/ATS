import os
#删除/var/core文件夹下的文件
def delete_var_core_files(file_path):
    if os.path.isdir(file_path):
        for file in ["pytest","python","CarConfigServic","a.out"]:
            core_file_pytest = [os.path.join(file_path,i) for i in os.listdir(file_path) if file in i]
            files = sorted(core_file_pytest, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
            if len(files) > 10:
                for i in files[10:]:
                    os.system(f"rm -rf {i}")
            
            else:
                print(f'core文件{file},个数为{len(files)}个')
    else:
        print(f"{file_path}目录不存在")

#删除/root/TCAM下的文件
def delete_root_TCAM_files(file_path):
    if os.path.isdir(file_path):
        TCAM_files = [os.path.join(file_path,i) for i in os.listdir(file_path)]
        files = sorted(TCAM_files, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
        if len(files) > 10:
            for i in files[10:]:
                os.system(f"rm -rf {i}")
        else:
            print(f'TCAM目录下文件个数为{len(files)}个')
    else:
        print(f"{file_path}目录不存在")

#删除root/autotest/willow/下的文件
def delete_root_autotest_files(file_path):
    if os.path.isdir(file_path):
        willow_dir = [ os.path.join(file_path,i) for i in os.listdir(file_path) 
                    if "-" in i and os.path.isdir(os.path.join(file_path,i))]
        dir = sorted(willow_dir, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
        agent_log = [os.path.join(file_path,i) for i in os.listdir(file_path) if "agent" in i and "-" in i]
        agent_files = sorted(agent_log, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
        if len(dir) > 10:
            for i in dir[10:]:
                os.system(f"rm -rf {i}")
        else:
            print(f"willow_dir下的带'-'的目录个数为{len(dir)}")
        
        if len(agent_files) > 10:
            for i in  agent_files[10:]:
                os.system(f"rm -rf {i}")
        else:
            print(f"agent_log文件个数为{len(agent_files)}")
    else:
        print(f"{file_path}目录不存在")

#删除/root/BGM下的文件
def delete_root_BGM_files(file_path):
    if os.path.isdir(file_path):
        BGM_dir = [os.path.join(file_path,i) for i in os.listdir(file_path)]
        dir = sorted(BGM_dir, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
        if len(dir) > 10:
            for i in dir[10:]:
                os.system(f"rm -rf {i}")
        else:
            print(f"BGM目录下的文件个数为{len(dir)}")
    else:
        print(f"{file_path}目录不存在")

#删除/root/SOA下的文件
def delete_root_SOA_files(file_path):
    if os.path.isdir(file_path):
        SOA_dir = [os.path.join(file_path,i) for i in os.listdir(file_path)]
        dir = sorted(SOA_dir, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
        if len(dir) > 10:
            for i in dir[10:]:
                os.system(f"rm -rf {i}")
        else:
            print(f"SOA目录下的文件个数为{len(dir)}")
    else:
        print(f"{file_path}目录不存在")

#删除/root/allure_report下的文件
def delete_root_allure_report_files(file_path):
    if os.path.isdir(file_path):
        allure_report = [os.path.join(file_path,i) for i in os.listdir(file_path)]
        dir = sorted(allure_report, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
        if len(dir) > 10:
            for i in dir[10:]:
                os.system(f"rm -rf {i}")
        else:
            print(f"allure_report目录下的文件个数为{len(dir)}")
    else:
        print(f"{file_path}目录不存在")

#删除/root/tset_case_log下的文件
def delete_root_test_case_log_files(file_path):
    if os.path.isdir(file_path):
        test_case_log = [os.path.join(file_path,i) for i in os.listdir(file_path)]
        files = sorted(test_case_log, key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
        if len(files) > 10:
            for i in files[10:]:
                os.system(f"rm -rf {i}")
        else:
            print(f"test_case_log目录下的文件个数为{len(files)}")
    else:
        print(f"{file_path}目录不存在")

if __name__=="__main__":
    print("删除前root目录的空间大小为：",os.system("du -sh /root"))
    delete_root_TCAM_files("/root/TCAM")
    # delete_root_autotest_files("/root/autotest/willow")
    delete_root_BGM_files("/root/BGM")
    delete_root_SOA_files("/root/SOA")
    delete_root_allure_report_files("/root/allure_report")
    delete_root_test_case_log_files("/root/test_case_log")
    print("删除后root目录的空间大小为：",os.system("du -sh /root"))
    print("删除前/var/core目录的空间大小为：",os.system("du -sh /var/core"))
    delete_var_core_files("/var/core")
    print("删除后/var/core目录的空间大小为",os.system("du -sh /var/core"))
    

