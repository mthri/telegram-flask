# Telegram Bot with Flask
## Using a self-signed SSL certificate and Gunicorn, then running as a systemd service on a VPS

You can get a free subdomain from [afraid](https://freedns.afraid.org/)

----
clone bot
```bash
cd /home
git clone github.com/mthri/telegram-flask
cd telegram-flask/
python3 -m venv venv
source venv/bin/active
pip3 install -r requirements.txt
```

----

### generate SSL certificate:
> make sure 'Common Name' matches your FQDN
```bash
openssl req -new -x509 -nodes -newkey rsa:2048 -keyout server.key -out server.crt -days 3650
```
---

### create systemd service
Create the service file with the command `sudo nano /etc/systemd/system/telegram-flask.service` then add the following code and save it:.
```
[Unit]
Description=Gunicorn instance to serve Telegram Bot
After=network.target

[Service]
WorkingDirectory=/home/telegram-flask
Environment="PATH=/home/telegram-flask/venv/bin"
ExecStart=/home/telegram-flask/venv/bin/gunicorn --certfile=/home/telegram-flask/server.crt --keyfile=/home/telegram-flask/server.key --bind 0.0.0.0:8443 wsgi:app

[Install]
WantedBy=multi-user.target
```

Next, run the following commands:
```bash
sudo systemctl daemon-reload
sudo systemctl start telegram-flask
sudo systemctl enable telegram-flask
```

**After making any changes, you must restart the service(`sudo systemctl restart telegram-flask`)**

---
**Credits:**

+ [leandrotoledo](https://gist.github.com/leandrotoledo/4e9362acdc5db33ae16c)
+ [rosehosting](https://www.rosehosting.com/blog/how-to-deploy-flask-application-with-nginx-and-gunicorn-on-ubuntu-20-04/)