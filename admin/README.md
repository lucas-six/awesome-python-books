# 系统管理

## 用户管理

```bash
# 新增用户
root# useradd <user-name>
root# passwd <user-name>

# 删除用户
root# userdel <user-name>
root# rm -rf /home/<user-name>

# 加入组
root# gpasswd -a <user-name> <grp>

# 退出组
root# gpasswd -d <user-name> <grp>

# sudo权限管理
root# visudo
root All=(ALL) ALL
%wheel ALL=(ALL) ALL
# %wheel ALL=(ALL) NOPASSWD: ALL
%<grp> ALL=<cmd> <args ...>

%mysql ALL=/sbin/service mysqld *
```

## 软件包管理

### CentOS

```bash
# 安装或更新软件包（在线）
$ sudo yum install <pkg>

# 卸载软件包（在线）
$ sudo yum remove <pkg>

# 安装或更新软件包（离线）
$ sudo rpm -Uvh <pkg>.rpm

# 卸载软件包（离线）
$ sudo rpm -e <pkg>.rpm
```

### Ubuntu

```bash
# 安装或更新软件包（在线）
$ sudo apt-get update
$ sudo apt-get install <pkg>

# 卸载软件包（在线）
$ sudo apt-get remove <pkg>
```
