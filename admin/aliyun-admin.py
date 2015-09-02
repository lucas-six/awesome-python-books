#!/usr/bin/env python3

# Copyright (c) 2015 Li Yun <leven.cn@gmail.com>
# All Rights Reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

'''阿里云管理脚本(root 权限)

支持操作系统：

- CentOS 7.0

支持的操作：

- 更新（初始化）系统

'''

import os
import argparse
import random

import pylib


def default_tcp_keep_alive(t=None, intvl=None, probes=None):
    '''配置Linux系统默认的TCP Keep-Alive。

    @param t tcp_keepalive_time值，如果不为None，则修改成该值；如果为None，返回当前系统默认值
    @param intvl keep_alive_intvl值，如果不为None，则修改成该值；如果为None，返回当前系统默认值
    @param probes keep_alive_probes值，如果不为None，则修改成该值；如果为None，返回当前系统默认值
    @return a tuple of tcp_keepalive_time, keep_alive_intvl and keep_alive_probes
    @exception ValueError parameter error

    <h2>TCP Keep-Alive机制</h2>
    1. 每隔tcp_keepalive_time秒，发送心跳包。
    2. 如果主机可达，对方就会响应ACK应答，就认为是存活的。
    3. 如果可达，但应用程序退出，对方就发RST应答，发送TCP撤消连接。
    4 .如果可达，但应用程序崩溃，对方就发FIN消息。
    5. 如果对方主机不响应ACK, RST，每隔tcp_keepalive_intvl秒继续发送tcp_keepalive_probes次直到超时，就撤消连接。

    # 查看探测间隔时间（秒）
    $ sysctl net.ipv4.tcp_keepalive_time
    net.ipv4.tcp_keepalive_time = 7200

    # 查看当不可达时，重复发送探测的时间间隔（秒）
    $ sysctl net.ipv4.tcp_keepalive_intvl
    net.ipv4.tcp_keepalive_intvl = 75

    # 查看当不可达时，重复发送探测的次数
    $ sysctl net.ipv4.tcp_keepalive_probes
    net.ipv4.tcp_keepalive_probes = 9
    
    # 永久修改 /etc/sysctl.conf
    #
    #     net.ipv4.tcp_keepalive_time=1800
    #     net.ipv4.tcp_keepalive_intvl=1
    #     net.ipv4.tcp_keepalive_probes=9
    #
    # 使其生效
    $ sudo sysctl -p /etc/sysctl.conf
    ## Ubuntu/Debian
    ## $ sudo service procps restart
    '''
    # 修改
    if t is not None:
        if t < 0:
            raise ValueError('net.ipv4.tcp_keepalive_time 不能设置成负数')
        pylib.shell_output('sudo sysctl -w net.ipv4.tcp_keepalive_time={}'.format(t))
    if intvl is not None:
        if intvl < 0:
            raise ValueError('net.ipv4.tcp_keepalive_intvl 不能设置成负数')
        pylib.shell_output('sudo sysctl -w net.ipv4.tcp_keepalive_intvl={}'.format(intvl))
    if probes is not None:
        if probes < 0:
            raise ValueError('net.ipv4.tcp_keepalive_probes 不能设置成负数')
        pylib.shell_output('sudo sysctl -w net.ipv4.tcp_keepalive_probes={}'.format(probes))

    # 获取默认值
    keep_alive_time = int(pylib.shell_output('sysctl net.ipv4.tcp_keepalive_time'))
    keep_alive_intvl = int(pylib.shell_output('sysctl net.ipv4.tcp_keepalive_intvl'))
    keep_alive_probes = int(pylib.shell_output('sysctl net.ipv4.tcp_keepalive_probes'))

    return keep_alive_time, keep_alive_intvl, keep_alive_probes


def sys_show():
    '''-s, --show选项.
    '''
    print('CPU: {}/{} cores'.format(pylib.cpu_cores_physical, pylib.cpu_cores_logical))
    print('OS: {}/{}'.format(pylib.os_name, pylib.os_version))
    print('Python {}'.format(pylib.py_version))


def update_system():
    '''更新系统.
    '''
    if pylib.os_name == 'centos':
        if pylib.os_version >= '7.0':
            # 更新核心组件
            #
            # Python依赖包：openssl, openssl-devel, sqlite-devel
            pylib.pkgs_install(['bash', 'bash-completion', 'sudo', 'python', 'coreutils', 
                    'binutils', 'vim', 'openssh', 'openssh-server',
                    'gcc', 'gcc-c++', 'openssl', 'openssl-devel',
                    'sqlite-devel'])

            # 安装Python拓展包(pip工具)
            pylib.pip_install(['pep8'])


