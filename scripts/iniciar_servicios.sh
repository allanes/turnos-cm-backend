#!/bin/bash

# Iniciar el servidor de backend
gnome-terminal -e "linux_iniciar_backend.sh"

# Iniciar el servicio de frontend del Simulador OTH
cd ../../turnos-cm-frontend
npm run start