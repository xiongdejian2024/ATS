# -*- coding:utf8 -*-

import time
import os
import subprocess
import chardet
from win32com.client import *
from win32com.client.connect import *

def DoEvents():
    pythoncom.PumpWaitingMessages()
    time.sleep(.5)

def DoEventsUntil(cond):
    t= time.perf_counter()
    while not cond():
        DoEvents()
        if time.perf_counter() -t > 180:
            print(time.perf_counter() -t)
            break

def KILL_CANOE():
    # command = 'taskkill /F /IM CANoe64.exe'
    # os.system(command)
    # time.sleep(3)
    killcanoeprocess_cmd = "taskkill /F /IM CANoe64.exe"
    stdout, stderr = subprocess.Popen(killcanoeprocess_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    stdout_e = chardet.detect(stdout)["encoding"]
    stderr_e = chardet.detect(stderr)["encoding"]
    if stdout_e is None:
        stdout_s = ""
    else:
        stdout_s = stdout.decode(stdout_e).strip()
    if stderr_e is None:
        stderr_s = ""
    else:
        stderr_s = stderr.decode(stderr_e).strip()
    # stderr_s = str(stderr, encoding="UTF-8").strip()
    # stdout_s = str(stdout, encoding="UTF-8").strip()
    if stderr_s == "" and ("SUCCESS" in stdout_s or "成功" in stdout_s):
        return True
    else:
        return False

class CanoeSync(object):
    """Wrapper class for CANoe Application object"""
    AppOpened = False
    AppStopped = False
    Started = False
    Stopped = False
    Report_Generate = False
    ConfigPath = ""

    def __init__(self):
        app = DispatchEx('CANoe.Application')
        # app.Configuration.Modified = False
        ver = app.Version
        print('Loaded CANoe version ',
              ver.major, '.',
              ver.minor, '.',
              ver.Build, '...', sep='')
        self.App = app
        self.Measurement = app.Measurement
        self.Running = lambda: self.Measurement.Running
        self.WaitForStart = lambda: DoEventsUntil(lambda: CanoeSync.Started)
        self.WaitForStop = lambda: DoEventsUntil(lambda: CanoeSync.Stopped)
        self.WaitForAppStart = lambda: DoEventsUntil(lambda: CanoeSync.AppOpened)
        self.WaitForAppStop = lambda: DoEventsUntil(lambda: CanoeSync.AppStopped)
        # self.WaitForGenReport = lambda: DoEventsUntil(lambda: CanoeSync.Report_Generate)
        WithEvents(self.App.Measurement, CanoeMeasurementEvents)
        WithEvents(self.App, CanoeAppEvents)

    def Load(self, cfgPath):
        # current dir must point to the script file
        cfg = os.path.join(os.curdir, cfgPath)
        cfg = os.path.abspath(cfg)
        print('Opening: ', cfg)
        self.ConfigPath = os.path.dirname(cfg)
        self.Configuration = self.App.Configuration
        self.App.Open(cfg)
        self.WaitForAppStart()

    def LoadTestSetup(self, testsetup):
        self.TestSetup = self.App.Configuration.TestSetup
        path = os.path.join(self.ConfigPath, testsetup)
        testenv = self.TestSetup.TestEnvironments.Add(path)
        testenv = CastTo(testenv, "ITestEnvironment2")
        # TestModules property to access the test modules
        self.TestModules = []
        self.TraverseTestItem(testenv, lambda tm: self.TestModules.append(CanoeTestModule(tm)))

    def LoadTestConfiguration(self, testcfgname, testunits):
        """ Adds a test configuration and initialize it with a list of existing test units """
        tc = self.App.Configuration.TestConfigurations.Add()
        tc.Name = testcfgname
        tus = CastTo(tc.TestUnits, "ITestUnits2")
        for tu in testunits:
            tus.Add(tu)
        # TestConfigs property to access the test configuration
        self.TestConfigs = [CanoeTestConfiguration(tc)]

    def Start_bak(self):
        if not self.Running():
            self.Measurement.Start()
            self.WaitForStart()

    # def CANOE_WriteWindows(self,path):
    #     app = DispatchEx('CANoe.Application')
    #     # app.UI.Write.Output("Hello world!")
    #     # path = "D:\System.TXT"
    #     app.UI.Write.EnableOutputFile(path),0
    #     # print(1421,app.UI.Write.Copy())
    def Start(self):
        if not self.Running():
            self.Measurement.Start()
            self.WaitForStart()
            # print(110)
        if not self.Running():
            # command = 'taskkill /F /IM CANoe64.exe'
            # os.system(command)
            print(open('CANOE 启动失败，请检查工程和环境配置是否报错'))
            # sys.exit(1)

    def Stop(self):
        if self.Running():
            # self.WaitForGenReport()
            # self.Measurement.Stop() #Canoe old stop interface
            self.Measurement.StopEx()

            self.WaitForStop()
        # self.App.Configuration.Modified = False
        # self.App.Quit()

    def savecanoecfg(self):
        self.App.Configuration.Save()

    def savetestenvironment(self,testenvindex=1):
        testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item(testenvindex)
        testenvironment = CastTo(testenvironment, "ITestEnvironment")
        testenvironment.Save()

    def app_quit(self):
        # self.App.Configuration.Modified = False
        self.App.Quit()
        self.WaitForAppStop()

    def checkTestModulesorTestConfigs(self):
        testmodule_tag = False
        testconfig_tag = False
        testenvs = self.App.Configuration.TestSetup.TestEnvironments
        testenvs_count = testenvs.Count
        for c in range(1,testenvs_count+1):
            testenvironment = testenvs.Item(c)
            if testenvironment.Enabled is True:
                print("testenvironment:%s enabled" % testenvironment.Name)
                testenvironment = CastTo(testenvironment, "ITestEnvironment2")
                testmodules = testenvironment.TestModules
                testmodules_count = testmodules.Count
                for m in range(1,testmodules_count+1):
                    testmodule = testmodules.Item(m)
                    if testmodule.Enabled is True:
                        print("testmodule:%s enabled" % testmodule.Name)
                        testmodules_Modules = testmodule.Modules
                        testmodules_Modules_Count = testmodules_Modules.Count
                        # print("testmodules_Modules_Count:",testmodules_Modules_Count)
                        for m in range(1, testmodules_Modules_Count + 1):
                            testmodules_Modules_item = testmodules_Modules.Item(m)
                            if testmodules_Modules_item.Enabled is True:
                                print("testmodules_Modules_item:%s enabled" % testmodules_Modules_item.Name)
                                testmodule_tag = True
                                break
                        if testmodule_tag is True:
                            break
                        testmodules_Sequence = testmodule.Sequence
                        # if testmodules_Sequence:
                        testmodules_Sequence_Count = testmodules_Sequence.Count
                        # print("testmodules_Sequence_Count:",testmodules_Sequence_Count)
                        # if testmodules_Sequence_Count != 0:
                        for ss in range(1, testmodules_Sequence_Count + 1):
                            testmodules_Sequence_item = testmodules_Sequence.Item(ss)
                            if testmodules_Sequence_item.Enabled is True:
                                print("testmodules_Sequence_item:%s enabled" % testmodules_Sequence_item.Name)
                                testmodule_tag = True
                                break
                        if testmodule_tag is True:
                            break
                        testmodule = CastTo(testmodule, "ITSTestModule7")
                        testmodules_SequenceEx = testmodule.SequenceEx
                        testmodules_SequenceEx_Count = testmodules_SequenceEx.Count
                        # print("testmodules_SequenceEx_Count:",testmodules_SequenceEx_Count)
                        for s in range(1, testmodules_SequenceEx_Count + 1):
                            testmodules_SequenceEx_item = testmodules_SequenceEx.Item(s)
                            if testmodules_SequenceEx_item.Enabled is True:
                                print("testmodules_SequenceEx_item:%s enabled" % testmodules_SequenceEx_item.Name)
                                testmodules_SequenceEx_item_sequence_count = testmodules_SequenceEx_item.SequenceEx.Count
                                if testmodules_SequenceEx_item_sequence_count != 0:
                                    testmodule_tag = True
                                    break
                        if testmodule_tag is True:
                            break
        tstconfigurations = self.App.Configuration.TestConfigurations
        tstconfigurations_count = tstconfigurations.Count
        for c in range(1,tstconfigurations_count+1):
            tstconfiguration = tstconfigurations.Item(c)
            if tstconfiguration.Enabled is True:
                print("%s enabled" % tstconfiguration.Name)
                tstunits = tstconfiguration.TestUnits
                tstunits_count = tstunits.Count
                for t in range(1,tstunits_count+1):
                    tstunit = tstunits.Item(t)
                    if tstunit.Enabled is True:
                        print("%s enabled" % tstunit.Name)
                        testconfig_tag = True
                        break
                if testconfig_tag is True:
                    break
        return [testmodule_tag,testconfig_tag]

    def EnableTestModuleTestcasebak(self, testcases, testsequencename, testmoduleindex=1, testenvindex=1):
        testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item(testenvindex)
        testenvironment = CastTo(testenvironment, "ITestEnvironment2")
        testmodule = testenvironment.TestModules.Item(testmoduleindex)
        testmodule = CastTo(testmodule, "ITSTestModule7")
        testmodules_SequenceEx = testmodule.SequenceEx
        if testsequencename is None:
            testmodules_SequenceEx_item = testmodules_SequenceEx.Item(1)
        else:
            testmodules_SequenceEx_item = testmodules_SequenceEx.Item(testsequencename)
        testmodules_SequenceEx_item.Enabled = False
        print("testmodules_SequenceEx_item enable:", testmodules_SequenceEx_item.Enabled)
        testmodules_SequenceEx_item_sequence = testmodules_SequenceEx_item.SequenceEx
        testcase_except = []
        for i in testcases:
            try:
                testcaseinfos = testmodules_SequenceEx_item_sequence.Item(i)
                testcaseinfos.Enabled = True
                print("Name:%s,Ident:%s,Type:%s,Enabled:%s,Verdict:%s" % (
                    testcaseinfos.Name, testcaseinfos.Ident,
                    testcaseinfos.Type, testcaseinfos.Enabled,
                    testcaseinfos.Verdict))
            except:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test.py")
                testcase_except.append(i)
        return testcase_except

    def EnableTestModuleTestcase(self, testcases, testsequencename, testmoduleindex=1, testenvindex=1):
        testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item(testenvindex)
        testenvironment = CastTo(testenvironment, "ITestEnvironment2")
        testmodule = testenvironment.TestModules.Item(testmoduleindex)
        # testmodules_Sequence = testmodule.Sequence
        testmodule = CastTo(testmodule, "ITSTestModule7")
        testmodules_SequenceEx = testmodule.SequenceEx
        testmodules_SequenceEx_Count = testmodules_SequenceEx.Count
        for i in range(1, testmodules_SequenceEx_Count + 1):
            testmodules_SequenceEx.Item(i).Enabled = False
        if testsequencename is None:
            testmodules_SequenceEx_item = testmodules_SequenceEx.Item(1)
        else:
            testmodules_SequenceEx_item = testmodules_SequenceEx.Item(testsequencename)
        print("testmodules_SequenceEx_item enable:", testmodules_SequenceEx_item.Enabled)
        testmodules_SequenceEx_item_sequence = testmodules_SequenceEx_item.SequenceEx
        testcase_except = []
        for i in testcases:
            try:
                testcaseinfos = testmodules_SequenceEx_item_sequence.Item(i)
                testcaseinfos.Enabled = True
                print("Name:%s,Ident:%s,Type:%s,Enabled:%s,Verdict:%s" % (
                testcaseinfos.Name, testcaseinfos.Ident,
                testcaseinfos.Type, testcaseinfos.Enabled,
                testcaseinfos.Verdict))
            except:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test.py")
                testcase_except.append(i)
        return testcase_except

    def EnableTestModuleTestcase_test(self, testcases, testsequencename, testmoduleindex=1, testenvindex=1):
        #testenvironment_name = self.App.Configuration.TestSetup.TestEnvironments.Name   error:no Name attribute
        # testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item(testenvindex)
        testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item("Test Environment")
        testenvironment = CastTo(testenvironment, "ITestEnvironment2")
        testmodule = testenvironment.TestModules.Item("Test 24")
        # testmodule = testenvironment.TestModules.Item(testmoduleindex)
        # testmodules_Sequence = testmodule.Sequence
        testmodule = CastTo(testmodule, "ITSTestModule7")
        testmodules_SequenceEx = testmodule.SequenceEx
        testmodules_SequenceEx_Count = testmodules_SequenceEx.Count
        print("testmodules_SequenceEx_Count:",testmodules_SequenceEx_Count)
        for i in range(1, testmodules_SequenceEx_Count + 1):
            testmodules_SequenceEx.Item(i).Enabled = False
            print("name:",testmodules_SequenceEx.Item(i).Name)
            print("count:",testmodules_SequenceEx.Item(i).SequenceEx.Count)

    def EnableTestModuleTestcaseV2(self, testcases, testsequencename, testmodulename, testenvname):
        try:
            testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item(testenvname)
            testenvironment = CastTo(testenvironment, "ITestEnvironment2")
            testmodule = testenvironment.TestModules.Item(testmodulename)
            if (testsequencename is None) or (testcases is None):
                testmodule.Enabled = True
                return True
            else:
                # testmodules_Sequence = testmodule.Sequence
                testmodule = CastTo(testmodule, "ITSTestModule7")
                testmodules_SequenceEx = testmodule.SequenceEx
                testmodules_SequenceEx_Count = testmodules_SequenceEx.Count
                for i in range(1, testmodules_SequenceEx_Count + 1):
                    testmodules_SequenceEx.Item(i).Enabled = False
                if testsequencename is None:
                    testmodules_SequenceEx_item = testmodules_SequenceEx.Item(1)
                else:
                    testmodules_SequenceEx_item = testmodules_SequenceEx.Item(testsequencename)
                print("testmodules_SequenceEx_item enable:", testmodules_SequenceEx_item.Enabled)
                if testcases == "*":
                    testmodules_SequenceEx_item.Enabled = True
                    return True
                elif isinstance(testcases,list):
                    testmodules_SequenceEx_item_sequence = testmodules_SequenceEx_item.SequenceEx
                    testcase_except = []
                    for i in testcases:
                        try:
                            testcaseinfos = testmodules_SequenceEx_item_sequence.Item(i)
                            testcaseinfos.Enabled = True
                            print("Name:%s,Ident:%s,Type:%s,Enabled:%s,Verdict:%s" % (
                            testcaseinfos.Name, testcaseinfos.Ident,
                            testcaseinfos.Type, testcaseinfos.Enabled,
                            testcaseinfos.Verdict))
                        except:
                            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test.py")
                            testcase_except.append(i)
                    return testcase_except
                else:
                    return False
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/test.py")
            return False

    def GetTestModuleTestcase(self, testcases, testenvindex=1, testmoduleindex=1, testsequenceindex=1):
        testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item(testenvindex)
        testenvironment = CastTo(testenvironment, "ITestEnvironment2")
        testmodule = testenvironment.TestModules.Item(testmoduleindex)
        testmodule = CastTo(testmodule, "ITSTestModule7")
        testmodules_SequenceEx = testmodule.SequenceEx
        testmodules_SequenceEx_item = testmodules_SequenceEx.Item(testsequenceindex)
        print("testmodules_SequenceEx_item enable:", testmodules_SequenceEx_item.Enabled)
        testmodules_SequenceEx_item_sequence = testmodules_SequenceEx_item.SequenceEx
        for i in testcases:
            testcaseinfos = testmodules_SequenceEx_item_sequence.Item(i)
            testcaseinfos.Enabled = True
            print("Name:%s,Ident:%s,Type:%s,Enabled:%s,Verdict:%s" % (
                testcaseinfos.Name, testcaseinfos.Ident,
                testcaseinfos.Type, testcaseinfos.Enabled,
                testcaseinfos.Verdict))

    def GetTestModuleTestcaseV2(self, testcases, testsequencename, testmodulename, testenvname):
        testenvironment = self.App.Configuration.TestSetup.TestEnvironments.Item(testenvname)
        testenvironment = CastTo(testenvironment, "ITestEnvironment2")
        testmodule = testenvironment.TestModules.Item(testmodulename)
        testmodule = CastTo(testmodule, "ITSTestModule7")
        testmodules_SequenceEx = testmodule.SequenceEx
        testmodules_SequenceEx_item = testmodules_SequenceEx.Item(testsequencename)
        print("testmodules_SequenceEx_item enable:", testmodules_SequenceEx_item.Enabled)
        testmodules_SequenceEx_item_sequence = testmodules_SequenceEx_item.SequenceEx
        for i in testcases:
            testcaseinfos = testmodules_SequenceEx_item_sequence.Item(i)
            testcaseinfos.Enabled = True
            print("Name:%s,Ident:%s,Type:%s,Enabled:%s,Verdict:%s" % (
                testcaseinfos.Name, testcaseinfos.Ident,
                testcaseinfos.Type, testcaseinfos.Enabled,
                testcaseinfos.Verdict))

    def RunTestModules(self):
        testenvs = self.App.Configuration.TestSetup.TestEnvironments
        self.TestModules = []
        for c in range(1, testenvs.Count + 1):
            testenv = CastTo(testenvs.Item(c), "ITestEnvironment2")
            self.TraverseTestItem(testenv, lambda tm: self.TestModules.append(CanoeTestModule(tm)))
        """ starts all test modules and waits for all of them to finish"""
        # start all test modules
        for tm in self.TestModules:
            tm.Start()
        # wait for test modules to stop
        # while not any([not tm.Enabled or tm.IsDone() or tm.ReportGenerate() for tm in self.TestModules]):
        #     DoEvents()

        # wait for test modules to stop and report generated succeed
        while not any([not tm.Enabled or tm.IsDone() and tm.ReportGenerate() for tm in self.TestModules]):
            DoEvents()

        for tm in self.TestModules:
            tm.Report_Generate()

    def RunTestModules_test(self):
        self.TestSetup = self.App.Configuration.TestSetup
        testenv_count = self.TestSetup.TestEnvironments.Count
        print("testenv_count:",testenv_count)
        testenv = self.TestSetup.TestEnvironments.Item(1)
        testenv = CastTo(testenv, "ITestEnvironment2")
        testmodules = testenv.TestModules
        testmodules_count = testmodules.Count
        print("testmodules_count:",testmodules_count)
        ts_testmodule = testmodules.Item(1)
        print("fullname:",ts_testmodule.FullName)
        print("name:",ts_testmodule.Name)
        print("path:",ts_testmodule.Path)
        '''
        testenv = self.TestSetup.TestEnvironments.Item(1)
        testenv = CastTo(testenv, "ITestEnvironment2")
        # TestModules property to access the test modules
        self.TestModules = []
        self.TraverseTestItem(testenv, lambda tm: self.TestModules.append(CanoeTestModule(tm)))
        """ starts all test modules and waits for all of them to finish"""
        # start all test modules
        for tm in self.TestModules:
            tm.Start()
        # wait for test modules to stop
        while not any([not tm.Enabled or tm.IsDone() for tm in self.TestModules]):
            DoEvents()
        '''

    def RunTestConfigs(self):
        """ starts all test configurations and waits for all of them to finish"""
        # start all test configurations
        for tc in self.TestConfigs:
            tc.Start()

        # wait for test modules to stop
        while not all([not tc.Enabled or tc.IsDone() for tc in self.TestConfigs]):
            DoEvents()

    def RunTestConfigs_SaveLast(self):
        tstconfigurations = self.App.Configuration.TestConfigurations
        self.TestConfigs = []
        for c in range(1, tstconfigurations.Count + 1):
            self.TestConfigs.append(CanoeTestConfiguration(tstconfigurations.Item(c)))
        """ starts all test configurations and waits for all of them to finish"""
        tcs = list(filter(lambda i: i.Enabled == True, self.TestConfigs))
        """ starts all test configurations and waits for all of them to finish"""
        # start all test configurations
        for tc in tcs:
            tc.Start()

        # wait for test modules to stop
        # while not all([not tc.Enabled or tc.IsDone() for tc in tcs]):
        #     DoEvents()

        # wait for test modules to stop and report generated succeed
        while not all([not tc.Enabled or tc.IsDone() and tc.ReportGenerate() for tc in tcs]):
            DoEvents()

        for tc in tcs:
            tc.Report_Generate()

    def RunTestConfigs_CheckCANoeStop(self):
        tc = self.App.Configuration.TestConfigurations.Item(1)
        # tc.Name = testcfgname
        # TestConfigs property to access the test configuration
        self.TestConfigs = [CanoeTestConfiguration(tc)]

        for tc in self.TestConfigs:
            tc.Start()

        # wait for test modules to stop
        while self.Running():
            DoEvents()

    def TraverseTestItem(self, parent, testf):
        for test in parent.TestModules:
            testf(test)
        for folder in parent.Folders:
            found = self.TraverseTestItem(folder, testf)

    def VTSystem(self, vtcfg):
        self.vts = self.App.Configuration.VTSystem
        # Get the VT System configuration instance
        # Export and import a configuration
        # self.vts.ExportConfiguration("D:\MyConfiguration.vtcfg")
        self.vts.ImportConfiguration(vtcfg, 0)  # Appends to the current config
        # self.vts.ImportConfiguration("D:\MyConfiguration.vtcfg", 1)  # Replace current config
        # Create a new configuration based on the connected hardware
        # self.vts.NewConfigurationFromHardware()
        # Adapt the existing configuration to the connected hardware
        self.vts.AdaptToHardware()
        # Import a module description into CANoe
        # vts.ImportModuleDescription("D:\MyModuleDescription.xml")
        # Switch all modules offline/online
        self.vts.SetAllModulesOffline()
        self.vts.SetAllModulesOnline()
        # Access a module or channel by its name
        # myModule = vts.GetModuleByName("M1_VT1004")
        # myChannel = vts.GetChannelByName("M1_Ch1")
        self.App.Configuration.Save()

class CanoeAppEvents(object):
    """Handler for CANoe Application events"""
    def OnOpen(self,fullname):
        CanoeSync.AppOpened = True
        print("*** < CANoe Application CFG:%s Opened > ***" % fullname)

    def OnQuit(self):
        CanoeSync.AppStopped = True
        print("*** < CANoe Application closed > ***")

class CanoeMeasurementEventsbak(object):
    """Handler for CANoe measurement events"""

    def OnStart(self):
        CanoeSync.Started = True
        CanoeSync.Stopped = False
        print("< measurement started >")

    def OnStop(self):
        CanoeSync.Started = False
        CanoeSync.Stopped = True
        print("< measurement stopped >")

class CanoeMeasurementEvents(object):
    """Handler for CANoe measurement events"""

    def OnStart(self):
        CanoeSync.Started = True
        CanoeSync.Stopped = False
        print("< measurement started >")

    def OnStop(self):
        CanoeSync.Started = False
        CanoeSync.Stopped = True
        print("< measurement stopped >")


class CanoeTestModule:
    """Wrapper class for CANoe TestModule object"""

    def __init__(self, tm):
        self.tm = tm
        self.Events = DispatchWithEvents(tm, CanoeTestEvents)
        self.Name = tm.Name
        self.IsDone = lambda: self.Events.stopped
        self.ReportGenerate = lambda: self.Events.Report_Generate
        self.Enabled = tm.Enabled

    def Start(self):
        if self.tm.Enabled:
            self.tm.Start()
            self.Events.WaitForStart()

    def Report_Generate(self):
        if self.IsDone():
            self.Events.WaitForReportGenerate()

class CanoeTestConfiguration:
    """Wrapper class for a CANoe Test Configuration object"""

    def __init__(self, tc):
        self.tc = tc
        self.Name = tc.Name
        self.Events = DispatchWithEvents(tc, CanoeTestEvents)
        self.TestConfigureportGeneratEvents = DispatchWithEvents(tc.Report,CanoeTestConfigureportEvents)
        self.IsDone = lambda: self.Events.stopped
        self.ReportGenerate = lambda: self.TestConfigureportGeneratEvents.Report_Generate
        self.Enabled = tc.Enabled

    def Start(self):
        if self.tc.Enabled:
            self.tc.Start()
            self.Events.WaitForStart()

    def Report_Generate(self):
        if self.IsDone():
            self.TestConfigureportGeneratEvents.WaitForReportGenerate()

class CanoeTestEvents:
    """Utility class to handle the test events"""

    def __init__(self):
        self.started = False
        self.stopped = False
        self.Report_Generate = False
        self.WaitForStart = lambda: DoEventsUntil(lambda: self.started)
        self.WaitForStop = lambda: DoEventsUntil(lambda: self.stopped)
        self.WaitForReportGenerate = lambda: DoEventsUntil(lambda: self.Report_Generate)

    def OnStart(self):
        self.started = True
        self.stopped = False
        print("<", self.Name, " started >")

    def OnStop(self, reason):
        self.started = False
        self.stopped = True
        print("<", self.Name, " stopped >")

    def OnReportGenerated(self, success, sourceFullName, generatedFullName):
        if success:
            self.Report_Generate = True
            print("<", self.Name, " report Generated succeed. >")
            print("sourceFullName:", sourceFullName)
            print("generatedFullName:", generatedFullName)
        else:
            print("<", self.Name, " report Generated Failed. >")


class CanoeTestConfigureportEvents:
    """Utility class to handle the test configure report generate event"""

    def __init__(self):
        self.Report_Generate = False
        self.WaitForReportGenerate = lambda: DoEventsUntil(lambda: self.Report_Generate)

    def OnGenerated(self, success, sourceFullName, generatedFullName):
        if success:
            self.Report_Generate = True
            print("[INFO]<", self.FullPath, " report Generated succeed. >")
            print("sourceFullName:", sourceFullName)
            print("generatedFullName:", generatedFullName)
        else:
            print("[ERROR]<", self.FullPath, " report Generated Failed. >")


if __name__ == "__main__":
    app = CanoeSync()
    app.Stop()
    cfg_path = r"D:\jenkins_home\workspace\ZEEKR\ZEEKR_718BE028_ZECU_1_SMOKE_Level2\LIN_Interface\LIN_Interface\CANoeConfig\LIN_Interface.cfg"
    # cfg_path = r"D:\test\test01.cfg"
    app.Load(cfg_path)
    # app.LoadTestSetup(r"D:\test\b1.tse")
    # app.Start()
    # testcase_except = app.EnableTestModuleTestcase_test(["test091911"],None)
    # testcase_except = app.EnableTestModuleTestcaseV2(["LIN1_0x1C_sig_tx_CcvmCmdVlvCalibReq_ZCL_LIN1_ZCL_LIN1_startvalue"],"LIN1_TX_Sig_startvalue","Test 24","Test Environment")
    # print(testcase_except)
    testcase_except = app.EnableTestModuleTestcaseV2("*", "LIN1_TX_Sig_startvalue", "Test 24", "Test Environment")

    # app.GetTestModuleTestcaseV2(["LIN1_0x1C_sig_tx_CcvmCmdVlvCalibReq_ZCL_LIN1_ZCL_LIN1_startvalue"],"LIN1_TX_Sig_startvalue","Test 24","Test Environment")
    # app.RunTestModules()
    # app.Stop()
    # app.GetTestModuleTestcase(["test0919"])
    # app.savetestenvironment()
    # app.savecanoecfg()
    # app.app_quit()
    print("finished")
