# How to use

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 修改脚本文件引用路径

```python
base_path = r"D:\Sylar\01_python\01_pythonCAPL\CANoePrj" # 修改为你的项目路径
```

3. 运行脚本

```bash
python test_canoe.py
```

# 脚本结构

## libCANoe.py

封装的CANoe Com32接口，用于调用CANoe

## GererateXMLModule.py

生成xml module文件的示例代码，用于生成 `*.vxt`文件

## test_canoe.py

调用执行

具体步骤如下

- 从`test_CANoeDemo.can` 文件中提取testcase的函数名生成 xml module文件 `CANoeDemo.vxt`
- 打开base CANoe工程 `CANoeDemo.cfg`
- 创建测试环境，保存测试环境 `test.tse`
- 创建XML module test
- 导入XML module文件 `CANoeDemo.vxt`
- 在`Components`导入`test_CANoeDemo.can` 文件
- 执行测试用例
- 结束测试用例，生成报告
- 退出CANoe