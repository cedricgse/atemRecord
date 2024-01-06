# atemRecord

Application for timed recording on Atem Mini Pro

# Installation on Raspberry Pi

1. Clone this repo

   ```bash
   git clone https://github.com/cedricgse/atemRecord.git
   cd atemRecord
   ```
2. Make Virtual Environment

   ```bash
   python3 -m venv .venv
   ```
3. Install Python dependencies

   ```bash
   source .venv/bin/activate
   pip3 install -r requirements.txt
   deactivate
   ```
4. Install system dependencies

   ```bash
   sudo apt-get install at
   sudo apt-get install nginx
   ```
5. Configure nginx

   * Open uwsgi.ini

     ```bash
     nano uwsgi.ini
     ```
     and change`chdir=/home/raspiStream/atemRecord` to `chdir=/home/USERNAME/atemRecord`
   * Delete default site

     ```bash
     sudo rm /etc/nginx/sites-enabled/default
     ```
   * Create configuration file

     ```bash
     sudo nano /etc/nginx/sites-available/atemRecord
     ```
     with content:

     ```bash
     server {
       listen 80;
       server_name localhost;

       location / { try_files $uri @app; }
       location @app {
         include uwsgi_params;
         uwsgi_pass unix:/tmp/atemRecord.sock;
       }
     }
     ```
   * Create link

     ```bash
     sudo ln -s /etc/nginx/sites-available/atemRecord /etc/nginx/sites-enabled
     ```
   * Restart NGINX

     ```bash
     sudo systemctl restart nginx
     ```
6. Configure at permissions

   * remove 'www-data' in:

     ```bash
     sudo nano /etc/at.deny
     ```
7. Autostart at boot

   * Create service

     ```bash
     sudo nano /etc/systemd/system/uwsgi.service
     ```
     with content:

     ```bash
     [Unit]
     Description=uWSGI Service
     After=network.target

     [Service]
     User=www-data
     Group=www-data
     WorkingDirectory=/home/USERNAME/atemRecord
     ExecStart=sh startServer.sh

     [Install]
     WantedBy=multi-user.target

     ```
   * Restart daemon

     ```bash
     sudo systemctl daemon-reload
     ```
   * Start service

     ```bash
     sudo systemctl uwsgi.service
     ```
   * Check status

     ```bash
     sudo systemctl status uwsgi.service
     ```
     Should be "active (running)"
   * Cancel with CTRL-C and enable service to run on reboot

     ```bash
     systemctl enable uwsgi.service
     ```
8. Webinterface should now be showing up when browsing to IP of Pi
