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

