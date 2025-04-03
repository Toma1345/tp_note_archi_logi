Thomas BROSSIER  
Antony PERDIEUS

# TP Noté Architecture logicielle

## Lancement du projet via le script de lancement

Depuis : `./`

```sh
bash script_lancement.sh
```

Dans le terminal, taper `o` puis cliquer sur la touche `entrée` de votre clavier

L'application se lance.

## Exécution manuelle du projet

### 1. Lancer l'API Flask

Depuis : `./api`

```sh
# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API Flask
python api_rest.py
```

### 2. Lancer l'application Vue.js

Depuis : `./`

```sh
# Installer les dépendances
npm install

# Lancer l'application Vue.js
npm run dev
```