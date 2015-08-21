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

- 更新Python 3环境

'''

import sys
import platform
import subprocess
import argparse


def shell_output(cmd):
    '''Run a shell command and return the result string.

    @param cmd shell command
    @return result string
    '''
    return subprocess.check_output(cmd, shell=True, universal_lines=True)


def cpu_cores():
    '''Get the CPU cores.

    @return a tuple of (physical cores, logical cores)
    '''
    # 查看CPU物理核数
    #     cat /proc/cpuinfo | grep "physical id" | uniq | wc -l
    physical_cores = int(shell_output('cat /proc/cpuinfo | grep "physical id" | uniq | wc -l'))

    # 查看CPU逻辑核数
    #     cat /proc/cpuinfo| grep "processor" | uniq | wc -l
    logical_cores = int(shell_output('cat /proc/cpuinfo | grep "processor" | uniq | wc -l'))
    return physical_cores, logical_cores


def get_default_tcp_keep_alive(t=None, intvl=None, probes=None):
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
        shell_output('sudo sysctl -w net.ipv4.tcp_keepalive_time={}'.format(t))
    if intvl is not None:
        if intvl < 0:
            raise ValueError('net.ipv4.tcp_keepalive_intvl 不能设置成负数')
        shell_output('sudo sysctl -w net.ipv4.tcp_keepalive_intvl={}'.format(intvl))
    if probes is not None:
        if probes < 0:
            raise ValueError('net.ipv4.tcp_keepalive_probes 不能设置成负数')
        shell_output('sudo sysctl -w net.ipv4.tcp_keepalive_probes={}'.format(probes))

    # 获取默认值
    keep_alive_time = int(shell_output('sysctl net.ipv4.tcp_keepalive_time'))
    keep_alive_intvl = int(shell_output('sysctl net.ipv4.tcp_keepalive_intvl'))
    keep_alive_probes = int(shell_output('sysctl net.ipv4.tcp_keepalive_probes'))

    return keep_alive_time, keep_alive_intvl, keep_alive_probes


def build_python_from_source(logical_cpu_cores=1):
    '''Build python from the source code.

    @param logical_cpu_cores number of CPU logical cores
    '''
    subprocess.check_call('./configure --prefix=/usr', shell=True)
    subprocess.check_call('make -j{}'.format(logical_cpu_cores), shell=True)
    subprocess.check_call('sudo make install', shell=True)


def install_or_update_pip_pkgs():
    '''Install or update python extension packages with pip.

    $ sudo pip3 install --upgrade <python-pkg ...>
    '''
    subprocess.check_call('sudo pip3 install --upgrade pip pep8', shell=True)


if __name__ == '__main__':
    if platform.system() != 'Linux':
        sys.exit('Only support Linux')

    # 设置命令行参数
    parser = argparse.ArgumentParser(description='Administrate Aliyun ECS.')
    parser.add_argument('commands', metavar='command', type=str, nargs='+',
                   help='a command to be executed, one of "upgrade-python", "upgrade-pip"')
    parser.add_argument('--foo', help='foo help')

    # 解析命令行参数
    _upgrade_python = False
    _upgrade_pip = False
    args = parser.parse_args()
    if 'upgrade-pip' in args.commands:
        _upgrade_pip = True
    if 'upgrade-python' in args.commands:
        _upgrade_python = True
        _upgrade_pip = True

    # 更新依赖包
    os_name, os_version,  _ = platform.dist()
    if os_name == 'centos':
        if os_version > '7.0':
            # 更新Yum
            subprocess.check_call('sudo yum install yum yum-utils deltarpm', shell=True)

            # 更新核心组件
            subprocess.check_call('sudo yum install bash bash-completion sudo python coreutils \
                    binutils vim openssh openssh-server gcc gcc-c++ openssl-devel', shell=True)

            # 更新Python依赖包
            if _upgrade_python:
                subprocess.check_call('sudo yum install sqlite-devel', shell=True)

    
    # 源码编译并安装
    if _upgrade_python:
        logical_cpu_cores, _ = cpu_cores()
        build_python_from_source(logical_cpu_cores)

    # 安装拓展包
    if _upgrade_pip:
        install_or_update_pip_pkgs()
