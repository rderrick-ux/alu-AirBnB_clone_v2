#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static.

# Install Nginx if not already installed
if ! command -v nginx > /dev/null 2>&1; then
    apt-get update
    apt-get install -y nginx
fi

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

# Update the Nginx configuration to serve /data/web_static/current/ to /hbnb_static
config="\\n\\tlocation /hbnb_static/ {\\n\\t\\talias /data/web_static/current/;\\n\\t}\\n"
sed -i "/server_name _;/a $config" /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
