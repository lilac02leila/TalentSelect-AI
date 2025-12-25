# Fondements Théoriques du Système Multi-Agents pour la Sélection de Candidats

## 1. Introduction

Ce document présente les fondements théoriques, concepts, méthodes et algorithmes utilisés dans le système multi-agents pour la sélection intelligente de candidats.

## 2. Architecture Multi-Agents

### 2.1 Concept des Systèmes Multi-Agents

Un système multi-agents (SMA) est un système distribué composé d'agents autonomes qui interagissent pour résoudre des problèmes complexes. Chaque agent possède :
- **Autonomie** : Capacité à prendre des décisions indépendantes
- **Réactivité** : Capacité à réagir aux changements de l'environnement
- **Proactivité** : Capacité à initier des actions pour atteindre ses objectifs
- **Socialité** : Capacité à communiquer et collaborer avec d'autres agents

### 2.2 Avantages de l'Approche Multi-Agents

1. **Spécialisation** : Chaque agent se concentre sur un domaine spécifique
2. **Parallélisation** : Les agents peuvent travailler simultanément
3. **Robustesse** : La défaillance d'un agent n'empêche pas le système de fonctionner
4. **Explicabilité** : Chaque agent fournit sa propre justification

### 2.3 Architecture du Système

Notre système utilise une architecture hiérarchique avec 5 agents spécialisés :

```
                    Agent Décideur
                         |
        +----------------+----------------+
        |                |                |
    Agent RH    Agent Profil    Agent Technique    Agent Soft Skills
```

## 3. Traitement du Langage Naturel (NLP)

### 3.1 Extraction d'Entités Nommées (NER)

La NER permet d'identifier et de classer les entités dans un texte :
- **Personnes** : Noms des candidats, références
- **Organisations** : Entreprises, universités
- **Localisations** : Villes, pays
- **Dates** : Périodes d'emploi, formations

**Algorithme utilisé** : Modèles spaCy basés sur des réseaux de neurones convolutifs et des embeddings contextuels.

### 3.2 Extraction de Compétences

L'extraction de compétences utilise :
- **Dictionnaires de compétences** : Listes prédéfinies de compétences techniques et soft skills
- **Reconnaissance de motifs** : Recherche de patterns dans le texte
- **Analyse sémantique** : Compréhension du contexte d'utilisation

### 3.3 Traitement de Texte

