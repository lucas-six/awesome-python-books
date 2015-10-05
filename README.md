# python
The Python Programming Language

## 阿里云管理脚本

```bash
cd admin

# 查看系统信息
$ python3 -O aliyun-admin.py sys --show

# 更新系统
$ sudo python3 -O aliyun-admin.py sys --update
```

### uWSGI服务

```bash
# 配置uWSGI Web服务(调试)
$ python3 aliyun-admin.py www --uwsgi 应用名称 最大内存

# 启动uWSGI服务（调试）
$ uwsgi uwsgii-app.ini

# 停止uWSGI服务（调试）
$ uwsgi --stop uwsgi-app.pid

# 重启uWSGI服务（调试）
$ uwsgi --reload uwsgi-app.pid

# 查看uWSGI日志（调试）
$ tail -f uwsgi-app.log
```

