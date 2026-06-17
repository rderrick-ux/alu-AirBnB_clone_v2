#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx
apt-get update -y
apt-get install -y nginx

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a test HTML file
cat > /data/web_static/releases/test/index.html << 'HTMLEOF'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
HTMLEOF

# Remove existing symlink and recreate it
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve /hbnb_static using alias directive
python3 -c '
import re
with open("/etc/nginx/sites-available/default") as f:
    content = f.read()
content = re.sub(r"[ \t]*location\s+/hbnb_static\b[^}]*\}", "", content)
block = "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
content = content.replace("server_name _;", "server_name _;" + block, 1)
with open("/etc/nginx/sites-available/default", "w") as f:
    f.write(content)
'

# Restart Nginx
service nginx restart

exit 0
