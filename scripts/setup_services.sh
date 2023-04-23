#!/bin/bash

# Define the paths for your script files
SCRIPTS_PATH="."
RUN_SERVICES_SCRIPT="$SCRIPTS_PATH/iniciar_servicios.sh"
OPEN_CHROME_WINDOWS_SCRIPT="$SCRIPTS_PATH/open_chrome_windows.sh"

# Replace 'your_user' with your Linux username
USERNAME="ados"

# Create the systemd service files
cat << EOF | sudo tee /etc/systemd/system/run_services.service
[Unit]
Description=Run backend and frontend services

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStart=/bin/bash $RUN_SERVICES_SCRIPT
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat << EOF | sudo tee /etc/systemd/system/open_chrome_windows.service
[Unit]
Description=Open Chrome windows on different screens
After=run_services.service

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$SCRIPTS_PATH
ExecStart=/bin/bash $OPEN_CHROME_WINDOWS_SCRIPT
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the services
sudo systemctl enable run_services.service
sudo systemctl enable open_chrome_windows.service

sudo systemctl start run_services.service
sudo systemctl start open_chrome_windows.service

echo "Services have been created, enabled, and started."
