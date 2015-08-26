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

支持的系统常量：

- CPU物理核数和逻辑核数
- 操作系统名及版本

支持的操作：

- 更新（初始化）系统

'''

import sys
import platform
import subprocess
import argparse


# CPU物理核数
_shell_cmd_cpu_physical = 'cat /proc/cpuinfo | grep "physical id" | uniq | wc -l'
cpu_cores_physical = int(subprocess.check_output(_shell_cmd_cpu_physical,
        shell=True, universal_newlines=True))

# CPU逻辑核数
_shell_cmd_cpu_logical = 'cat /proc/cpuinfo| grep "processor" | uniq | wc -l'
cpu_cores_logical = int(subprocess.check_output(_shell_cmd_cpu_logical, 
        shell=True, universal_newlines=True))

os_name, os_version,  _ = platform.dist()


def shell_output(cmd):
    '''Run a shell command and return the result string.

    @param cmd shell command
    @return result string
    '''
    return subprocess.check_output(cmd, shell=True, universal_lines=True)


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


def sys_show():
    '''-s, --show选项.
    '''
    print('CPU: {} physical, {} logical'.format(cpu_cores_physical, cpu_cores_logical))
    print('OS: {}/{}'.format(os_name, os_version))


def update_system(init=False):
    '''更新（初始化）系统.
    '''
    if os_name == 'centos':
        if os_version >= '7.0':
            # 更新Yum系统
            subprocess.check_call('sudo yum install yum yum-utils deltarpm', shell=True)

            # 更新核心组件
            #
            # Python依赖包：openssl, openssl-devel, sqlite-devel
            subprocess.check_call('sudo yum install bash bash-completion sudo python coreutils \
                    binutils vim openssh openssh-server \
                    gcc gcc-c++ openssl openssl-devel \
                    sqlite-devel', shell=True)

            if init:
                # 源码编译并安装Python 3
                subprocess.check_call('./configure --prefix=/usr', shell=True)
                subprocess.check_call('make -j{}'.format(cpu_cores_logical), shell=True)
                subprocess.check_call('sudo make install', shell=True)

            # 安装Python拓展包(pip工具)
            #     $ sudo pip3 install --upgrade <python-pkg ...>
            subprocess.check_call('sudo pip3 install --upgrade pip pep8 uwsgi', shell=True)


if __name__ == '__main__':
    if platform.system() != 'Linux':
        sys.exit('Only support Linux')

    valid_commands = ['sys']

    # 设置命令行参数
    parser = argparse.ArgumentParser(description='Administrate Aliyun ECS.')
    parser.add_argument('commands', metavar='command', nargs='+', choices=valid_commands,
            help='one of {}'.format(valid_commands))
    parser.add_argument('-s', '--show', action='store_true',
            help='[sys] show the system configuration')
    parser.add_argument('-i', '--init', action='store_true', help='[sys] initialize the system')
    parser.add_argument('-u', '--update', action='store_true', help='[sys] update the system')

    # 解析命令行参数
    args = parser.parse_args()
    if 'sys' in args.commands:
        # -s, --show选项
        if args.show:
            sys_show()
        # -i, --init选项
        elif args.init:
            update_system(True)
        # -u, --update选项
        elif args.update:
            update_system()
        # 默认-s, --show选项
        else:
            sys_show()
