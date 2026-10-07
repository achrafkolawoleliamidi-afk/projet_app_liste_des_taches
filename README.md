# Application de liste de tâches

Projet Python — M2 Mathématiques appliquées, modélisation statistique (2026-2027).

Application web réalisée avec **Streamlit** permettant de créer et de gérer une liste de tâches.

## Paquets nécessaires

- Python 3.12
- Streamlit

L'environnement complet (paquets et versions) est décrit dans le fichier `environment.yaml`, à la racine du dépôt.

## Installation

Le projet utilise un environnement **Conda** nommé `liste_taches`. Pour le recréer à partir du fichier fourni, ouvrir un terminal (par exemple Anaconda Prompt) dans le dossier du projet, puis :

```bash
conda env create -f environment.yaml
conda activate liste_taches
```

## Lancer l'application

Depuis le dossier du projet, avec l'environnement `liste_taches` activé :

```bash
streamlit run app.py
```

L'application s'ouvre dans le navigateur à l'adresse `http://localhost:8501`. Pour l'arrêter, appuyer sur `Ctrl+C` dans le terminal.

## Fonctionnement

- Saisir le texte d'une tâche dans la zone « Nouvelle tâche », puis cliquer sur **Ajouter**.
- La tâche s'affiche dans la liste, et la zone de saisie se vide automatiquement.
- Le libellé d'une tâche peut contenir du **Markdown** : par exemple `**gras**`, `*italique*`.
- Une tâche vide (ou composée uniquement d'espaces) n'est pas ajoutée.
- Chaque tâche est précédée d'une **case à cocher** : cocher la case marque la tâche comme faite, la décocher annule.
- Les tâches faites sont automatiquement **déplacées à la fin de la liste**, **barrées** et **grisées**. Une tâche décochée remonte parmi les tâches à faire.

## Démarche de réalisation

Étapes réalisées :

1. Ajouter et afficher des tâches
2. Cocher et décocher une tâche
3. Rejeter les tâches faites en fin de liste, barrées et grisées

### Étape 1 : ajouter et afficher des tâches

L'objectif de cette étape était de construire la base de l'application : permettre à l'utilisateur de saisir une tâche et de la voir apparaître dans une liste.

Streamlit relit tout le fichier `app.py` à chaque interaction. Une liste stockée dans une variable ordinaire serait donc remise à zéro à chaque clic. Pour la conserver, on l'a rangée dans `st.session_state`, la mémoire de l'application, en la créant une seule fois au premier lancement grâce au test `if "taches" not in st.session_state`.

On a ensuite créé un formulaire (`st.form`) contenant une zone de saisie et un bouton « Ajouter ». Quand l'utilisateur clique et que le texte n'est pas vide, une nouvelle tâche est ajoutée à la liste sous la forme d'un dictionnaire à quatre champs : un identifiant unique (`id`), le texte (`libelle`), son état (`fait`) et sa date limite (`echeance`).

Enfin, une boucle parcourt la liste et affiche chaque libellé avec `st.markdown`.

### Étape 2 : cocher et décocher une tâche

L'objectif de cette étape était de pouvoir signaler qu'une tâche a été faite, grâce à une case à cocher placée à sa gauche, et de pouvoir la décocher en cas d'erreur.

L'affichage avec `st.markdown` a été remplacé par `st.checkbox`, dont l'étiquette est le libellé de la tâche : la case est placée automatiquement à gauche du texte, et le Markdown reste interprété. Le paramètre `value=tache["fait"]` donne l'état de départ de la case.

Chaque case reçoit une clé unique, `key=tache["id"]`. Cette clé utilise l'identifiant prévu à l'étape 1 : elle évite une erreur lorsque deux tâches ont le même libellé, et elle permet à Streamlit de rattacher chaque case à la bonne tâche d'une exécution à l'autre.

L'état de la case est ensuite enregistré dans le champ `fait` de la tâche. C'est la première fois que l'application modifie une tâche existante, et non plus seulement qu'elle en ajoute une.

### Étape 3 : rejeter les tâches faites en fin de liste

L'objectif de cette étape était de placer les tâches faites à la fin de la liste et de les distinguer visuellement, en les barrant et en les grisant.

Pour que le tri soit correct dès le clic, le champ `fait` doit être mis à jour avant que Streamlit relise le fichier. On a donc ajouté une fonction `changer_etat`, appelée automatiquement à chaque clic sur une case grâce au paramètre `on_change`. Elle retrouve la tâche par son identifiant et recopie l'état de la case, disponible dans `st.session_state[id_tache]`.

Avant l'affichage, la liste est triée avec `sorted(..., key=lambda t: t["fait"])` : comme `False` passe avant `True`, les tâches à faire s'affichent en premier et les tâches faites à la fin.

Enfin, le libellé d'une tâche faite est entouré de `~~...~~` pour le barrer et de `:gray[...]` pour le griser.