#!/bin/bash

# Define the paths for your script files
SCRIPTS_PATH="/home/administrador/Escritorio/app_centro_medico/turnos-cm-backend/scripts"
NGROK_APP_PATH="$SCRIPTS_PATH/../ngrok_app"
FRONTEND_APP_PATH="$SCRIPTS_PATH/../../turnos-cm-frontend"

# Replace 'your_user' with your Linux username
USERNAME="administrador"

source $FRONTEND_APP_PATH/.env
source $NGROK_APP_PATH/.env

# Update nginx config file
cat << EOF | tee /etc/nginx/nginx.conf
events {
    worker_connections  1024;  ## Default: 1024
}
http {
    server {
        listen $NGINX_REVERSE_PROXY_PORT;
        location /static/ {
            proxy_pass http://localhost:$PORT;
        }
        location /manifest.json{
            proxy_pass http://localhost:$PORT;
        }
        location ~ /doctorsVie.+ {
            proxy_pass http://localhost:$PORT;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host 'localhost:$PORT';
            proxy_cache_bypass $http_upgrade;
        }
        location ~ /api/v1/doctors.+ {
            proxy_pass http://localhost:$PORT;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host 'localhost:$PORT';
            proxy_cache_bypass $http_upgrade;
        }        
    }
}

EOF

sudo service nginx restart