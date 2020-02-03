Installation
============

### 1. Install required libraries ###

```
pip install -r requirements.txt
```

### 2. Setup ###
Edit configs for your env

```
cp adapter.wsgi.sample adapter.wsgi
cp instance/config.py.sample instance/config.py
vim adapter.wsgi
vim instance/config.py
chmod 777 var
```

### 2. WEB Server Setting ###

If use Apache, Edit config file like below.

```
sudo vim /etc/httpd/conf.d/virtual.conf

LoadModule wsgi_module /PATH-TO-SITE_PACKAGES/site-packages/mod_wsgi/server/mod_wsgi-py************.so
<VirtualHost *:80>
  ServerName example.com
  DocumentRoot /var/www/sites/example.com
  WSGIScriptAlias / /var/www/sites/example.com/adapter.wsgi
  <Directory "/var/www/sites/example.com/">
    Order deny,allow
    Allow from all
    #options Indexes FollowSymLinks +ExecCGI
  </Directory>
</VirtualHost>
```

And start web server.

```
sudo systemctl start httpd
```

