# Application de liste de tâches

Application web réalisée en Python avec **Streamlit** pour créer et gérer une ou plusieurs listes de tâches : cases à cocher, échéances avec compte à rebours, suppression, et sauvegarde au format JSON.

Projet Python — M2 Mathématiques appliquées, modélisation statistique (2026-2027).
Auteur : Achraf Kolawole LIAMIDI

## Paquets nécessaires

- Python 3.12
- Streamlit

L'environnement est décrit dans le fichier `environment.yaml`, à la racine du dépôt. Il fonctionne sous Windows, Mac et Linux.

## Installation

Le projet utilise un environnement **Conda** nommé `liste_taches`. Ouvrir un terminal (par exemple Anaconda Prompt), puis :

```bash
git clone https://github.com/achrafkolawoleliamidi-afk/projet_app_liste_des_taches.git
cd projet_app_liste_des_taches
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

- Saisir le texte d'une tâche dans la zone « Nouvelle tâche », puis cliquer sur **Ajouter**. La zone de saisie se vide automatiquement.
- Le libellé peut contenir du **Markdown**, par exemple `**gras**` ou `*italique*`. Une tâche vide (ou composée uniquement d'espaces) n'est pas ajoutée.
- Chaque tâche est précédée d'une **case à cocher** : cocher la case marque la tâche comme faite, la décocher annule.
- Les tâches faites sont automatiquement **déplacées à la fin de la liste**, **barrées** et **grisées**.
- Une **date et une heure limites** peuvent être ajoutées à une tâche (facultatif). Si seule la date est renseignée, l'échéance est fixée à 23h59.
- Le **temps restant** s'affiche à droite du libellé, par exemple « Réviser · ⏳ reste 2 j 5 h ». Si l'échéance est dépassée, la durée du retard s'affiche en rouge : « Réviser · ⚠ En retard de 35 min ». Toutes les tâches restent ainsi alignées à gauche.
- Le bouton 📅 à droite d'une tâche permet d'**ajouter, modifier ou enlever son échéance** à tout moment.
- Le bouton 🗑 **supprime** définitivement la tâche.
- La barre latérale **Mes listes** permet de **créer une nouvelle liste** (par exemple « Cours », « Alternance », « Perso ») et de choisir la liste affichée. Chaque liste garde ses propres tâches. Un nom déjà utilisé est refusé.
- Le bouton **Exporter les listes (JSON)** télécharge **toutes les listes** dans un seul fichier `taches.json`.
- La zone **Importer des listes** permet de choisir un fichier JSON, puis de cliquer sur **Importer** pour remplacer les listes actuelles par celles du fichier. Un message confirme le nombre de tâches importées. Les anciens fichiers, qui ne contiennent qu'une seule liste, sont chargés dans « Ma liste ».
- Le fichier `exemple_taches.json`, fourni dans le dépôt, peut être importé pour tester l'application.

## Organisation du code

Tout le code se trouve dans `app.py`.

**Principe de Streamlit.** Streamlit relit tout le fichier `app.py` à chaque interaction (clic, saisie). J'ai donc rangé les données qui doivent être conservées d'une relecture à l'autre dans `st.session_state`, la mémoire de l'application.

**Structure des données.** `st.session_state.listes` est un dictionnaire : chaque clé est le nom d'une liste, chaque valeur est une liste de tâches. Une tâche est un dictionnaire à quatre champs :

```json
{
"id": "un identifiant unique (uuid)",
"libelle": "Réviser le **TOEIC**",
"fait": false,
"echeance": "2026-11-13T16:45:00"
}
```

`echeance` vaut `null` si la tâche n'a pas de date limite. C'est aussi le format des fichiers JSON exportés.

**Fonctions principales.**

| Fonction | Rôle |
|---|---|
| `taches_actives()` | renvoie les tâches de la liste affichée |
| `changer_etat(id)` | met à jour le champ `fait` quand on coche une case |
| `supprimer_tache(id)` | retire une tâche de la liste |
| `modifier_echeance(id)` | ajoute ou modifie l'échéance d'une tâche |
| `retirer_echeance(id)` | enlève l'échéance d'une tâche |
| `oublier_widgets(id)` | efface l'état mémorisé des champs d'une tâche |
| `importer()` | charge un fichier JSON |
| `formater_duree(s)` | convertit des secondes en texte (`2 j 5 h`) |
| `temps_restant(echeance)` | calcule le texte du compte à rebours |

Les actions déclenchées par un clic passent par les paramètres `on_change` et `on_click` : la fonction s'exécute **avant** la relecture du fichier, si bien que l'affichage est tout de suite à jour.

**Pour modifier le code.** Une nouvelle propriété de tâche s'ajoute au dictionnaire créé dans le bloc « Ajouter », puis s'affiche dans la boucle `for tache in taches_triees`. Chaque widget lié à une tâche doit avoir une clé unique construite à partir de son `id`.

## Démarche de réalisation

J'ai construit l'application étape par étape :

1. Ajouter et afficher des tâches
2. Cocher et décocher une tâche
3. Rejeter les tâches faites en fin de liste, barrées et grisées
4. Ajouter une date limite optionnelle et afficher le temps restant
5. Exporter et importer la liste au format JSON
6. Supprimer une tâche et rendre l'environnement multi-plateforme
7. Gérer plusieurs listes de tâches
8. Modifier l'échéance de chaque tâche et afficher le temps restant à droite

### Étape 1 : ajouter et afficher des tâches

Dans cette étape, j'ai construit la base de l'application : pouvoir saisir une tâche et la voir apparaître dans une liste.

Comme Streamlit relit tout le fichier à chaque interaction, une variable ordinaire aurait été remise à zéro à chaque clic. J'ai donc rangé la liste dans `st.session_state`, en la créant une seule fois grâce au test `if "taches" not in st.session_state` (j'ai ensuite remplacé cette liste unique par un dictionnaire de listes à l'étape 7).

J'ai créé un formulaire (`st.form`) avec une zone de saisie et un bouton « Ajouter ». Chaque nouvelle tâche est un dictionnaire à quatre champs : `id`, `libelle`, `fait` et `echeance`. J'ai prévu ces quatre champs dès le départ pour ne pas avoir à changer la structure plus tard. Une boucle affiche ensuite chaque libellé avec `st.markdown`.

### Étape 2 : cocher et décocher une tâche

Dans cette étape, j'ai ajouté une case à cocher à gauche de chaque tâche pour indiquer qu'elle est faite.

J'ai remplacé `st.markdown` par `st.checkbox`, en utilisant le libellé comme étiquette : la case se place à gauche du texte et le Markdown reste interprété. Le paramètre `value=tache["fait"]` donne l'état de départ de la case.

J'ai donné à chaque case une clé unique, `key=tache["id"]`. Cela évite une erreur quand deux tâches ont le même libellé, et permet à Streamlit de rattacher chaque case à la bonne tâche d'une exécution à l'autre.

### Étape 3 : rejeter les tâches faites en fin de liste

Dans cette étape, j'ai fait en sorte que les tâches faites passent à la fin de la liste, barrées et grisées.

Pour que le tri soit correct dès le clic, j'ai écrit une fonction `changer_etat`, appelée à chaque clic grâce au paramètre `on_change`. Elle recopie l'état de la case, disponible dans `st.session_state[id_tache]`, dans le champ `fait` de la tâche.

J'ai ensuite trié la liste avec `sorted(..., key=lambda t: t["fait"])` : comme `False` passe avant `True`, les tâches à faire s'affichent en premier. Pour barrer et griser une tâche faite, j'ai entouré son libellé de `~~...~~` et de `:gray[...]`.

### Étape 4 : date limite et temps restant

Dans cette étape, j'ai permis d'ajouter une date et une heure limites facultatives à une tâche, et d'afficher le temps restant.

**Saisie.** J'ai ajouté au formulaire un `st.date_input` et un `st.time_input`, côte à côte grâce à `st.columns(2)`. Je les ai créés avec `value=None` : ils sont vides par défaut, ce qui rend l'échéance facultative.

**Enregistrement.** J'assemble la date et l'heure avec `datetime.combine` (23h59 si l'heure manque), puis je les stocke en texte avec `.isoformat()`, car un objet `datetime` ne peut pas être enregistré directement au format JSON.

**Calcul.** J'ai écrit `formater_duree`, qui convertit un nombre de secondes en texte lisible à l'aide de la division entière `//` et du reste `%`, et `temps_restant`, qui calcule la différence entre l'échéance et `datetime.now()`. Une durée négative signifie que l'échéance est dépassée : le retard s'affiche alors en rouge. Comme le calcul sert à la fois pour le temps restant et pour le retard, je l'ai placé dans une fonction séparée pour ne pas répéter le code.

