# flask-api-template

## setup ##

```
cp instance/config.py.sample instance/config.py
vim instance/config.py
chmod 777 var
cp adapter.wsgi.sample adapter.wsgi
vim adapter.wsgi
echo "CREATE DATABASE DB-name DEFAULT CHARACTER SET utf8" | mysql -u root -p
python3 manage.py setup_db
python3 manage.py scrape --mode=all
sudo vim /etc/httpd/conf.d/virtual.conf
```
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
sudo /etc/init.d/httpd restart

sudo vim /etc/crontab
```
00 23,7,15 * * *  root /usr/bin/python3 /var/www/sites/example.com/manage.py scrape > /dev/null
```
