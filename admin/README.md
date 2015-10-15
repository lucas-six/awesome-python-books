# 系统管理

## 用户管理

```bash
# sudo权限管理
root# visudo
root All=(ALL) ALL
%wheel ALL=(ALL) ALL
# %wheel ALL=(ALL) NOPASSWD: ALL
%<grp> ALL=<cmd> <args ...>

%mysql ALL=/sbin/service mysqld *

# 查看用户登录日志（正常）
# /var/log/wtmp
$ last

# 查看用户登录日志（异常）
# /var/log/btmp
$ sudo lastb
```
