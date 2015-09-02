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

'''Python 拓展库

支持系统：

- CentOS 7.0+

- Python 3.4.3+


包含：

- cpu_cores_physical
- cpu_cores_logical
- supported_os
- os_name
- os_version
- py_version

- shell_output()
'''

import sys
import platform
import subprocess


if platform.system() != 'Linux':
    sys.exit('Only support Linux')

py_version = sys.version_info[:3]
if py_version < (3, 4, 3):
    sys.exit('Only support Python 3.4.3+, current {}'.format(py_version))


def shell(cmd):
    '''执行shell命令. 当debug模式(__debug__为true)时，仅打印命令.

    @param cmd 待执行的shell命令
    '''
    if __debug__:
        print('[DEBUG] shell: '+cmd, file=sys.stderr)
    else:
        subprocess.check_call(cmd, shell=True)


def shell_output(cmd, debug_result=''):
    '''执行shell命令并返回字符串结果. 当debug模式(__debug__为true)时，仅打印命令.

    @param cmd 待执行的shell命令
    @return 结果字符串
    '''
    if __debug__:
        print('[DEBUG] shell: '+cmd, file=sys.stderr)
        return debug_result
    else:
        return subprocess.check_output(cmd, shell=True, universal_newlines=True)


# CPU物理核数
_cmd_cpu_physical = 'cat /proc/cpuinfo | grep "physical id" | uniq | wc -l'
cpu_cores_physical = int(shell_output(_cmd_cpu_physical, '1'))

# CPU逻辑核数
_cmd_cpu_logical = 'cat /proc/cpuinfo| grep "processor" | uniq | wc -l'
cpu_cores_logical = int(shell_output(_cmd_cpu_logical, '1'))


# 操作系统名称及版本
os_name, os_version,  _ = platform.dist()
supported_os = ('centos', 'ubuntu')
if os_name not in supported_os:
    sys.exit('Only support {}'.format(','.join(supported_os)))
if os_name == 'centos' and os_version < '7.0':
    sys.exit('Only support CentOS 7.0+, current {}'.format(os_version))
if os_name == 'ubuntu':
    raise NotImplementedError


# 网络常量
max_system_port = 1024  # 系统保留的端口号最大值


def pkgs_install(pkgs):
    '''安装软件包 (CentOS).

    @param pkgs 软件包列表
    '''
    cmd = 'sudo'
    if os_name == 'centos':
        # 更新Yum系统
        cmd += ' yum install yum yum-utils deltarpm'

        # 安装软件包
        cmd += ' {}'.format(' '.join(pkgs))
    shell(cmd)


def pip_install(pkgs):
    '''用pip安装Python拓展包.

    @param pkgs 拓展包列表

    $ sudo pip3 install --upgrade <python-pkg ...>
    '''
    cmd = 'sudo pip3 install --upgrade pip {}'.format(' '.join(pkgs))
    shell(cmd)


if __name__ == '__main__':
    print('Hello pylib!')
    print('Only support {}'.format(','.join(supported_os)))
