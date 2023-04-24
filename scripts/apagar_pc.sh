#!/bin/bash

# Cerrar ventanas de chrome
# Cerrar ventanas de firefox

sudo systemctl stop centro_medico_backend.service
sudo systemctl stop centro_medico_frontend.service

sudo systemctl poweroff