**Prétraitement** :
- Normalisation (suppression d'espaces, caractères spéciaux)
- Tokenisation
- Lemmatisation (réduction à la forme canonique)

**Métriques calculées** :
- Nombre de mots
- Richesse du vocabulaire
- Longueur moyenne des phrases

## 4. Retrieval-Augmented Generation (RAG)

### 4.1 Principe du RAG

Le RAG combine :
1. **Retrieval** : Recherche d'informations pertinentes dans une base de connaissances
2. **Augmentation** : Enrichissement du contexte avec les informations récupérées
3. **Generation** : Génération de réponses par un LLM

### 4.2 Architecture RAG

```
Requête → Embeddings → Recherche Vectorielle → Documents Pertinents
                                                      ↓
                                              Contexte Enrichi
                                                      ↓
                                              LLM → Réponse
```

### 4.3 Embeddings et Recherche Vectorielle

**Embeddings** : Représentation vectorielle dense du texte qui capture le sens sémantique.

**Modèle utilisé** : OpenAI `text-embedding-3-small`
- Dimension : 1536
- Basé sur des transformers pré-entraînés

**Similarité cosinus** : Mesure de similarité entre vecteurs
```
similarity = cos(θ) = (A · B) / (||A|| × ||B||)
```

**Base vectorielle** : ChromaDB
- Stockage persistant
- Index HNSW (Hierarchical Navigable Small World) pour recherche rapide
- Distance cosinus pour similarité sémantique

## 5. Modèles de Langage (LLMs)

### 5.1 GPT-4 et Architecture Transformer

Les LLMs modernes utilisent l'architecture Transformer :
- **Attention multi-têtes** : Permet de capturer différentes relations dans le texte
- **Positional encoding** : Encode la position des tokens
- **Feed-forward networks** : Traitement non-linéaire

### 5.2 Prompt Engineering

Chaque agent utilise des prompts spécialisés :
- **Rôle** : Définit l'identité de l'agent
- **Contexte** : Informations sur la tâche
- **Instructions** : Étapes à suivre
- **Format de sortie** : Structure attendue (JSON)

### 5.3 In-Context Learning

Les LLMs apprennent à partir d'exemples dans le prompt :
- Few-shot learning : Quelques exemples suffisent
- Zero-shot learning : Aucun exemple nécessaire

## 6. Framework CrewAI

### 6.1 Concept

CrewAI est un framework pour orchestrer des agents LLM :
- **Agents** : Entités autonomes avec rôles et objectifs
- **Tasks** : Tâches assignées aux agents
- **Crew** : Équipe d'agents collaborant sur des tâches

### 6.2 Workflow

```
1. Définition des agents avec rôles et backstories
2. Création de tâches avec descriptions détaillées
3. Formation d'un Crew avec agents et tâches
4. Exécution séquentielle ou parallèle
5. Agrégation des résultats
```

## 7. Explicabilité (XAI)

### 7.1 Importance de l'Explicabilité

Dans le recrutement, l'explicabilité est cruciale pour :
- **Transparence** : Comprendre les décisions
- **Conformité légale** : Respect des réglementations
- **Confiance** : Acceptation par les recruteurs

### 7.2 Méthodes d'Explicabilité

**1. Justifications textuelles par LLM**
- Chaque agent génère une explication de son évaluation
- Format structuré avec points forts/faibles

**2. Scores décomposés**
- Score technique, soft skills, profil séparés
- Permet d'identifier les forces/faiblesses

**3. Traçabilité**
- Historique complet des évaluations
- Chaque étape documentée

### 7.3 SHAP (Shapley Additive Explanations)

SHAP attribue une valeur à chaque feature :
- **Valeur de Shapley** : Contribution marginale de chaque feature
- **Additivité** : Somme des contributions = score final

## 8. Analyse Exploratoire des Données (EDA)

### 8.1 Objectifs

- Comprendre la distribution des données
- Identifier les patterns
- Détecter les anomalies
- Préparer les données pour le ML

### 8.2 Techniques Utilisées

**Statistiques descriptives** :
- Moyennes, médianes, écarts-types
- Distributions (histogrammes)
- Corrélations

**Visualisations** :
- Graphiques en barres (distribution des compétences)
- Nuages de points (expérience vs longueur CV)
- Heatmaps (corrélations)

## 9. Pipeline de Traitement

### 9.1 Étapes du Pipeline

```
1. Chargement des documents (PDF, DOCX, TXT)
2. Extraction de texte
3. Prétraitement (nettoyage, normalisation)
4. Extraction d'entités (NER)
5. Extraction de compétences
6. Calcul de métriques
7. Création d'embeddings
8. Stockage dans base vectorielle
9. Recherche par similarité (RAG)
10. Évaluation multi-agents
11. Agrégation et décision finale
```

### 9.2 Optimisations

- **Parallélisation** : Traitement simultané de plusieurs candidats
- **Mise en cache** : Stockage des embeddings
- **Indexation** : Recherche rapide avec HNSW

## 10. Métriques d'Évaluation

### 10.1 Scores par Agent

**Agent Profil** :
- Score de cohérence du parcours (0-100)
- Pertinence de l'expérience (0-100)
- Qualité de la formation (0-100)

**Agent Technique** :
- Score par compétence (0-100)
- Profondeur des connaissances (0-100)
- Expérience pratique (0-100)

**Agent Soft Skills** :
- Communication (0-100)
- Leadership (0-100)
- Motivation (0-100)
- Adéquation culturelle (0-100)

### 10.2 Score Final

Score agrégé avec pondération :
```
Score_Final = w1 × Score_Technique + w2 × Score_Soft_Skills + 
              w3 × Score_Profil + w4 × Score_Culturel
```

Pondérations par défaut :
- Technique : 35%
- Soft Skills : 25%
- Profil : 25%
- Culturel : 15%

## 11. Limitations et Améliorations Futures

### 11.1 Limitations Actuelles

- Dépendance aux LLMs (coût, latence)
- Biais potentiels des modèles
- Nécessité de données de qualité
- Complexité de l'extraction depuis PDFs

### 11.2 Améliorations Possibles

- Fine-tuning de modèles spécialisés
- Intégration de données LinkedIn via API
- Interface de feedback pour amélioration continue
- Modèles de confiance pour les scores
- Analyse de biais et équité

## 12. Références

1. Wooldridge, M. (2009). An Introduction to MultiAgent Systems.
2. Devlin, J., et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers.
3. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.
4. Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions.
5. Vaswani, A., et al. (2017). Attention Is All You Need.

