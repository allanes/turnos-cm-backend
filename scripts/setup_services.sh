#!/bin/bash

# Define the paths for your script files
SCRIPTS_PATH="/home/ados/Desktop/Proyectos/Facu/turnos-cm-backend/scripts"
RUN_BACKEND_SCRIPT="$SCRIPTS_PATH/linux_iniciar_backend.sh"
RUN_FRONTEND_SCRIPT="$SCRIPTS_PATH/linux_iniciar_frontend.sh"

# Replace 'your_user' with your Linux username
USERNAME="ados"

# Create the systemd service files
cat << EOF | sudo tee /etc/systemd/system/centro_medico_backend.service
[Unit]
Description=Run backend and frontend services

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStart=/bin/bash $RUN_BACKEND_SCRIPT
Restart=always

[Install]
WantedBy=mdefault.target
EOF

# Create the systemd service files
cat << EOF | sudo tee /etc/systemd/system/centro_medico_frontend.service
[Unit]
Description=Run backend and frontend services

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStart=/bin/bash $RUN_FRONTEND_SCRIPT
Restart=always

[Install]
WantedBy=default.target
EOF

# Enable and start the services
sudo systemctl enable centro_medico_backend.service
sudo systemctl enable centro_medico_frontend.service

echo "Services have been created and enabled. Restart system to check startup."
