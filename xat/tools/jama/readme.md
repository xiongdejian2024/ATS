# jama用例上传

**1,修改sheet.yaml文件中的用户名和密码（自己的）**
```
username: "public_soa_bgm_tcam"
password: "public_soa_bgm_tcam"
```
**2,在IT Care中添加jama的编辑权限**
```
https://wtoolkit.jiduauto.com/weChatToolKits/wechat/index
```
**3,在jama新建sheet页的文件夹，更新在sheet.yaml文件中,如下**
```
格式《sheet名: jama文件夹id》

BGM网络通道定义: 1193435
数字安全: 1188842
EM: 1193655
```
**4,更改to_new_excel.py文件中expect_list列表中的值为自己需要修改的sheet名称**
```
expect_list = ['Ecall', 'EM']
```
**5,更改to_new_excel.py文件中main方法的两个参数**
```
to_new_excel("需要更新的测试用例.xlsx", "新生成的测试用例.xlsx")
```
**6,运行to_new_excel.py文件**
```
生成新文件中的jama_id回填到sharepoint中
```