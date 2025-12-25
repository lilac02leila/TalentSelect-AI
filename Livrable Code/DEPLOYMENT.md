# Guide de Déploiement - TalentSelect AI

Ce guide vous accompagne dans le déploiement de l'application TalentSelect AI sur différentes plateformes.

## Table des Matières

1. [Déploiement sur Streamlit Cloud](#déploiement-sur-streamlit-cloud) ⭐ Recommandé
2. [Déploiement avec Docker](#déploiement-avec-docker)
3. [Déploiement sur Heroku](#déploiement-sur-heroku)
4. [Déploiement sur Railway](#déploiement-sur-railway)
5. [Déploiement sur un serveur VPS](#déploiement-sur-un-serveur-vps)
6. [Configuration des variables d'environnement](#configuration-des-variables-denvironnement)
7. [Dépannage](#dépannage)

---

## Déploiement sur Streamlit Cloud ⭐

**Streamlit Cloud** est la solution la plus simple et gratuite pour déployer des applications Streamlit.

### Prérequis

- Un compte GitHub
- Un compte Streamlit Cloud (gratuit) : https://share.streamlit.io/
- Une clé API Groq

### Étapes

#### 1. Préparer le dépôt GitHub

1. **Créer un dépôt GitHub** (si ce n'est pas déjà fait) :
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/votre-username/votre-repo.git
   git push -u origin main
   ```

2. **Vérifier que les fichiers suivants sont présents** :
   - `app.py` (fichier principal)
   - `requirements.txt` (dépendances)
   - `.gitignore` (pour exclure les fichiers sensibles)

#### 2. Créer un fichier de configuration Streamlit (optionnel)

Créez un dossier `.streamlit` et un fichier `config.toml` :

```bash
mkdir .streamlit
```

Créez `.streamlit/config.toml` :
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

#### 3. Déployer sur Streamlit Cloud

1. **Aller sur** https://share.streamlit.io/
2. **Se connecter** avec votre compte GitHub
3. **Cliquer sur "New app"**
4. **Remplir le formulaire** :
   - **Repository** : Sélectionner votre dépôt
   - **Branch** : `main` (ou `master`)
   - **Main file path** : `app.py`
5. **Cliquer sur "Deploy"**

#### 4. Configurer les variables d'environnement

1. **Dans la page de votre app déployée**, cliquer sur "⚙️ Settings"
2. **Aller dans "Secrets"**
3. **Ajouter les variables suivantes** :
   ```toml
   GROQ_API_KEY=votre_cle_groq_ici
   GROQ_MODEL=llama-3.3-70b-versatile
   ```
4. **Sauvegarder**

#### 5. Redéployer

L'application se redéploie automatiquement. Attendez quelques minutes.

### Avantages

- ✅ Gratuit
- ✅ Déploiement automatique à chaque push
- ✅ HTTPS inclus
- ✅ Pas de configuration serveur nécessaire

### Limitations

- ⚠️ Les données sont stockées temporairement (perdues au redémarrage)
- ⚠️ Limites de ressources (CPU/RAM)
- ⚠️ Timeout après 10 minutes d'inactivité

---

## Déploiement avec Docker

Docker permet de déployer l'application de manière portable sur n'importe quelle plateforme.

### Prérequis

- Docker installé
- Docker Compose (optionnel)

### Étapes

#### 1. Créer un Dockerfile

Créez un fichier `Dockerfile` à la racine du projet :

```dockerfile
FROM python:3.10-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer le modèle spaCy français
RUN python -m spacy download fr_core_news_sm

# Copier le code de l'application
COPY . .

# Exposer le port Streamlit
EXPOSE 8501

# Commande de démarrage
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 2. Créer un .dockerignore

Créez un fichier `.dockerignore` :

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.env
.git/
.gitignore
chroma_db/
data/raw/*
*.log
.DS_Store
```

#### 3. Construire l'image Docker

```bash
docker build -t talentselect-ai .
```

#### 4. Lancer le conteneur

```bash
docker run -d \
  -p 8501:8501 \
  -e GROQ_API_KEY=votre_cle_groq \
  -e GROQ_MODEL=llama-3.3-70b-versatile \
  --name talentselect-ai \
  talentselect-ai
```

#### 5. Accéder à l'application

Ouvrez votre navigateur à : `http://localhost:8501`

### Avec Docker Compose

Créez un fichier `docker-compose.yml` :

```yaml
version: '3.8'

services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GROQ_MODEL=${GROQ_MODEL:-llama-3.3-70b-versatile}
    volumes:
      - ./data:/app/data
      - ./chroma_db:/app/chroma_db
    restart: unless-stopped
```

Lancez avec :
```bash
docker-compose up -d
```

---

## Déploiement sur Heroku

### Prérequis

- Compte Heroku
- Heroku CLI installé
- Git

### Étapes

#### 1. Installer Heroku CLI

Téléchargez depuis : https://devcenter.heroku.com/articles/heroku-cli

#### 2. Se connecter à Heroku

```bash
heroku login
```

#### 3. Créer une application Heroku

```bash
heroku create votre-app-name
```

#### 4. Créer un Procfile

Créez un fichier `Procfile` (sans extension) :

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### 5. Créer un fichier setup.sh

Créez `setup.sh` :

```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

#### 6. Modifier le Dockerfile pour Heroku

Ajoutez dans le Dockerfile (ou créez-en un) :

```dockerfile
# ... (contenu existant)

# Exécuter le script de configuration
RUN chmod +x setup.sh && ./setup.sh
```

#### 7. Configurer les variables d'environnement

```bash
heroku config:set GROQ_API_KEY=votre_cle_groq
heroku config:set GROQ_MODEL=llama-3.3-70b-versatile
```

#### 8. Déployer

```bash
git push heroku main
```

---

## Déploiement sur Railway

### Prérequis

- Compte Railway (https://railway.app/)
- GitHub account

### Étapes

1. **Aller sur** https://railway.app/
2. **Se connecter** avec GitHub
3. **Cliquer sur "New Project"** → **"Deploy from GitHub repo"**
4. **Sélectionner votre dépôt**
5. **Railway détecte automatiquement** que c'est une app Python
6. **Configurer les variables d'environnement** :
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
7. **Ajouter un service** → **"Generate Domain"** pour obtenir une URL publique

Railway détecte automatiquement `requirements.txt` et déploie l'application.

---

## Déploiement sur un serveur VPS

### Prérequis

- Serveur VPS (Ubuntu/Debian recommandé)
- Accès SSH
- Python 3.8+

### Étapes

#### 1. Se connecter au serveur

```bash
ssh utilisateur@votre-serveur.com
```

#### 2. Installer les dépendances système

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx
```

#### 3. Cloner le projet

```bash
git clone https://github.com/votre-username/votre-repo.git
cd votre-repo
```

#### 4. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Installer les dépendances

```bash
pip install -r requirements.txt
python -m spacy download fr_core_news_sm
```

#### 6. Créer un fichier .env

```bash
nano .env
```

Ajoutez :
```
GROQ_API_KEY=votre_cle_groq
GROQ_MODEL=llama-3.3-70b-versatile
```

#### 7. Créer un service systemd

Créez `/etc/systemd/system/talentselect.service` :

```ini
[Unit]
Description=TalentSelect AI Streamlit App
After=network.target

[Service]
Type=simple
User=votre-utilisateur
WorkingDirectory=/chemin/vers/votre-repo
Environment="PATH=/chemin/vers/votre-repo/venv/bin"
ExecStart=/chemin/vers/votre-repo/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 8. Activer et démarrer le service

```bash
sudo systemctl daemon-reload
sudo systemctl enable talentselect
sudo systemctl start talentselect
```

#### 9. Configurer Nginx (optionnel, pour HTTPS)

Créez `/etc/nginx/sites-available/talentselect` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activez le site :
```bash
sudo ln -s /etc/nginx/sites-available/talentselect /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 10. Configurer SSL avec Let's Encrypt (optionnel)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

---

## Configuration des variables d'environnement

### Variables requises

| Variable | Description | Exemple |
|----------|-------------|---------|
| `GROQ_API_KEY` | Clé API Groq (obligatoire) | `gsk_...` |
| `GROQ_MODEL` | Modèle Groq à utiliser (optionnel) | `llama-3.3-70b-versatile` |

### Où configurer

- **Streamlit Cloud** : Settings → Secrets
- **Heroku** : `heroku config:set VARIABLE=valeur`
- **Railway** : Variables tab
- **Docker** : `-e VARIABLE=valeur` ou fichier `.env`
- **VPS** : Fichier `.env` à la racine

---

## Dépannage

### L'application ne démarre pas

1. **Vérifier les logs** :
   ```bash
   # Docker
   docker logs talentselect-ai
   
   # Systemd
   sudo journalctl -u talentselect -f
   ```

2. **Vérifier les variables d'environnement** :
   ```bash
   # Vérifier que GROQ_API_KEY est définie
   echo $GROQ_API_KEY
   ```

3. **Vérifier les dépendances** :
   ```bash
   pip install -r requirements.txt
   python -m spacy download fr_core_news_sm
   ```

### Erreur "Module not found"

Réinstallez les dépendances :
```bash
pip install -r requirements.txt
```

### Erreur "spaCy model not found"

Téléchargez le modèle :
```bash
python -m spacy download fr_core_news_sm
```

### L'application est lente

- Réduire le nombre de candidats évalués
- Utiliser un modèle Groq plus rapide (ex: `llama-3.1-8b-instant`)
- Vérifier la connexion internet

### Port déjà utilisé

Changez le port dans la commande :
```bash
streamlit run app.py --server.port=8502
```

---

## Recommandations

### Pour un déploiement de production

1. **Utiliser HTTPS** (Let's Encrypt)
2. **Configurer un reverse proxy** (Nginx)
3. **Mettre en place des sauvegardes** pour `chroma_db/`
4. **Monitorer les logs** régulièrement
5. **Limiter l'accès** si nécessaire (authentification)
6. **Utiliser un service de gestion de secrets** (ex: AWS Secrets Manager)

### Sécurité

- ⚠️ **Ne jamais commiter** le fichier `.env` ou les clés API
- ⚠️ **Utiliser des variables d'environnement** pour les secrets
- ⚠️ **Limiter l'accès** à l'application si elle contient des données sensibles
- ⚠️ **Mettre à jour régulièrement** les dépendances

---

## Support

Pour toute question ou problème :
- Consultez les logs de l'application
- Vérifiez la documentation Streamlit : https://docs.streamlit.io/
- Consultez les autres fichiers de documentation du projet

