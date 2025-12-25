# Guide d'Utilisation du Système Multi-Agents

## Vue d'Ensemble

Ce guide vous accompagne dans l'utilisation du système multi-agents pour la sélection de candidats.

## Workflow Complet

### Étape 1 : Préparation des Données

1. **Placer les CVs des candidats** dans `data/raw/`
   - Formats acceptés : PDF, DOCX, TXT
   - Nommage recommandé : `candidate_001.pdf`, `CV_002.txt`, etc.

2. **Placer la description de poste** dans `data/job_descriptions/`
   - Format : fichier texte (.txt)
   - Inclure : titre du poste, exigences techniques, soft skills recherchés

### Étape 2 : Analyse Exploratoire

1. Ouvrir l'application Streamlit
2. Aller dans la section **"Analyse Exploratoire"**
3. Cliquer sur **"Charger et Traiter les Candidats"**
4. Consulter les statistiques :
   - Nombre total de candidats
   - Expérience moyenne
   - Distribution des compétences
   - Visualisations

### Étape 3 : Évaluation Multi-Agents

1. Aller dans la section **"Évaluation Multi-Agents"**
2. **Entrer la description du poste** dans le champ texte
   - Vous pouvez copier depuis un fichier de `data/job_descriptions/`
   - Ou saisir directement

3. **Recherche RAG (optionnelle)** :
   - Cliquer sur "Rechercher Candidats Pertinents"
   - Le système utilise RAG pour trouver les candidats les plus pertinents
   - Ajuster le nombre de candidats à évaluer

4. **Lancer l'évaluation** :
   - Cliquer sur "Lancer l'Évaluation Multi-Agents"
   - Sélectionner les candidats à évaluer
   - Le système va :
     - Analyser les exigences du poste (Agent RH)
     - Évaluer chaque candidat (Agents Profil, Technique, Soft Skills)
     - Générer une décision finale (Agent Décideur)

### Étape 4 : Consultation des Résultats

1. Aller dans la section **"Résultats"**
2. Consulter :
   - Le classement final des candidats
   - Les scores détaillés
   - Les justifications pour chaque candidat
   - Les points forts et faibles

3. **Exporter les résultats** (optionnel) :
   - Cliquer sur "Exporter les Résultats"
   - Télécharger le fichier JSON

## Exemple d'Utilisation

### Cas d'Usage : Recrutement d'un Data Scientist

**Description du poste** :
```
Data Scientist avec 2 ans d'expérience, maîtrise Python et Power BI.
```

**Processus** :

1. **Chargement** : 5 candidats chargés dans `data/raw/`

2. **Analyse Exploratoire** :
   - 5 candidats trouvés
   - Expérience moyenne : 2.4 ans
   - Compétences techniques identifiées : Python, Power BI, SQL, etc.

3. **Évaluation** :
   - Agent RH analyse les exigences
   - Pour chaque candidat :
     - Agent Profil évalue le parcours
     - Agent Technique évalue Python et Power BI
     - Agent Soft Skills évalue la communication et l'adaptabilité
   - Agent Décideur génère le classement final

4. **Résultats** :
   - Top 3 candidats identifiés avec scores
   - Justifications détaillées pour chaque classement
   - Rapport exportable

## Comprendre les Résultats

### Scores par Agent

- **Score Profil** (0-100) : Évaluation du parcours professionnel
- **Score Technique** (0-100) : Évaluation des compétences techniques
- **Score Soft Skills** (0-100) : Évaluation des qualités interpersonnelles
- **Score Final** (0-100) : Score agrégé pondéré

### Justifications

Chaque agent fournit :
- **Points forts** : Ce qui fait la force du candidat
- **Points faibles** : Ce qui pourrait être amélioré
- **Justification détaillée** : Explication du score attribué

### Recommandations

- **Recommandé** : Candidat idéal pour le poste
- **À considérer** : Candidat intéressant mais avec des réserves
- **Non recommandé** : Candidat ne correspondant pas aux critères

## Conseils d'Utilisation

1. **Qualité des données** : Plus les CVs sont détaillés, meilleure sera l'évaluation

2. **Description de poste** : Soyez précis dans les exigences pour des résultats optimaux

3. **Nombre de candidats** : Évaluez 5-10 candidats à la fois pour des résultats rapides

4. **Interprétation** : Les scores sont indicatifs, toujours consulter les justifications

5. **Itération** : Vous pouvez réévaluer avec des critères différents

## Dépannage

### L'évaluation prend trop de temps
- Réduire le nombre de candidats évalués
- Vérifier votre connexion internet (appels API OpenAI)

### Erreurs lors de l'évaluation
- Vérifier que la clé API OpenAI est correcte
- Vérifier que les candidats ont été chargés
- Consulter les logs dans la console

### Résultats inattendus
- Vérifier la qualité de la description de poste
- Consulter les justifications détaillées
- Ajuster les critères si nécessaire

## Support

Pour toute question ou problème, consultez :
- `README.md` : Documentation générale
- `docs/theoretical_foundation.md` : Fondements théoriques
- `SETUP.md` : Guide d'installation

