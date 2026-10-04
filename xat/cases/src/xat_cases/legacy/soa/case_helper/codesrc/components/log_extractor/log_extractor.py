#!/usr/bin/python3
# -*- coding=utf-8 -*-
'''
(C) Copyright Jidu Auto 2023-2023.
    @Author: Edison
    @Date: 2023-07-06
    @Description: log management
    @Status: In Progress
    @Docs: TODO
'''

import os
import sys
from pathlib import Path

_forder = Path(__file__).resolve().parents[3]
sys.path.append(str(_forder))
from codesrc.public.device.env_check import DomainConnction
from codesrc.public.utils import load_custom_settings, logger


class LogExtractor(DomainConnction):
    '''
    @desp: 拉日志功能
    '''

    def __init__(self, userinfo, ipaddr, ipport=22, dev_name='bgm', local_path=None, remote_path_list=None, **kwargs):
        '''
        @param userinfo:
        @param ipaddr:
        @param ipport:
        @param dev_name: 域名称
        @param conn_method: 连接方法，默认为空（ssh），可选项为['ssh', 'adb']
        @param local_path: 本地的日志存放路径
        @param remote_path_list: 远端的日志存放路径
        '''

        super().__init__(userinfo, ipaddr, ipport, dev_name, **kwargs)

        self.local_path = Path(local_path)
        self.remote_path_list = remote_path_list
        if 'conn_method' in kwargs:
            self.conn_method = kwargs['conn_method']
        else:
            self.conn_method = 'ssh'

    def init_local(self):
        self.local_path.mkdir(parents=True, exist_ok=True)

    def download(self, path, is_dir=False):
        '''
        @desp: 下载对应目录的日志
        '''
        try:
            self.get(path, self.local_path, is_dir=is_dir)
            if os.path.basename(path) in os.listdir(self.local_path):
                logger.info(f'Success download {path}')
            else:
                logger.warning(f'Failed download {path}')
                return False
            return True
        except Exception as e:
            logger.warning(f'Error while downloading log from {self.dev_name} - {path}. {e}')
            return False

    def download_all(self):
        '''
        @desp: 下载全部日志，默认都是文件夹
        '''
        for path in self.remote_path_list:
            if not self.download(path, is_dir=True):
                return False
        return True

    def remove(self, path):
        '''
        @desp: 删除对应目录的日志
        '''
        try:
            self.run(f'rm -rf {path}/*')
            return True
        except Exception as e:
            logger.warning(f'Error while removing log from {self.dev_name} - {path}. {e}')
            return False

    def remove_all(self):
        '''
        @desp: 删除所有日志
        '''
        for path in self.remote_path_list:
            logger.info(f'rm logs from: {path}')
            self.remove(path)


class BgmLogExtractor(LogExtractor):
    def __init__(self, userinfo, ipaddr, ipport=22, local_path=None, remote_path_list=None, **kwargs):
        super().__init__(
            userinfo,
            ipaddr,
            ipport=ipport,
            dev_name='bgm',
            local_path=local_path,
            remote_path_list=remote_path_list,
            **kwargs,
        )
        self._passwd = userinfo['passwd']

    def download_all(self):
        '''
        @desp: override
            这里处理比较特殊，为了兼容现稳定版本，针对"/log"文件夹单独处理
        '''
        try:
            self.run(f'echo {self._paswd} | sudo -S chmod a+r /log/ -R')
            remote_path = '/log/'
            logger.info("下载路径: /log/")
            log_file = []
            files = self.conn.run(f'ls {remote_path}')
            logger.info(f"文件夹log中的文件有{files}")
            for file in str(files).split():
                if 'log' in file or 'bootes' in file or 'coredump' in file:
                    log_file.append(file)
            logger.info(f"需要下载的文件有{log_file}")
            for f in log_file:
                l_path = self.local_path / f
                r_path = remote_path + '/' + f
                self.get(remote_path=r_path, local_path=l_path)
            return True
        except Exception as e:
            logger.warning(f'Error while downloading log from {self.dev_name}. {e}')
            return False

    def remove_all(self):
        '''
        @desp: override
            这里处理比较特殊，为了兼容现稳定版本，针对"/log"文件夹单独处理
        '''
        try:
            self.run(f'echo {self._paswd} | sudo -S chmod a+r /log/ -R')
            remote_path = '/log/'
            log_file = []
            for file in str(self.conn.run(f'ls {remote_path}')).split():
                if 'log' in file or 'bootes' in file or 'coredump' in file:
                    log_file.append(file)
            print(log_file)
            for f in log_file:
                r_path = remote_path + '/' + f
                self.run(f'echo {self._paswd} | sudo -S rm -rf {r_path}')
            return True
        except Exception as e:
            logger.warning(f'Error while removing log from {self.dev_name}. {e}')
            return False


