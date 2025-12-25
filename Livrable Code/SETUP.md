# Guide d'Installation et de Configuration

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API Groq (obtenez-la sur https://console.groq.com/)

## Installation

### 1. Cloner ou télécharger le projet

```bash
cd "projet machine learning candidate selection"
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Installer le modèle spaCy français

```bash
python -m spacy download fr_core_news_sm
```

### 5. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet :

```bash
cp .env.example .env
```

Éditez le fichier `.env` et ajoutez votre clé API Groq :

```
GROQ_API_KEY=votre_cle_groq_ici
GROQ_MODEL=llama-3.3-70b-versatile
```

## Structure des Données

### Candidats

Placez les CVs et lettres de motivation dans `data/raw/` :
- Formats supportés : PDF, DOCX, TXT
- Exemples fournis : `candidate_001.txt`, `candidate_002.txt`, `candidate_003.txt`

### Descriptions de Postes

Placez les descriptions de postes dans `data/job_descriptions/` :
- Format : fichiers texte (.txt)
- Exemple fourni : `data_scientist.txt`

## Lancement de l'Application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## Utilisation

1. **Accueil** : Vue d'ensemble du système
2. **Analyse Exploratoire** : Chargez et explorez les données des candidats
3. **Évaluation Multi-Agents** : Définissez un poste et évaluez les candidats
4. **Résultats** : Consultez le classement final avec justifications

## Dépannage

### Erreur : "spaCy model not found"
```bash
python -m spacy download fr_core_news_sm
```

### Erreur : "GROQ_API_KEY not found"
Vérifiez que le fichier `.env` existe et contient votre clé API Groq.

### Erreur : "No module named 'crewai'"
Réinstallez les dépendances :
```bash
pip install -r requirements.txt
```

## Notes

- La première utilisation peut prendre du temps pour créer les embeddings
- Les résultats sont stockés dans `chroma_db/` pour réutilisation
- Groq offre un quota gratuit généreux pour les tests
- Pour déployer l'application, consultez `DEPLOYMENT.md` ou `QUICK_DEPLOY.md`

