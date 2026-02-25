Epic Events CRM (CLI)

CRM en ligne de commande sécurisé avec gestion avancée des rôles, architecture en couches et authentification JWT.

## 📌 Contexte

Projet réalisé dans le cadre du parcours Développeur d'application Python – OpenClassrooms (Projet P12).

Epic Events est une entreprise spécialisée dans l’organisation d’événements (mariages, séminaires, conférences…).
L’objectif est de remplacer des fichiers Excel dispersés par un CRM structuré, sécurisé et utilisable en ligne de commande.

L’application permet de gérer :

les utilisateurs

les clients

les contrats

les événements

avec une gestion fine des droits selon le rôle de chaque collaborateur.

## 🎯 Objectifs pédagogiques

Ce projet m’a permis de travailler sur :

Architecture en couches (CLI → Services → Repository → Models)

Authentification sécurisée avec JWT

Hachage des mots de passe avec bcrypt

Gestion des rôles et permissions (RBAC)

SQLAlchemy (ORM)

Séparation des responsabilités

Journalisation des erreurs avec Sentry

Structuration d’un projet Python professionnel

## 🛠 Stack technique

Python 3.9+

SQLAlchemy (ORM)

MySQL + PyMySQL

bcrypt (hash des mots de passe)

PyJWT (authentification JWT)

python-dotenv (.env)

Rich (affichage CLI)

Sentry (monitoring & logging)

## 👥 Gestion des rôles

L’application repose sur le principe du moindre privilège.

### 🔹 Rôles disponibles

gestion

commercial

support

## 🔐 Permissions par rôle
### 🟦 Rôle : gestion

Accès complet au système.

**Peut :** 

Créer / modifier / supprimer des utilisateurs

Créer / modifier / supprimer tous les clients

Créer / modifier / supprimer tous les contrats

Voir tous les événements

Modifier tous les événements

Assigner ou changer un support sur un événement

### 🟩 Rôle : commercial

Accès limité à son portefeuille clients.

**Peut :**

Créer des clients (automatiquement liés à lui)

Voir uniquement ses propres clients

Modifier uniquement ses propres clients

Créer des contrats pour ses clients

Modifier uniquement ses contrats

Créer un événement uniquement si le contrat est signé

**Ne peut pas :**

Supprimer des clients

Supprimer des contrats

Modifier les événements

### 🟨 Rôle : support

Accès opérationnel aux événements assignés.

**Peut :**

Voir uniquement les événements qui lui sont assignés

Modifier uniquement les événements qui lui sont assignés

**Ne peut pas :**

Créer des clients

Créer des contrats

Créer des événements

Accéder aux données hors assignation

## 🏗 Architecture du projet

epic_events/
├── cli/
│   ├── auth.py
│   ├── user_cli.py
│   ├── client_cli.py
│   ├── contrat_cli.py
│   └── evenement_cli.py
├── models/
│   ├── base.py
│   ├── utilisateur.py
│   ├── client.py
│   ├── contrat.py
│   └── evenement.py
├── repositories/
├── services/
├── utils/
├── main.py
├── requirements.txt
└── README.md

Architecture en couches

CLI → Interface utilisateur

Services → Logique métier

Repositories → Accès base de données

Models → Entités SQLAlchemy

## 🗄 Modèle de données
**Utilisateur**

id

nom

email

mot_de_passe (haché)

role (gestion / commercial / support)

**Relations :**

contrats (en tant que commercial)

evenements (en tant que support)

**Client**

id

nom_complet

email

telephone

entreprise

date_creation

derniere_mise_a_jour

commercial_id (FK)

**Contrat**

id

client_id (FK)

commercial_id (FK)

montant_total

montant_restant

date_creation

statut (signé / non signé)

Evenement

id

contrat_id (FK)

support_id (FK)

date_debut

date_fin

lieu

participants

notes

## ⚙️ Installation

### 1️⃣ Cloner le dépôt

git clone https://github.com/abi-seg/oc_p12_epic_events.git
cd oc_p12_epic_events

### 2️⃣ Créer un environnement virtuel

python -m venv venv

Activation :

Windows

venv\Scripts\activate

macOS / Linux

source venv/bin/activate

### 3️⃣ Installer les dépendances

pip install -r requirements.txt

### 4️⃣ Créer un fichier .env

DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:PORT/NOM_BASE
SECRET_KEY=une_cle_secrete_pour_le_JWT
SENTRY_DSN=optional
SENTRY_ENV=dev

### 5️⃣ Lancer l’application

python main.py

Les tables sont créées automatiquement via :

Base.metadata.create_all(engine)

## 🚀 Utilisation

**Connexion**

1 - Se connecter
4 - Se déconnecter
5 - Voir utilisateur connecté
0 - Quitter

**Gestion des utilisateurs (gestion)**

2  - Créer un utilisateur
3  - Voir tous les utilisateurs
19 - Modifier
20 - Supprimer

**Clients**

6 - Créer
7 - Voir
8 - Modifier
9 - Supprimer (gestion)

**Contrats**

10 - Créer
11 - Voir tous
12 - Voir non signés
13 - Voir non payés
14 - Modifier
15 - Supprimer

**Événements**
16 - Créer (commercial)
17 - Voir
18 - Modifier (gestion/support)

## 🔒 Sécurité

Mots de passe jamais stockés en clair

Hash sécurisé avec bcrypt

Authentification JWT signée

Token stocké localement (.token)

Vérifications systématiques des rôles

Protection contre les injections SQL via SQLAlchemy

## 📊 Monitoring

L’application utilise Sentry pour :

journaliser les erreurs critiques

suivre les exceptions

monitorer les événements importants

Configuration via la variable d’environnement SENTRY_DSN.
