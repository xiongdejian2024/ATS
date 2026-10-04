import os 
import os.path 
import shutil 
import time,  datetime
from zipfile import *
import zipfile 
import shutil
import chardet
import codecs

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name)) 
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname)-len(zipfilename)+4:]
        zf.write(tar,arcname)
    zf.close()

def alter(file,old_str,new_str):
  """
  :param file:
  :param old_str:
  :param new_str:
  :return:
  """
  file_data = ""
  with open(file, "r",encoding='utf-8') as f:
    for line in f:
      if old_str in line:
        #line = line.replace(old_str,new_str)
        line = '<Library Include="libs\\windows\\x86\\USB2XXX.lib" />'
      file_data += line
  with open(file,"w",encoding='utf-8') as f:
    f.write(file_data)

def remove_linux_dir ():
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        if (not("vs2010" in root))and(not("linux" in root))and(not("source" in root))and("USB2XXX" in root):
            if 'vs2010' in dirs:
                print(root)
                linux_path=root+'\linux'
                if os.path.exists(linux_path):
                    shutil.rmtree(linux_path)

def change_file_name (root_dir,project_name):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        if 'USB2XXX' in os.path.split(root)[1]:
            #print(root)
            old_name=root
            new_name=os.path.join(os.path.split(root)[0],project_name)
            #if old_name != new_name:
                #os.rename(old_name, new_name)
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for name in files:# Remove .sdf file
            if '.sln' in name:
                print(os.path.join(root, name))
                old_str = name[0:-4]
                #alter(os.path.join(root, name),old_str,project_name)
                #os.rename(os.path.join(root, name), os.path.join(root, project_name+'.sln'))
            if '.vcxproj' in name:
                print(os.path.join(root, name))
                old_str = name[0:-8]
                #alter(os.path.join(root, name),old_str,project_name)
                #alter(os.path.join(root, name),"libs\\windows\\x86\\USB2XXX.lib",'abcdefghijklmnopqrst')
                #alter(os.path.join(root, name),'abcdefghijklmnopqrst','libs\\windows\\x86\\USB2XXX.lib')
                #os.rename(os.path.join(root, name), os.path.join(root, project_name+'.vcxproj'))
                new_file_name=os.path.join(root, name)+'.user'
                print(new_file_name)
                with open(new_file_name,"w",encoding='utf-8') as f:
                    f.write('''<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <LocalDebuggerEnvironment>path=%path%;./libs/windows/x86
$(LocalDebuggerEnvironment)</LocalDebuggerEnvironment>
    <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
  </PropertyGroup>
</Project>''')

def change_vs_project_name ():
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        if (not("vs2010" in root))and(not("linux" in root))and(not("source" in root))and("USB2XXX" in root):
            if 'vs2010' in dirs:
                project_name = os.path.split(root)[1]
                print(project_name)
                linux_path=os.path.join(root,'linux')
                print(linux_path)
                change_file_name(os.path.join(root,'vs2010'),project_name)

def change_linux_dir_name (root_dir,project_name):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        if 'USB2XXX' in os.path.split(root)[1]:
            print(root)
            old_name=root
            new_name=os.path.join(os.path.split(root)[0],project_name)
            print(new_name)
            if old_name != new_name:
                os.rename(old_name, new_name)

def change_linux_project_name ():
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        if (not("vs2010" in root))and(not("linux" in root))and(not("source" in root))and("USB2XXX" in root):
            if 'vs2010' in dirs:
                project_name = os.path.split(root)[1]
                print(project_name)
                linux_path=os.path.join(root,'linux')
                print(linux_path)
                change_linux_dir_name(linux_path,project_name)


def change_code_file_name (root_dir,project_name):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for name in files:
            if ('.h' in name):
                print(os.path.join(root, name))
                #os.rename(os.path.join(root, name), os.path.join(root, project_name+'.cpp'))
                file_name = os.path.join(root, name)
                print(file_name)
                file_data = ""
                with open(file_name, "rb") as f:
                    encode = chardet.detect(f.read())
                    print(encode["encoding"])
                    f.close()
                    #f=open(file_name,'r',encode["encoding"])
                    #file_data = f.read()
                    with open(file_name, mode='r', encoding=encode["encoding"]) as fi:
                        lines=fi.readlines()
                        fi.close()
                        with open(file_name, mode='w+b') as fo:
                            for li in lines:
                                li = li.replace('\n', '').replace('\r', '')
                                line_sep='\r\n'
                                fo.write(li.encode(encoding="GB2312") + line_sep.encode(encoding="GB2312"))
                            fo.close()
        #print(root_dir)
        #print(project_name)
        #print(files)

