#!/bin/bash

# Define the paths for your script files
SCRIPTS_PATH="/home/administrador/Escritorio/app_centro_medico/turnos-cm-backend/scripts"
RUN_BACKEND_SCRIPT="$SCRIPTS_PATH/linux_iniciar_backend.sh"
RUN_FRONTEND_SCRIPT="$SCRIPTS_PATH/linux_iniciar_frontend.sh"
RUN_ABRIR_TELES_SCRIPT="$SCRIPTS_PATH/abrir_teles.sh"

# Replace 'your_user' with your Linux username
USERNAME="administrador"

# Create the systemd service files
cat << EOF | sudo tee /etc/systemd/system/centro_medico_backend.service
[Unit]
Description=Run backend service

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStart=/bin/bash $RUN_BACKEND_SCRIPT
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create the systemd service files
cat << EOF | sudo tee /etc/systemd/system/centro_medico_frontend.service
[Unit]
Description=Run frontend service

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStart=/bin/bash $RUN_FRONTEND_SCRIPT
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the services
sudo systemctl enable centro_medico_backend.service
sudo systemctl enable centro_medico_frontend.service

echo "Services have been created and enabled. Restart system to check startup."
