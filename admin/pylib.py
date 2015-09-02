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

- CPU核数（物理和逻辑）
- 操作系统名称及版本
- Python版本
- 系统保留的最大端口号
- MIME类型

- 执行shell命令
- 安装软件包
- 安装Python拓展包
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
_cmd_cpu_logical = 'cat /proc/cpuinfo | grep "processor" | uniq | wc -l'
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


# MIME类型
mime_types = '''
text/html                             html htm shtml;
text/css                              css;
text/xml                              xml;
image/gif                             gif;
image/jpeg                            jpeg jpg;
application/javascript                js;
application/atom+xml                  atom;
application/rss+xml                   rss;

text/mathml                           mml;
text/plain                            txt;
text/vnd.sun.j2me.app-descriptor      jad;
text/vnd.wap.wml                      wml;
text/x-component                      htc;

image/png                             png;
image/tiff                            tif tiff;
image/vnd.wap.wbmp                    wbmp;
image/x-icon                          ico;
image/x-jng                           jng;
image/x-ms-bmp                        bmp;
image/svg+xml                         svg svgz;
image/webp                            webp;

application/font-woff                 woff;
application/java-archive              jar war ear;
application/json                      json;
application/mac-binhex40              hqx;
application/msword                    doc;
application/pdf                       pdf;
application/postscript                ps eps ai;
application/rtf                       rtf;
application/vnd.apple.mpegurl         m3u8;
application/vnd.ms-excel              xls;
application/vnd.ms-fontobject         eot;
application/vnd.ms-powerpoint         ppt;
application/vnd.wap.wmlc              wmlc;
application/vnd.google-earth.kml+xml  kml;
application/vnd.google-earth.kmz      kmz;
application/x-7z-compressed           7z;
application/x-cocoa                   cco;
application/x-java-archive-diff       jardiff;
application/x-java-jnlp-file          jnlp;
application/x-makeself                run;
application/x-perl                    pl pm;
application/x-pilot                   prc pdb;
application/x-rar-compressed          rar;
application/x-redhat-package-manager  rpm;
application/x-sea                     sea;
application/x-shockwave-flash         swf;
application/x-stuffit                 sit;
application/x-tcl                     tcl tk;
application/x-x509-ca-cert            der pem crt;
application/x-xpinstall               xpi;
application/xhtml+xml                 xhtml;
application/xspf+xml                  xspf;
application/zip                       zip;

application/octet-stream              bin exe dll;
application/octet-stream              deb;
application/octet-stream              dmg;
application/octet-stream              iso img;
application/octet-stream              msi msp msm;

application/vnd.openxmlformats-officedocument.wordprocessingml.document    docx;
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet          xlsx;
application/vnd.openxmlformats-officedocument.presentationml.presentation  pptx;

audio/midi                            mid midi kar;
audio/mpeg                            mp3;
audio/ogg                             ogg;
audio/x-m4a                           m4a;
audio/x-realaudio                     ra;

video/3gpp                            3gpp 3gp;
video/mp2t                            ts;
video/mp4                             mp4;
video/mpeg                            mpeg mpg;
video/quicktime                       mov;
video/webm                            webm;
video/x-flv                           flv;
video/x-m4v                           m4v;
video/x-mng                           mng;
video/x-ms-asf                        asx asf;
video/x-ms-wmv                        wmv;
video/x-msvideo                       avi;
'''


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
