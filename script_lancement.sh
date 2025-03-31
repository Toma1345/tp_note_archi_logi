#!/bin/bash

# Définition des chemins
dir_api="./api"
dir_venv="$dir_api/venv"
file_requirements="$dir_api/requirements.txt"
flask_pid_file="$dir_api/flask.pid"

kill -9 $(lsof -t -i:5000)

# Vérification et activation de l'environnement virtuel
if [ ! -d "$dir_venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv "$dir_venv"
    source "$dir_venv/bin/activate"
    echo "Installation des dépendances..."
    pip install -r "$file_requirements"
else
    echo "Activation de l'environnement virtuel..."
    source "$dir_venv/bin/activate"
fi

# Arrêt du Flask existant
stop_flask

# Lancement de l'API Flask
echo "Démarrage de l'API Flask..."
cd "$dir_api"
python api_rest.py &
flask_pid=$!
echo $flask_pid > "$flask_pid_file"
cd ..

# Installation des dépendances et lancement de l'application Vue.js
echo "Installation des dépendances Vue.js..."
npm install
echo "Démarrage de l'application Vue.js..."
npm run dev

# Nettoyage à la sortie
trap "stop_flask; exit" SIGINT SIGTERM