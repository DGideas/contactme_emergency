ContactMe @ emergency 支持使用 CI & CD 自动化流程进行部署，要进行自动化部署流程，首先需要构建具有适当权限(如`chmod u+wrx g+wrxs -R contactme && setfacl -R -d -m u::rwx -m g::rwx contactme`)的 `/opt/contactme` 目录，为 www-data 用户添加 CI&CD 流程的用户组权限。目录内提供如下文件:

/opt/contactme
  - venv/ - python3 -m venv 生成的生产环境 env
  - local_settings.py - 环境特定的 local_settings

同时，需要将对应的 service 添加到 /lib/systemd/system 中。

由于自动集成流程会在部署时自动重启服务，请使用 visudo 添加如下行:

ALL ALL=NOPASSWD: /usr/bin/systemctl

同时需要在 Nginx 中进行如下配置:
```
server {
        server_name example.com;
        index index.html index.htm;
        root /var/www/contactme;
        listen 443 ssl http2;
        ssl_certificate /etc/nginx/cloudflare/public.pem;
        ssl_certificate_key /etc/nginx/cloudflare/private.pem;
        ssl_client_certificate /etc/nginx/cloudflare/cloudflare.crt;
        ssl_verify_client on;

        location / {
                include uwsgi_params;
                uwsgi_pass unix:/opt/contactme/contactme.sock;
        }
}

server {
        if ($host = example.com) {
                return 301 https://$host$request_uri;
        }
        server_name example.com;
        listen 80;
        return 404;
}
```
首次部署成功后，记得运行一下 scripts/ 里边的 init 打头的脚本，用于初始化数据。
