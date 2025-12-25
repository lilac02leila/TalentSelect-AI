#!/bin/bash

# Créer le dossier de configuration Streamlit
mkdir -p ~/.streamlit/

# Créer le fichier de configuration
cat > ~/.streamlit/config.toml <<EOF
[server]
headless = true
port = \$PORT
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
EOF

# Installer le modèle spaCy français si nécessaire
python -m spacy download fr_core_news_sm || true

echo "Configuration terminée!"

