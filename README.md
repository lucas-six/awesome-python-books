# python
The Python Programming Language

## 安装

### 安装依赖包

```bash
# CentOS 7.0
$ sudo yum install gcc-c++ openssl openssl-devel sqlite-devel
```

### 源码编译安装

```bash
$ ./configure --prefix=/usr
$ make -j4  ## 4 为CPU核数
$ sudo make install
```

## 阿里云管理脚本

```bash
cd admin

# 查看系统信息
python3 -O aliyun-admin.py sys

# 更新系统
python3 -O aliyun-admin.py sys --update

# 配置uWSGI Web服务
python3 -O aliyun-admin.py www --uwsgi
```