Le temps restant est recalculé à chaque interaction. Les tâches faites n'affichent pas de compte à rebours.

### Étape 5 : export et import au format JSON

Dans cette étape, j'ai rendu possible la sauvegarde des tâches dans un fichier et leur rechargement plus tard. Sans cela, tout disparaît dès que la page est rafraîchie.

**Export.** J'utilise `json.dumps` pour transformer les données en texte JSON (`ensure_ascii=False` conserve les accents, `indent=2` rend le fichier lisible), puis `st.download_button` pour proposer le téléchargement de `taches.json`.

**Import.** J'ai ajouté une zone `st.file_uploader` pour choisir un fichier JSON. J'ai choisi de ne lancer l'import qu'au clic sur un bouton « Importer » : sans ce bouton, Streamlit réimporterait le fichier à chaque relecture, et les modifications faites après l'import seraient perdues. J'efface aussi l'ancien état des cases avec `pop`, pour que les cases cochées dans le fichier s'affichent correctement.

### Étape 6 : suppression d'une tâche et environnement multi-plateforme

**Suppression.** J'ai ajouté un bouton 🗑 à chaque tâche, avec une clé `suppr_` suivie de l'identifiant de la tâche. Un clic appelle `supprimer_tache` grâce à `on_click`, qui garde toutes les tâches sauf celle qui porte cet identifiant. J'ai utilisé l'identifiant plutôt que le libellé pour ne supprimer qu'une seule tâche, même si deux tâches ont le même texte.

