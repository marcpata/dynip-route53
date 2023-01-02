#!/bin/bash

while true; do
    # Ejecutar la aplicación de Python
    python ddns.py

    # Esperar 30 minutos antes de volver a ejecutar la aplicación
    sleep 1800
done
