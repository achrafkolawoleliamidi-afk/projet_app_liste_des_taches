# Application de liste de tâches

Projet Python — M2 Mathématiques appliquées, modélisation statistique (2026-2027).

Application web réalisée avec **Streamlit** permettant de créer et de gérer une ou plusieurs listes de tâches.

## Paquets nécessaires

- Python 3.12
- Streamlit

L'environnement complet est décrit dans le fichier `environment.yaml`, à la racine du dépôt. Il fonctionne sous Windows, Mac et Linux.

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
- Une **date et une heure limites** peuvent être ajoutées à une tâche (facultatif). Le **temps restant** s'affiche alors avant le libellé, par exemple « Il vous reste ⏳ 2 j 5 h pour : réviser ». Si l'échéance est dépassée, la **durée du retard** s'affiche en rouge, par exemple « ⚠️ En retard de 35 min : réviser ». Une tâche sans date affiche seulement son libellé. Si seule la date est renseignée, l'échéance est fixée à 23h59.
- Le bouton 🗑️ à droite d'une tâche la **supprime** définitivement de la liste.
- La barre latérale **Mes listes** permet de **créer une nouvelle liste** (par exemple « Cours », « Alternance », « Perso ») et de choisir la liste affichée dans le menu **Liste affichée**. Chaque liste garde ses propres tâches. Un nom de liste déjà utilisé est refusé.
- Le bouton **Exporter les listes (JSON)** télécharge **toutes les listes** dans un seul fichier `taches.json`, avec l'état et la date limite de chaque tâche.
- La zone **Importer des listes** permet de choisir un fichier JSON, puis de cliquer sur **Importer** pour remplacer les listes actuelles par celles du fichier. Un message confirme le nombre de tâches importées. Les anciens fichiers, qui ne contiennent qu'une seule liste, restent compatibles : ils sont chargés dans « Ma liste ».
- Le fichier `exemple_taches.json`, fourni dans le dépôt, peut être importé pour tester l'application.

## Démarche de réalisation

Étapes réalisées :

1. Ajouter et afficher des tâches
2. Cocher et décocher une tâche
3. Rejeter les tâches faites en fin de liste, barrées et grisées
4. Ajouter une date limite optionnelle et afficher le temps restant
5. Exporter et importer la liste au format JSON
6. Supprimer une tâche et rendre l'environnement multi-plateforme
7. Gérer plusieurs listes de tâches

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

### Étape 4 : date limite et temps restant

L'objectif de cette étape était de permettre à l'utilisateur d'ajouter, s'il le souhaite, une date et une heure limites à une tâche, et d'afficher le temps restant avant le libellé.

**Saisie de l'échéance.** Deux champs ont été ajoutés au formulaire, côte à côte grâce à `st.columns(2)` : un `st.date_input` pour la date et un `st.time_input` pour l'heure. Ils sont créés avec `value=None`, ce qui les laisse vides par défaut : l'échéance reste ainsi facultative.

**Enregistrement de l'échéance.** Au moment de l'ajout, si une date a été choisie, elle est assemblée avec l'heure grâce à `datetime.combine`. Sans heure précisée, on prend 23h59, c'est-à-dire la fin de la journée. L'échéance est ensuite stockée sous forme de texte avec `.isoformat()` (par exemple `"2026-10-15T18:00:00"`), car un objet `datetime` ne peut pas être enregistré directement au format JSON. Sans date, le champ vaut `None`. Le champ `echeance`, prévu depuis l'étape 1, est donc enfin utilisé.

**Calcul du temps restant.** Deux fonctions ont été ajoutées :

- `formater_duree(secondes)` convertit un nombre de secondes en un texte lisible (`2 j 5 h`, `3 h 10 min` ou `12 min`), à l'aide de la division entière `//` et du reste `%` ;
- `temps_restant(echeance)` calcule la différence entre l'échéance et l'heure actuelle (`datetime.now()`). Si la durée est positive, elle renvoie le temps restant précédé de ⏳. Si elle est négative, l'échéance est dépassée : elle renvoie « ⚠️ En retard de … » en rouge, en passant `-secondes` à `formater_duree` pour obtenir une durée positive. Sans échéance, elle renvoie un texte vide.

Le calcul en jours, heures et minutes servant à la fois pour le temps restant et pour le retard, il a été placé dans une fonction séparée pour ne pas répéter le code.

**Affichage.** Pour chaque tâche à faire, trois cas sont distingués :

| Situation | Affichage |
|---|---|
| Pas d'échéance | le libellé seul |
| Échéance future | « Il vous reste ⏳ 18 h 12 min pour : faire la cuisine » |
| Échéance dépassée | « ⚠️ En retard de 35 min : faire la cuisine » (en rouge) |

Les tâches déjà faites n'affichent pas de compte à rebours. Le temps restant est recalculé à chaque relecture du fichier, c'est-à-dire à chaque interaction de l'utilisateur.

### Étape 5 : export et import au format JSON

L'objectif de cette étape était de pouvoir sauvegarder la liste dans un fichier, puis de la recharger plus tard. Sans cela, la liste disparaît dès que la page est rafraîchie, car elle n'existe que dans la mémoire de Streamlit (`st.session_state`).

