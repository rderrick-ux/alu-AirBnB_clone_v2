#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static.

# Install Nginx if it is not already installed
apt-get update
apt-get install -y nginx

# Create the required folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test the Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create (or recreate) the symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group, recursively
chown -R ubuntu:ubuntu /data/

# Overwrite the default Nginx site config to serve /data/web_static/current/
# at /hbnb_static/ using an alias. Writing the whole block avoids depending on
# any pre-existing line (server_name differs across Nginx/Ubuntu versions).
printf '%s\n' "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm;
    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}" > /etc/nginx/sites-available/default

# Restart Nginx to apply the new configuration
service nginx restart