class CdcqLogExtractor(LogExtractor):
    def __init__(self, userinfo, ipaddr, ipport, local_path=None, remote_path_list=None, **kwargs):
        super().__init__(
            userinfo,
            ipaddr,
            ipport=ipport,
            dev_name='cdcq',
            local_path=local_path,
            remote_path_list=remote_path_list,
            **kwargs,
        )

    def remove_all(self):
        '''
        @desp: cdcq先做mount再进行删除操作
        '''
        self.run(f'/ifs/bin/mount -urw /mnt')
        for path in self.remote_path_list:
            logger.info(f'rm logs from: {path}')
            self.remove(path)

    def remove(self, path):
        '''
        @desp: cdcq删除对应目录的日志需指定rm位置
        '''
        try:
            self.run(f'/mnt/bin/rm -rf {path}/*')
            return True
        except Exception as e:
            logger.warning(f'Error while removing log from {self.dev_name} - {path}. {e}')
            return False


class CdcaLogExtractor(LogExtractor):
    def __init__(self, userinfo, ipaddr, ipport, local_path=None, remote_path_list=None, **kwargs):
        super().__init__(
            userinfo,
            ipaddr,
            ipport=ipport,
            dev_name='cdca',
            local_path=local_path,
            remote_path_list=remote_path_list,
            **kwargs,
        )


class TcamLogExtractor(LogExtractor):
    def __init__(self, userinfo, ipaddr, ipport, local_path=None, remote_path_list=None, **kwargs):
        super().__init__(
            userinfo,
            ipaddr,
            ipport=ipport,
            dev_name='tcam',
            local_path=local_path,
            remote_path_list=remote_path_list,
            **kwargs,
        )


class AcuLogExtractor(LogExtractor):
    def __init__(self, userinfo, ipaddr, ipport, local_path=None, remote_path_list=None, **kwargs):
        super().__init__(
            userinfo,
            ipaddr,
            ipport=ipport,
            dev_name='acu',
            local_path=local_path,
            remote_path_list=remote_path_list,
            **kwargs,
        )


EXTRACTOR_LIST = {
    'bgm': BgmLogExtractor,
    'cdcq': CdcqLogExtractor,
    'cdca': CdcaLogExtractor,
    'tcam': TcamLogExtractor,
    'acu': AcuLogExtractor,
}


def init_extractor(ipaddr, cfg_list, domain: str = None, local_path=Path.cwd()):
    '''
    @desp: 初始化extractor
    '''
    if domain is None:
        domain = 'bgm'
    if domain not in cfg_list.keys():
        logger.warning('Please choose a valid device')
        return False

    cfg = cfg_list[domain]
    extractor = EXTRACTOR_LIST[domain](
        cfg['userinfo'],
        ipaddr,
        ipport=cfg['ipinfo']['dport'],
        conn_method=cfg['conn_method'],
        local_path=local_path,
        remote_path_list=cfg['remote_settings']['log_path'],
    )

    extractor.init_local()
    return extractor


def pull_log(extractor):
    '''
    @desp: 拉取extractor目标域日志
    '''
    return extractor.download_all()


def remove_log(extractor):
    '''
    @desp: 清空extractor目标域日志
    '''
    extractor.remove_all()


if __name__ == '__main__':
    # import optparse

    # logger.info(f'{_forder}')
    # # 所有域: domain_list = ['bgm', 'cdca', 'cdcq', 'tcam', 'acu']

    # usage = "log_extractor --ip xx.xx.xx.xx --domain bgm"
    # opt_parser = optparse.OptionParser(usage)
    # opt_parser.add_option('--ip', dest='ip', type='string', help="obd's ip addr")
    # opt_parser.add_option('--domain', dest='domain', type='string', help="domain")
    # opt_parser.add_option('--dest', dest='local_path', type='string', help="path to log save")
    # opt_parser.add_option('--remove', dest='remove', default=False, action='store_true', help='Pull log')

    # (options, args) = opt_parser.parse_args()

    # dev_name = options.domain

    # if options.local_path:
    #     local_path = Path(options.local_path)
    # else:
    #     local_path = Path('build_results') / 'app_run' / 'pull_log'
    # local_path = local_path / dev_name

    # cfgs = load_custom_settings(-1)
    # instance = init_extractor(options.ip, cfgs, options.domain, local_path=local_path)
    # if options.remove:
    #     remove_log(instance)
    # else:
    #     pull_log(instance)
    print("init_extractor bgm ")
    cfgs = load_custom_settings(ver_type=-1)
    bgm_log_path = os.path.join("./logs/", 'bgm')
    bgm_extractor = init_extractor("169.254.1.1", cfgs, 'bgm', bgm_log_path)
    pull_log(bgm_extractor)
