import os

workers = 1  # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent"
# 采用gevent库，支持异步处理请求，提高吞吐量
bind = "{}:{}".format(os.environ.get('DOMAIN_NAME', '0.0.0.0'), os.environ.get('APP_PORT', '5000'))