**Export.** La fonction `json.dumps` transforme la liste de tâches en texte au format JSON. L'option `ensure_ascii=False` conserve les accents, et `indent=2` rend le fichier lisible. Le bouton `st.download_button` propose ensuite de télécharger ce texte dans un fichier `taches.json`, enregistré par le navigateur comme n'importe quel téléchargement. C'est pour cette raison que l'identifiant et la date limite sont stockés sous forme de texte depuis le début : le format JSON n'accepte que des types simples (texte, nombres, booléens, listes, dictionnaires).

**Import.** La zone `st.file_uploader` permet de choisir un fichier JSON, qui est relu pour retrouver la liste de dictionnaires. L'import ne se déclenche qu'au clic sur le bouton « Importer » : sans ce bouton, Streamlit réimporterait le fichier à chaque relecture du script, et les modifications faites après l'import seraient perdues.

Avant de remplacer la liste, l'ancien état des cases est effacé de `st.session_state` avec `pop`, afin que les cases cochées dans le fichier s'affichent correctement.

L'import ne déplace ni ne modifie le fichier : l'application lit seulement son contenu et le recopie dans sa mémoire.

### Étape 6 : suppression d'une tâche et environnement multi-plateforme

L'objectif de cette étape était de pouvoir retirer une tâche de la liste, par exemple après une erreur de saisie, et de s'assurer que l'environnement puisse être recréé sur n'importe quel ordinateur.

**Suppression.** Chaque tâche est maintenant affichée sur deux colonnes grâce à `st.columns([0.9, 0.1])` : la case à cocher et le texte à gauche, un bouton 🗑️ à droite. Ce bouton reçoit une clé unique, `suppr_` suivi de l'identifiant de la tâche, pour ne pas entrer en conflit avec la clé de la case.

Un clic sur le bouton appelle la fonction `supprimer_tache` grâce au paramètre `on_click`, avant que Streamlit relise le fichier : la tâche a donc déjà disparu au moment de l'affichage. Cette fonction reconstruit la liste en gardant toutes les tâches sauf celle qui porte cet identifiant. On utilise l'identifiant plutôt que le libellé, pour ne supprimer qu'une seule tâche même si deux tâches ont le même texte. L'état de sa case est aussi effacé de `st.session_state` avec `pop`.

**Environnement.** Le fichier `environment.yaml` a été réexporté avec `conda env export --from-history`, qui ne garde que les paquets installés volontairement : Python 3.12 et Streamlit. Les canaux propres à Windows et la ligne `prefix`, qui contenait un chemin de l'ordinateur, ont été retirés, et le canal `conda-forge` a été ajouté. Conda choisit ainsi lui-même les bons paquets selon le système (Windows, Mac ou Linux).

Le fichier a été testé en créant un environnement neuf avec `conda env create -f environment.yaml -n test_liste`, puis en lançant l'application depuis cet environnement. L'environnement de test a ensuite été supprimé.

### Étape 7 : gérer plusieurs listes

L'objectif de cette étape était de pouvoir ranger les tâches dans des listes séparées, par exemple « Cours », « Alternance » et « Perso », comme le suggère l'énoncé (« une ou des listes »).

**Organisation des données.** La liste unique `st.session_state.taches` a été remplacée par un dictionnaire, `st.session_state.listes` : chaque clé est le nom d'une liste, et chaque valeur est sa liste de tâches. Au premier lancement, il contient une seule liste vide, « Ma liste ». Une petite fonction, `taches_actives()`, renvoie les tâches de la liste affichée : l'ajout, le tri, l'affichage, la case à cocher et la suppression l'utilisent, ce qui a évité de réécrire leur logique.

**Barre latérale.** Une barre latérale (`st.sidebar`) contient un formulaire pour créer une nouvelle liste, qui devient aussitôt la liste affichée. Un nom vide ou déjà utilisé est refusé, avec un avertissement (`st.warning`). Un menu déroulant (`st.selectbox`) permet ensuite de choisir la liste affichée : sa clé, `liste_active`, mémorise ce choix dans `st.session_state`.

**Suppression.** La fonction `supprimer_tache` utilise désormais `taches[:] = ...`, qui remplace le contenu de la liste sur place. La liste rangée dans le dictionnaire est ainsi directement mise à jour.

**Export et import.** L'export enregistre maintenant le dictionnaire complet : toutes les listes sont sauvegardées dans un seul fichier. L'import a été placé dans une fonction `importer`, appelée par le paramètre `on_click` du bouton « Importer ». Elle s'exécute avant la relecture du fichier, ce qui permet de changer la liste affichée : Streamlit interdit de modifier la valeur d'un menu déroulant après son affichage. Le fichier est lu avec `getvalue()`, qui lit tout son contenu quelle que soit la position de lecture.

Après l'import, l'application affiche la première liste qui contient des tâches, pour que l'utilisateur voie tout de suite ce qu'il a importé, et un message (`st.toast`) indique le nombre de tâches et de listes chargées. Les anciens fichiers, qui contiennent une seule liste et non un dictionnaire, sont reconnus avec `isinstance(donnees, list)` et chargés dans « Ma liste ».

Un import remplace toutes les listes affichées : on a choisi de ne pas fusionner plusieurs fichiers, pour éviter les conflits entre des listes de même nom et garder un comportement simple et prévisible.