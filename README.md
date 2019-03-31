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
