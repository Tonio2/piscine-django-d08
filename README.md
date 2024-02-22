# Piscine Django Day 08 - AJAX et Websockets

## Description des Exercices

Cette série se concentre sur l'utilisation d'AJAX et de Websockets dans Django. Les exercices impliquent la création d'un système de connexion/déconnexion avec AJAX, le développement d'une application de chat utilisant JQuery et Websockets, l'amélioration de cette application avec un historique des messages, la gestion d'une liste d'utilisateurs connectés se mettant à jour automatiquement, et enfin, l'ajout d'un conteneur de messages avec une barre de défilement pour une meilleure présentation.

## Installation

To get started with this project, follow these steps:

### Setting Up the Environment

1. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Dependency Installation**
   ```bash
   pip install -r requirements.txt
   ```
3. **Redis server**
   ```bash
   docker run --rm -p 6379:6379 redis:7
   ```
4. **Start app**

   Open a new terminal and type
   ```bash
   cd d08
   python manage.py makemigrations chat
   python manage.py migrate
   python manage.py runserver
   ```
