#!/usr/bin/env bash

echo "Installing packages"
python -m pip install -e /app/* || exit

echo "Configuring database"
cd /flyway && flyway migrate

echo "Starting API"
python -m flask run --extra-files /app --host 0.0.0.0 --port 5000
