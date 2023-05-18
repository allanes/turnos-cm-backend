#!/bin/bash

# Set the environment variable for XWayland
export GDK_BACKEND=x11

# Launch the Chrome windows on each screen using the position and size information
google-chrome --new-window --start-fullscreen --app=http://localhost:3000/patientsView/1 &
firefox --new-window --kiosk http://localhost:3000/patientsView/2