def www_uwsgi(max_requests=2000, app_name='app', max_mem=512, buffer_size=4, stats=None):
    '''配置uWSGI Web服务.

    @param max_requests 最大请求数
    @param app_name 应用名称
    @param max_mem 最大使用内存（单位：MB）,必须是2的倍数, 默认512MB。
    @param buffer_size 缓存大小 （单位：KB），必须是2的倍数，默认4KB。
    @param stats 监控端口号，None为不监控

    配置逻辑

        循环语句

            for = <x> <y> <z> ...
            ... %(_)
            endfor =

        条件语句

            环境变量是否设置

                if-env = <ENV>
                ...
                endif =

            文件是否存在

                if-exists = <file>
                ...
                endif =
 
            普通文件是否存在

                if-file = <regular-file>
                ...
                endif =

            目录是否存在

                if-dir = <dir>
                ...
                endif =

            配置选项是否存在

                if-opt = <option>
                ...
                endif

    @since uWSGI 2.0.11.1 (64bit)
    '''
    pylib.pip_install(['uwsgi'])

    # 端口绑定配置
    #
    # TODO
    #'https': ':1234,x.crt,x.key',
    #'http-socket': '127.0.0.1:1234',
    #'https-socket': '127.0.0.1:1234,x.crt,x.key',
    if __debug__:
        # Debug环境下，通过HTTP Web服务
        # 端口号为当前用户的ID加上1024
        port = os.getuid() + pylib.max_system_port
        port_config = 'http = :{}'.format(port)
    else:
        # 部署环境，采用内部通信方式，通过前段Web Server提供对外服务(nginx)
        # 端口号在1025-9999范围内
        port = random.randint(pylib.max_system_port+1, 9999)
        port_config = 'socket = 127.0.0.1:{}'.format(port)

    # 应用配置
    if __debug__:
        chdir = '.'
        procname_prefix = 'debug'
        pidfile_dir = '.'
        autoreload_config = 'py-autoreload = 2'
    else:
        chdir = '/var/spool/www'
        procname_prefix = 'stable'
        pidfile_dir = '/var/run'
        autoreload_config = ''

    # 监控配置
    if __debug__:
        log_dir = '.'
    else:
        log_dir = '/var/log'
    if stats is None:
        stats_config = ''
    else:
        assert isinstance(stats, int)
        stats_config = 'stats = 127.0.0.1:{}'.format(stats)

    # configparser module not used, because it don't support for '%'
    config_ini = '''# uWSGI 2.0.11.1 (64bit) 配置文件
# 由脚本自动生成，请勿修改

[uwsgi]
{port_config}

# Concurrency (并发)
master = true
processes = %k
reload-mercy = 8
threads = 2
enable-threads = true
offload-threads = %k
max-requests = {max_requests}

# 应用部署
chdir = {chdir}
wsgi-file = {app_name}.py
auto-procname = true
procname-prefix-spaced = {procname_prefix}
pidfile = {pidfile_dir}/%n.pid
{autoreload_config}
touch-reload = %n.ini

# I/O
limit-as = {max_mem}
reload-on-as = {reload_on_as}
reload-on-rss = {reload_on_rss}
cache = true
buffer-size = {buffer_size}

# Monitor (系统监控)
daemonize = {log_dir}/%n.log
#daemonize = 127.0.0.1:4000 UDP服务器
cpu-affinity = 1
no-orphans = true
memory-report = true
{stats_config}
'''.format(port_config=port_config, max_requests=max_requests, chdir=chdir, app_name=app_name,
        autoreload_config=autoreload_config, max_mem=max_mem, reload_on_as=max_mem//2,
        reload_on_rss=max_mem//4, buffer_size=buffer_size*1024, stats_config=stats_config,
        procname_prefix=procname_prefix, pidfile_dir=pidfile_dir, log_dir=log_dir)

    config_file = 'uwsgi-{}.ini'.format(app_name)
    if not __debug__:
        config_file = '/var/spool/www/' + config_file
    with open(config_file, 'w') as f:
        f.write(config_ini)


if __name__ == '__main__':
    valid_commands = ['sys', 'www']

    # 设置命令行参数
    parser = argparse.ArgumentParser(description='Administrate Aliyun ECS.')
    parser.add_argument('command', metavar='command', nargs=1, choices=valid_commands,
            help='one of {}'.format(valid_commands))
    parser.add_argument('-ss', '--show', action='store_true',
            help='[sys] show the system configuration')
    parser.add_argument('-su', '--update', action='store_true', help='[sys] update the system')
    parser.add_argument('-wu', '--uwsgi', action='store_true', help='[www] configure uWSGI')

    # 解析命令行参数
    args = parser.parse_args()
    if 'sys' in args.command:
        # -ss, --show选项
        if args.show:
            sys_show()
        # -su, --update选项
        elif args.update:
            update_system()
        # 默认-ss, --show选项
        else:
            sys_show()
    if 'www' in args.command:
        if not __debug__:
            os.makedirs('/var/spool/www', exist_ok=True)

        # -wu, --uwsgi选项
        if args.uwsgi:
            www_uwsgi()
        # 默认-wu, --uwsgi选项
        else:
            www_uwsgi()