**Environnement.** J'ai généré le fichier `environment.yaml` avec `conda export -n liste_taches --from-history -f environment.yaml`, qui ne garde que les paquets installés volontairement. J'ai retiré les canaux propres à Windows et la ligne `prefix`, qui contenait un chemin de mon ordinateur, et j'ai ajouté le canal `conda-forge` : Conda choisit ainsi les bons paquets selon le système. J'ai testé ce fichier en créant un environnement neuf, puis en lançant l'application depuis cet environnement.

### Étape 7 : gérer plusieurs listes

Dans cette étape, j'ai permis de ranger les tâches dans des listes séparées, comme le suggère l'énoncé (« une ou des listes »).

**Données.** J'ai remplacé la liste unique par le dictionnaire `st.session_state.listes`. J'ai écrit une fonction `taches_actives()` qui renvoie les tâches de la liste affichée : l'ajout, le tri, l'affichage et la suppression l'utilisent, ce qui m'a évité de réécrire leur logique. Dans `supprimer_tache`, j'utilise maintenant `taches[:] = ...`, qui modifie la liste sur place, directement dans le dictionnaire.

**Barre latérale.** J'ai ajouté dans `st.sidebar` un formulaire de création de liste (un nom vide ou déjà utilisé est refusé avec `st.warning`) et un menu déroulant (`st.selectbox`), dont la clé `liste_active` mémorise la liste choisie.

**Export et import.** L'export enregistre maintenant le dictionnaire complet. J'ai placé l'import dans une fonction `importer`, appelée par `on_click`, car Streamlit interdit de modifier la valeur d'un menu déroulant après son affichage. Je lis le fichier avec `getvalue()`, puis l'application affiche la première liste non vide. Les anciens fichiers (une seule liste) sont reconnus avec `isinstance(donnees, list)`. J'ai choisi qu'un import remplace toutes les listes, sans fusionner plusieurs fichiers, pour éviter les conflits entre listes de même nom et garder un comportement simple et prévisible.

### Étape 8 : modifier l'échéance et réorganiser l'affichage

Dans cette étape, j'ai pris en compte les retours de l'enseignant.

**Modifier l'échéance.** Jusqu'ici, l'échéance ne pouvait être choisie qu'à la création de la tâche. J'ai ajouté à chaque tâche un bouton 📅 qui ouvre une petite fenêtre (`st.popover`) contenant une date, une heure et deux boutons : « Enregistrer » appelle `modifier_echeance`, et « Enlever l'échéance » appelle `retirer_echeance`. Les champs sont pré-remplis avec l'échéance actuelle, et leurs clés (`date_` et `heure_` suivies de l'identifiant) les rattachent à la bonne tâche.

**Affichage.** J'ai déplacé le temps restant à droite du libellé : toutes les tâches commencent ainsi au même endroit et restent alignées à gauche. J'ai découpé chaque ligne en trois colonnes avec `st.columns([0.8, 0.1, 0.1])` : la case et le texte, le bouton 📅, puis le bouton 🗑.

**Nettoyage.** J'ai écrit une fonction `oublier_widgets`, qui efface l'état mémorisé de la case, de la date et de l'heure d'une tâche. Je l'utilise lors de la suppression et de l'import, pour que d'anciennes valeurs ne s'affichent pas par erreur.