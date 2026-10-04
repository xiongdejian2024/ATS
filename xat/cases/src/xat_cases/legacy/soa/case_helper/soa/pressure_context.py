#!/usr/bin/python3
# coding=UTF-8

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_cases.legacy.soa.case_helper.soa.check_doc import reset_log
from xat_cases.legacy.soa.case_helper.soa.domain.cdca import check_cdca_is_on
from xat_cases.legacy.soa.case_helper.soa.bootes_log_handler import rm_log, log_once_to_json, report_file
from xat_cases.legacy.soa.case_helper.soa.poweroff_strategy import PoweroffStrategy
from xat_ecu.legacy.common.logger import logger  as logging
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.pre_env_ioe import IoE_start
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.utils import check_bgm_is_on, get_obd_ip
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.push_docx import WikiTools
from xat_cases.legacy.soa.case_helper.codesrc.components.log_extractor.log_extractor import pull_log, init_extractor
from xat_cases.legacy.soa.case_helper.codesrc.public.utils.conf_parser import load_custom_settings
from xat_cases.legacy.soa.case_helper.codesrc.public.utils.utils import get_host_ip
from xat_cases.legacy.soa.case_helper.codesrc.public.utils.report import WechatTools



class PressureContext(object):
    def __init__(self, config, bgm_addr, cdca_addr, script_path, file_path, file_name,
                 bgm_version, cdca_version, tcam_version, acu_version, tc_config, nucapp=None) -> None:
        self._index = 1
        self._script_path = script_path
        self._file_path = file_path
        self._file_name = file_name
        self._bgm_version = bgm_version
        self._cdca_version = cdca_version
        self._tcam_version = tcam_version
        self._acu_version = acu_version
        self._bgm_addr = bgm_addr
        self._bgm_uname = config['bgm_uname']
        self._bgm_pwd = config['bgm_pwd']
        self._cdca_addr = cdca_addr
        self.nucapp = nucapp
        self.tc_config = tc_config
        self._analyzer_path = os.path.join(os.path.abspath(os.path.join(script_path, '../')), 'log_analyzer')

        self._strategy = [{'poweroff': ['bgm', 'cdc', 'acu', 'tcam']}]
        if config is not None:
            self._config = config
            self._times = config['times']
            self._space = config['space']
            self._title = config['title']
            if 'strategy' in config:
                self._strategy = config['strategy']
        else:
            logging.info('缺少传入配置')
            exit(1)
        self.wiki_uname = config['wiki_uname']
        self.wiki_pwd = config['wiki_pwd']
        self.wiki = WikiTools(
            driver_path=config['chrome_path'],
            options_list=[
                '--ignore-certificate-errors',
                '--ignore-ssl-errors',
                '--headless',
                '--no-sandbox',
                '--disable-dev-shm-usage',
            ],
        )

    def run(self, ipdu=None, sd=False):
        '''
        域控启动主流程
        '''
        json_msg ={
            "msgtype": "text",
            "text": {
            "content": f"运行备注::{get_host_ip()} \n当前压测环境版本信息：\nBGM:{self._bgm_version} \nCDC:{self._cdca_version}\nTCAM:{self._tcam_version}\nACU:{self._acu_version}\n环境准备完毕，即将运行压测程序\n此环境保存3天内压测日志，请及时备份日志到本地，谢谢！ \n预计占用时间（6-8小时）\n提醒大家暂时不要对此环境操作，谢谢！",
                }
            }
        WechatTools.log(json=json_msg)
        logging.info(f'self._strategy==》》 {self._strategy}')
        for item in self._strategy:
            if 'times' not in item:
                item['times'] = self._times
            if 'space' not in item:
                item['space'] = self._space
            if 'title' not in item:
                item['title'] = self._title
            self._poweroff_strategy = PoweroffStrategy(item, self.tc_config, self.nucapp)
            
            logging.info(f"poweroff={item.get('poweroff')}")
            if 'tcam' in item["poweroff"]:
                self.has_tcam=True
            else:
                self.has_tcam=False
            if not self._poweroff_strategy.times():
                continue    
            index = 1
            while index <= self._poweroff_strategy.times():
                logging.info(f'策略内循环。子序号: {index}')
                
                rm_log(self._bgm_uname, self._bgm_addr, self._bgm_pwd, self._cdca_addr, self._config['tcam_pwd'],
                self._config['acu_name'], self._config['acu_pwd'], self._index,item)
                logging.info('日志清理成功')
                
                if self.process(ipdu, sd):
                    index += 1
                    self._index += 1
                else:
                    logging.error(f'策略内循环执行失败，重新执行，再次清理日志。子序号: {index}')
                    index = index
                    rm_log(self._bgm_uname, self._bgm_addr, self._bgm_pwd, self._cdca_addr, self._config['tcam_pwd'],
                    self._config['acu_name'], self._config['acu_pwd'], self._index,item)

                
            docx_path = report_file(self._script_path, self._file_path, self._file_name, self._poweroff_strategy.titles())
            logging.info(f'docx_path ===== {docx_path}')
            try:
                self.wiki.login(wiki_url="https://wiki.jiduauto.com/pages/viewpage.action?pageId=820929570", username=self.wiki_uname, passwd=self.wiki_pwd)
                title = docx_path.split('/')[-1]
                logging.info(f'title ===== {title}')
                self.wiki.create_pages(title)
                wiki_url = self.wiki.import_docx(docx_path)
                logging.info(f'wiki_url ===== {wiki_url}')
            except Exception as e:
                logging.info(f'push wiki failed {e}')
                wiki_url = 'None'
            json_msg ={
                "msgtype": "text",
                "text": {
                "content": f"《{self._poweroff_strategy.titles()}的压力测试报告》\n运行备注:{get_host_ip()} \n当前压测环境版本信息：\nBGM: {self._bgm_version} \nCDC: {self._cdca_version}\nTCAM: {self._tcam_version}\nACU:{self._acu_version}\n压力测试继续进行\n报告wiki_url: {wiki_url}\n提醒大家暂时不要对此环境操作，\n此环境保存3天内压测日志，请及时备份日志到本地, 谢谢！",
                    }
                }
            WechatTools.log(json=json_msg)

        logging.info(f'循环执行完毕，开始解析！')
        # json_msg ={
        #     "msgtype": "text",
        #     "text": {
        #     "content": f"运行备注:{get_host_ip()} \n当前压测环境版本信息：\nBGM: {self._bgm_version} \nCDC: {self._cdca_version}\nTCAM: {self._tcam_version}\nACU:{self._acu_version}\n前{self._index}次压力测试报告\n压力测试继续进行\n报告wiki_url: {wiki_url}\n提醒大家暂时不要对此环境操作，\n此环境保存3天内压测日志，请及时备份日志到本地, 谢谢！",
        #         }
        #     }
        # WechatTools.log(json=json_msg)

    def process(self, ipdu=None, sd=False):
        if sd:
            logging.info("通过诊断命令重启四域环境")
            self._sd_reboot(ipdu)
        else:
            self._poweroffandon(ipdu)
            logging.info("cdc执行下电命令后，需要等待大概15秒左右才会下电")
            time.sleep(20)  

        logging.info("上下电后，obd_ip可能会变，重新获取一下")
        bgm_addr = get_obd_ip()
        logging.info(f"上下电后，obd_ip为{bgm_addr}")
        cdca_addr = f"{bgm_addr}:1313"
        self._bgm_addr = bgm_addr
        self._cdca_addr = cdca_addr
        IoE_start(self._bgm_addr, self._bgm_uname, self._bgm_pwd, force_flag=True)
        if self._precheck():
            self._wait()
            if not self._handle_log():
                return False
        else:
            logging.info(f"上电检查 Failed")
            return False
        return True

    def _poweroffandon(self, ipdu):
        logging.info(f'主流程开始。序号: {self._index}')
        self._poweroff_strategy.sd_reboot_domian(ipdu)
        if self.has_tcam:
            delay_time= 180
        else:
            delay_time= 0
        logging.info(f'重启后 延时{delay_time}秒')
        time.sleep(delay_time)
        
    def _poweroff(self):
        logging.info(f'主流程开始。序号: {self._index}')
        self._poweroff_strategy.poweroff()
        if self.has_tcam:
            delay_time= 30
        else:
            delay_time= 0
        logging.info(f'下电后 延时{delay_time}秒')
        time.sleep(delay_time)

    def _poweron(self):
        self._poweroff_strategy.poweron()
        if self.has_tcam:
            delay_time= 180 
        else:
            delay_time= 0
        logging.info(f'上电后 延时{delay_time}秒')
        time.sleep(delay_time)

    def _sd_reboot(self, ipdu):
        logging.info(f'主流程开始。序号: {self._index}')
        self._poweroff_strategy.sd_reboot_bgm()
        self._poweroff_strategy.sd_reboot_tcam(ipdu)
        self._poweroff_strategy.sd_reboot_cdc(ipdu)
        self._poweroff_strategy.sd_reboot_acu(ipdu)
        for domain_name in self._poweroff_strategy.powerons():
            if "sleep" in domain_name :
                logging.info(f'延时{domain_name[6:-1]}s')
                time.sleep(eval(domain_name.strip()[6:-1]))

        
            

    def _precheck(self):
        """
        1. 切换为ssh方式，不再检测tcam adb 连接情况
        2. 检查bgm ssh key,刷机后需要做一次
        """
        logging.info("上电成功,开始检查")
        res_cdca = check_cdca_is_on(self._cdca_addr)
        if res_cdca != 0:
            logging.error("cdca连接失败")
        # 检查bgm是否连接
        ssh_bgm = check_bgm_is_on(self._bgm_uname, self._bgm_addr, self._bgm_pwd)
        if not ssh_bgm:
            logging.error("bgm连接失败")
        if res_cdca == 0 and ssh_bgm:
            logging.info("cdca号已查询到, bgm已连接")
            return True
        else:
            return False

    def _wait(self):
        self._poweroff_strategy.wait()

    def _clear_log(self):
        """
        日志获取失败，清理拉取过的当次日志序号目录
        """
        os.system(f'rm -rf {os.path.join(self._file_path, str(self._index))}')
        return False

    def _handle_log(self):
        """
        拉取各域日志，完成后删除日志
        """
        cfgs = load_custom_settings(ver_type=-1)
        logging.debug("init_extractor bgm ")
        bgm_log_path = os.path.join(self._file_path, str(self._index), 'bgm')
        bgm_extractor = init_extractor(self._bgm_addr, cfgs, 'bgm', bgm_log_path)
        if not pull_log(bgm_extractor):
            return self._clear_log()
        reset_log(bgm_log_path)
        logging.debug("init_extractor cdca ")
        cdca_log_path = os.path.join(self._file_path, str(self._index), 'cdca')
        cdca_extractor = init_extractor(self._bgm_addr, cfgs, 'cdca', cdca_log_path)
        if not pull_log(cdca_extractor):
            return self._clear_log()
        reset_log(cdca_log_path)
        logging.debug("init_extractor cdcq ")
        cdcq_log_path = os.path.join(self._file_path, str(self._index), 'cdcq')
        cdcq_extractor = init_extractor(self._bgm_addr, cfgs, 'cdcq', cdcq_log_path)
        if not pull_log(cdcq_extractor):
            return self._clear_log()
        reset_log(cdcq_log_path)
        logging.debug("init_extractor tcam ")
        tcam_log_path = os.path.join(self._file_path, str(self._index), 'tcam')
        tcam_extractor = init_extractor(self._bgm_addr, cfgs, 'tcam', tcam_log_path)
        if not pull_log(tcam_extractor):
            return self._clear_log()
        reset_log(tcam_log_path)
        all_path = []
        logging.debug("init_extractor acu ")
        acu_log_path = os.path.join(self._file_path, str(self._index), 'acu')
        try:
            acu_extractor = init_extractor(self._bgm_addr, cfgs, 'acu', acu_log_path)
            if not pull_log(acu_extractor):
                logging.info(f'ACU 日志获取Failed')
            all_path.append(acu_log_path)
        except Exception as e:
            logging.info(f"handle_log error:  {e}")
        reset_log(acu_log_path)        
        # 开始一个子进程-生成单次json
        log_once_to_json(self._analyzer_path, os.path.join(self._file_path, str(self._index)))
        logging.info(f'第{self._index}次日志子进程同步转json')
        # 部分流程不下电日志较多，在转csv之前确保json能转化完成
        time.sleep(60)
        logging.info(f"日志拉取成功,清理日志")
        logging.info(f'主流程结束。序号: {self._index}')
        return True

