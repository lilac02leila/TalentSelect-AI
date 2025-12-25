# Déploiement Rapide - TalentSelect AI

## Option 1 : Streamlit Cloud (5 minutes) ⭐ RECOMMANDÉ

### Étapes rapides :

1. **Pousser votre code sur GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Aller sur** https://share.streamlit.io/

3. **Se connecter avec GitHub**

4. **Cliquer sur "New app"** et remplir :
   - Repository : votre repo
   - Branch : `main`
   - Main file : `app.py`

5. **Configurer les secrets** (⚙️ Settings → Secrets) :
   ```toml
   GROQ_API_KEY=votre_cle_groq
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

6. **C'est tout !** L'app se déploie automatiquement.

---

## Option 2 : Docker (Local ou Serveur)

### Commandes rapides :

```bash
# Construire l'image
docker build -t talentselect-ai .

# Lancer le conteneur
docker run -d \
  -p 8501:8501 \
  -e GROQ_API_KEY=votre_cle_groq \
  --name talentselect-ai \
  talentselect-ai

# Ou avec docker-compose
docker-compose up -d
```

Accéder à : `http://localhost:8501`

---

## Option 3 : Local (Développement)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Installer spaCy français
python -m spacy download fr_core_news_sm

# Créer .env avec votre clé Groq
echo "GROQ_API_KEY=votre_cle_groq" > .env

# Lancer l'application
streamlit run app.py
```

---

## Obtenir une clé API Groq

1. Aller sur https://console.groq.com/
2. Créer un compte
3. Générer une clé API
4. Copier la clé dans vos variables d'environnement

---

## Besoin d'aide ?

Consultez `DEPLOYMENT.md` pour un guide détaillé avec toutes les options de déploiement.