def change_vs_code_name ():
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        if (not("vs2010" in root))and(not("linux" in root))and(not("source" in root))and("USB2XXX" in root):
            if 'source' in dirs:
                project_name = os.path.split(root)[1]
                print(project_name)
                change_code_file_name(os.path.join(root,'source'),project_name)


def make_linux_dir ():
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        if (not("vs2010" in root))and(not("linux" in root))and(not("source" in root))and("USB2XXX" in root):
            if 'vs2010' in dirs:
                print(root)
                linux_path=root+'\linux'
                if os.path.exists(linux_path):
                    shutil.rmtree(linux_path)
                os.mkdir(linux_path)
                project_dir = os.path.join(linux_path,os.path.split(root)[1])
                print(project_dir)
                shutil.copytree(os.path.join(os.getcwd(),'LinuxGccPublicFiles'),project_dir)

def update_windows_libs ():
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        if 'vs2010' in root:
            #print(root)
            file_type = ['.vcxproj']
            file_path = root
            file_path_vec = [os.path.join(file_path,imgpath) for imgpath in os.listdir(file_path) if os.path.splitext(imgpath)[1] in file_type]
            if len(file_path_vec) > 0:
                print(root)
                libs_dir = os.path.join(root,'libs')
                if os.path.exists(libs_dir):
                    shutil.rmtree(libs_dir)
                shutil.copytree(os.path.join(os.path.join(os.getcwd(),'LinuxGccPublicFiles'),'libs'),os.path.join(root,'libs'))
'''
            for name in files:
                if name.endswith(".dll") or name.endswith(".lib"):
                    os.remove(os.path.join(root, name))
                    print ("Delete File: " + os.path.join(root, name))
'''
# copy USB2XXX.dll to project directory
def copyFile(srcPath,rootDir):  
	if os.path.exists(srcPath):
		obj = listDir(rootDir)
		if None != obj:
			shutil.copy(srcPath,obj)  
# list all directory
def listDir(rootDir):
    filelist=os.listdir(rootDir) 
    for f in filelist:
        file = os.path.join( rootDir, f ) 
        if os.path.isdir(file):
            dllDirList = os.listdir(file)
            print(dllDirList)
            if 'usb_device.h' in dllDirList:
                return file

# remove all file exception excList
def removeFiles(rootDir,excList):
    filelist=os.listdir(rootDir) 
    for f in filelist:
        file = os.path.join( rootDir, f ) 
        if os.path.isfile(file) and not f in excList: 
            os.remove(file)  
            print (file+" removed!") 
        elif os.path.isdir(file):
            removeFiles(file,excList)
# remove directory
def removeDirs(rootDir):
    filelist=os.listdir(rootDir)  
    for f in filelist:  
        file = os.path.join( rootDir, f )
        if os.path.isdir(file):  
            shutil.rmtree(file,True)  
            print ("dir "+file+" removed!") 
    os.rmdir(rootDir)

def cleanProject():  
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:# Remove .sdf file
            if '.sdf' in name:
                os.remove(os.path.join(root, name))
            if '.suo' in name:
                os.remove(os.path.join(root, name))
            if '.cmd' in name:
                os.remove(os.path.join(root, name))
            if '.vcxproj.filters' in name:
                os.remove(os.path.join(root, name))
            if '.vcxproj.user' in name:
                os.remove(os.path.join(root, name))
        for name in dirs:# Remove buil directory
            if name == 'Debug' or name == 'ipch'or name == 'Release' or name == 'raspberrypi' or name =='.vs':
                removeFiles(os.path.join(root, name),())
                removeDirs(os.path.join(root, name))

def list_all_files(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir)
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files

def update_header_files():
    raw_header_file_path = 'E:\\Projects\\USB2XXX\\trunk\\USB2XXX\\USB2XXX\\source'
    headerFileList = [item for item in filter(lambda file: file.endswith('.h'),list_all_files(raw_header_file_path))]
    #print(headerFileList)
    header_file_path = '..\\..\\sdk\\api\\C&C++'
    used_header_file_list = [item for item in filter(lambda file: file.endswith('.h'),os.listdir(header_file_path))]
    for root, dirs, files in os.walk(header_file_path, topdown=False):
        for name in files:
            for all_name in headerFileList:
                if name == os.path.split(all_name)[1]:
                    #print(name)
                    shutil.copy(all_name,os.path.join(root, name))
    #print(headerFileList)
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            if name in used_header_file_list:
                shutil.copy(os.path.join(header_file_path, name),os.path.join(root, name))
if __name__ == '__main__':
    update_header_files()
    #change_linux_project_name()
