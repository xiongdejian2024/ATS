'''
@filename     : libCANoe.py
@time         : 2024/06/20 14:27
@author       : junxing.pang@jiduauto.com
@description  : CANoe com32 interface
'''

import os
import time
import logging
import subprocess
from typing import Optional, Union, Any

from win32com.client import *
from win32com.client.connect import *


def DoEvents():
    pythoncom.PumpWaitingMessages()
    time.sleep(.1)


def DoEventsUntil(cond):
    while not cond():
        DoEvents()


class CANoe:
    """Wrapper class for CANoe Application object"""
    Started = False
    Stopped = False

    def __init__(self):
        app = DispatchEx("CANoe.Application")
        dir(app)
        self.app = app

    @property
    def version(self) -> str:
        """
        Get the CANoe version

        :return: The CANoe version
        :rtype: `str`
        """
        if (self.app != None):
            self.ver = self.app.Version
            return 'Loaded CANoe version ' \
                + str(self.ver.major) + '.' \
                + str(self.ver.minor) + '.' \
                + str(self.ver.Build) + '...'
        else:
            raise RuntimeError(
                "Get CANoe Application failed, unable to get version")

    @property
    def running(self) -> bool:
        """
        Whether the CANoe is running

        :return: Whether the CANoe is running
        :rtype: `bool` True is running and False is not
        """
        return True if self.app.Measurement.Running else False

    def new(self) -> None:
        """
        Create a new default CANoe project
        """
        if (self.app != None):
            self.app.New()

    def open(self, cfg_path: str) -> bool:
        """
        Loads a configuration.

        :param cfg_path: MUST be the complete path for the configuration.
        :type: `str`

        :return: whether the configuration was successfully loaded
        :rtype: `bool` True is load successfully and False is not
        """
        if (self.app != None):
            # if os.path.isfile(cfg_path) and (os.path.splitext(cfg_path)[1] == ".cfg"):
            if (os.path.splitext(cfg_path)[1] == ".cfg"):
                self.app.Open(cfg_path)  # TODO need to enhance
                if self.app.Configuration.OpenConfigurationResult.result:
                    return True
                else:
                    return False
            else:
                raise RuntimeError("Can't find CANoe cfg file")
        else:
            raise RuntimeError(
                "CANoe Application is missing, unable to load Configuration")

    def quit(self):
        """
        Quits the app.
        """
        if (self.app != None):
            self.stop()
            self.app.Quit()
        # make sure the CANoe is close properly, otherwise enforce taskkill
        output = subprocess.check_output('tasklist', shell=True)
        if "CANoe32.exe" in str(output):
            os.system("taskkill /im CANoe32.exe /f 2>nul >nul")
        self.app = None

    def save(self, cfg_path: str):
        """save the project, if you set another "*.cfg", that means you save as the project

        :param cfg_path: cfg path, and this MUST be the absolute path
        :type cfg_path: str
        """
        if (self.app is not None):
            self.app.Configuration.Save(cfg_path)

    def start(self):
        """
        Start the canoe

        And this function will try to start the app 3 times if it fails
        """
        retry = 0
        retry_counter = 3
        # try to establish measurement within 20s timeout
        while not self.running and (retry < retry_counter):
            self.app.Measurement.Start()
            time.sleep(1)
            retry += 1
        if (retry == retry_counter):
            raise RuntimeWarning(
                "CANoe start measuremet failed, Please Check Connection!")

    def stop(self):
        """
        Stop the canoe
        """
        if self.running:
            self.app.Measurement.Stop()
        else:
            pass

    def add_variable(self, name: str, name_space=Union[str, None], init_value=Union[str, int, float, None], min_value=Union[str, int, float, None], max_value=Union[str, int, float, None], readonly=False) -> None:
        """
        Add new variables

        :param name: Name of the variable
        :type name: `str`

        :param name_space: Name of the Namespace
        :type name_space: `str`

        :param init_value: Initial value of the variable
        :type init_value: `Union[str, int, float, None]`

        :param min_value: Minimum value
        :type min_value: `Union[str, int, float, None]`

        :param max_value: Maximum value
        :type max_value: `Union[str, int, float, None]`
        """
        try:
            if (self.app != None):
                ns = self.app.System.Namespaces(name_space)
                vars = ns.Variables
                if readonly:
                    vars.AddEx(name, init_value, min_value, max_value, None)
                else:
                    vars.AddWritableEx(name, init_value, min_value, max_value)
            else:
                raise RuntimeError("CANoe is not open, unable to add variable")
        except Exception as e:
            logging.exception(
                "Add variable run to error, exception is {%s}" % e)

    def get_namespace_names(self) -> Optional[list]:
        """
        Get all the names of namespaces

        :return: all the names of namespaces
        :rtype: `list` or `None`
        """
        if (self.app != None):
            ns = self.app.System.Namespaces
            return [item.Name for item in ns]
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def get_sysvars_names_by_namespace(self, namespace: str) -> Optional[list]:
        """
        Gets the names of all variables in the namespace

        :param namespace: the name of the namespace
        :type namespace: `str`

        :return: all the names of variables in a namespace
        :rtype: `list` or `None`
        """
        if (self.app != None):
            ns = self.app.System.Namespaces
            vars = ns(namespace)
            var = vars.Variables
            return [item.Name for item in var]
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def get_sysvars_value_by_namespace(self, namespace: str) -> Optional[dict]:
        """
        Gets the names and values of all variables in the namespace

        :param namespace: the name of the namespace
        :type namespace: `str`

        :return: all the names of variables in a namespace
        :rtype: `dict` or `None`
        """
        if (self.app != None):
            ns = self.app.System.Namespaces
            vars = ns(namespace)
            var = vars.Variables
            names = [item.Name for item in var]
            values = [item.Value for item in var]
            return dict(zip(names, values))
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def set_sysvar_value(self, sysvar_name: str, namespace: str, value: Any) -> None:
        """
        Set the value of a variable

        :param sysvar_name: the name of the variable
        :type sysvar_name: `str`

        :param namespace: the name of the namespace
        :type namespace: `str`

        :param value: the value you want to set
        :type: `Any`
        """
        if (self.app != None):
            ns = self.app.System.Namespaces
            vars = ns(namespace)
            var = vars.Variables(sysvar_name)
            var.Value = value
        else:
            raise RuntimeError(
                "CANoe is not open, unable to set sysvaribale value")

    def insert_test_module(self, env_name: str, env_path: str, module_path: Union[str, list]) -> None:
        """Insert CAPL Test Module

        :param env_name: Test environment name
        :type env_name: str
        :param env_path: Ready to save the test environment path
        :type env_path: str
        :param module_path: Ready to add to the test environment module path
        :type module_path: Union[str, list]
        """
        self.TestSetup = self.app.Configuration.TestSetup
        testitem = self.TestSetup.TestEnvironments.Add(env_name)
        testitem.Save(env_path)
        testmodules = self.TestSetup.TestEnvironments(1).TestModules
        if type(module_path) is not list:
            testmodules.Add(module_path)
        else:
            for module in module_path:
                testmodules.Add(module)

    def insert_XML_module(self, env_name: str, env_path: str, xml_path: str, component_path: Union[str, list]) -> None:
        """insert_XML_module

        :param env_name: Test enviroment name
        :type env_name: str
        :param env_path: Ready to save the test environment path
        :type env_path: str
        :param xml_path: Ready to add to the test environment xml module
        :type xml_path: str
        :param component_path: Additional components added to the xml module
        :type component_path: Union[str, list]
        """

        self.TestSetup = self.app.Configuration.TestSetup
        for testitem in self.TestSetup.TestEnvironments:
            print(testitem.Name)
            print("112")
            if testitem.Name == "Test Environment":
                print("11111111111111111111111111")
                # testitem = self.TestSetup.TestEnvironments.Add(env_name)  # 文件夹的名字
                # testitem.Save(env_path)
                # testmodules = testitem.Items.AddTestModule(xml_path)  # 节点的名字 vxt后缀的文件（xml格式）
                # if type(component_path) is not list:
                #     testmodules.Modules.Add(component_path)
                # else:
                #     for module in component_path:
                #         testmodules.Modules.Add(module)
                # print("类型打印")
                # print(type(testmodules))
                testenvironment = self.TestSetup.TestEnvironments.Item("Test Environment")
                testenvironment = CastTo(testenvironment, "ITestEnvironment2")
                testmodules_old = testenvironment.TestModules.Item("Test 3")
                print(type(testmodules_old))
                for abc in testmodules_old.Modules:
                    print(abc.Name)
                    print(abc.FullName)
                else:
                    pass
                    # testmodules_old.Modules.Remove("DoIP")
                # print(dir(testmodules_old.Modules))

    def load_test_setup(self):
        """
        load test setup
        """
        self.TestSetup = self.app.Configuration.TestSetup
        testitem = self.TestSetup.TestEnvironments.Item(1)
        #! currently only support one environment
        testenv = CastTo(testitem, "ITestEnvironment2")
        # TestModules property to access the test modules
        self.TestModules = []
        self.traverse_test_item(
            testenv, lambda tm: self.TestModules.append(CanoeTestModule(tm)))

    def run_test_modules(self):
        """ starts all test modules and waits for all of them to finish"""
        # start all test modules
        for tm in self.TestModules:
            tm.Start()

        # wait for test modules to stop
        while not all([not tm.Enabled or tm.IsDone() for tm in app.TestModules]):
            DoEvents()

    def traverse_test_item(self, parent, testf):
        for test in parent.TestModules:
            testf(test)
        for folder in parent.Folders:
            found = self.traverse_test_item(folder, testf)

    def set_report_config(self, auto_numbering: bool, full_name: str) -> None:
        """set report config

        :param auto_numbering: automatically be numbered (consecutively) or not
        :type auto_numbering: bool
        :param full_name: Sets or determines the complete path to the test report
        :type full_name: str
        """
        # TODO NEED TO TEST
        testitem = self.TestSetup.TestEnvironments.Item(1)
        testitem.Report.AutoNumbering = auto_numbering
        testitem.Report.FullName = full_name


class CanoeTestModule:
    """Wrapper class for CANoe TestModule object"""

    def __init__(self, tm):
        self.tm = tm
        self.Events = DispatchWithEvents(tm, CanoeTestEvents)
        self.Name = tm.Name
        self.IsDone = lambda: self.Events.stopped
        self.Enabled = tm.Enabled

    def Start(self):
        if self.tm.Enabled:
            self.tm.Start()
            while not self.Events.stopped:
                DoEvents()


class CanoeTestEvents:
    """Utility class to handle the test events"""

    def __init__(self):
        self.started = False
        self.stopped = False
        self.WaitForStart = lambda: DoEventsUntil(lambda: self.started)
        self.WaitForStop = lambda: DoEventsUntil(lambda: self.stopped)

    def OnStart(self):
        self.started = True
        self.stopped = False
        logging.info(f"< {self.Name} started >")

    def OnStop(self, reason):
        self.started = False
        self.stopped = True
        logging.info(f"< {self.Name} stopped >")


app = CANoe()
