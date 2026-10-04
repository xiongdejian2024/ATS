#!/usr/bin/python3
# -*- coding=utf-8 -*-
'''
(C) Copyright Jidu Auto 2023-2023.
    @Author: Edison
    @Date: 2023-06-27
    @Description: 环境检查
    @Status: To verify
    @Docs: TODO
'''

import sys
from pathlib import Path

_forder = Path(__file__).resolve().parents[3]
sys.path.append(str(_forder))
from codesrc.public.utils import RemoteTools, RemoteToolsAdb, logger, load_custom_settings, save_results


class DomainConnction(object):
    '''
    暂时只适配了 v1.1.0
    '''

    # 设置timeout，避免阻塞
    timeout = 5

    def __init__(self, userinfo, ipaddr, ipport=22, dev_name='bgm', **kwargs):
        '''
        @param userinfo:
        @param ipaddr:
        @param ipport:
        @param dev_name: 域名称
        @param conn_method: 连接方法，默认为空（ssh），可选项为['ssh', 'adb']
        '''
        self._paswd = userinfo['passwd']
        self.dev_name = dev_name

        if 'conn_method' in kwargs:
            self.conn_method = kwargs['conn_method']
        else:
            self.conn_method = 'ssh'

        try:
            if self.conn_method == 'ssh':
                conn = RemoteTools(
                    host=ipaddr,
                    port=ipport,
                    user=userinfo['user'],
                    connect_kwargs={'password': userinfo['passwd'], 'timeout': self.timeout},
                )
                conn.open()
            else:
                conn = RemoteToolsAdb(ipaddr, port=ipport)
                conn.connect()
            self.conn = conn
        except Exception:
            self.conn = None

    @property
    def is_connected(self) -> bool:
        '''
        @desp: 校验是否能够成功连接
        '''
        msg = f'Connect to {self.dev_name}'
        res = False

        if self.conn is not None:
            try:
                out = self.run('pwd')
                logger.info(f'{msg} success. Current dir: {out}')
                res = True
            except Exception as e:
                logger.warning(f'{msg} failed. Error: {e}')
        else:
            logger.warning(f'{msg} failed. Error: Invalid connection.')
        return res

    def run(self, cmd, **kwargs):
        if self.conn_method == 'ssh':
            return self.conn.run(cmd, **kwargs)
        return self.conn.shell(cmd)

    def sudo(self, cmd, **kwargs):
        '''
        TODO: @jiahao.chen
        '''
        pass

    def get(self, remote_path, local_path, is_dir=False):
        if self.conn_method == 'ssh':
            # 当前get方法已对文件夹做了判断
            return self.conn.get(remote_path=remote_path, local_path=local_path)

        return self.conn.pull(remote_path, local_path, recursive=is_dir)


def conn_check(ipaddr, domain: str = None):
    '''
    @param ipaddr: obd's ip_addr
    @param domain: default is 'bgm'
    '''
    cfg_list = load_custom_settings(ver_type=-1)

    if domain is None:
        domain = 'bgm'
    if domain not in cfg_list.keys():
        logger.warning('Please choose a valid device')
        return False

    cfg = cfg_list[domain]
    checker = DomainConnction(
        cfg['userinfo'],
        ipaddr,
        ipport=cfg['ipinfo']['dport'],
        dev_name=domain,
        conn_method=cfg['conn_method'],
    )
    return checker.is_connected


if __name__ == '__main__':
    import optparse

    usage = ""
    opt_parser = optparse.OptionParser(usage)
    opt_parser.add_option('--ip', dest='ip', type='string', help="obd's ip addr")
    opt_parser.add_option('--domain', dest='domain', type='string', help="domain")
    opt_parser.add_option('--workspace', default='.', dest='workspace', type='string', help='result saving location')

    (options, args) = opt_parser.parse_args()
    res = conn_check(options.ip, domain=options.domain)

    if options.workspace:
        contents = {'errcode': 0, 'results': res}
        save_results(options.workspace, 'env_check', contents)
