import streamlit as st
import uuid
import json  # ÉTAPE 5 : pour l'export et l'import au format JSON
# Outils pour manipuler les dates et les heures
from datetime import datetime, time

st.title("Ma liste des tâches")

# ÉTAPE 7 : plusieurs listes
# st.session_state.listes est un dictionnaire :
# clé = nom de la liste, valeur = liste de tâches
if "listes" not in st.session_state:
    st.session_state.listes = {"Ma liste": []}


# ÉTAPE 7 : renvoie les tâches de la liste actuellement choisie
def taches_actives():
    return st.session_state.listes[st.session_state.liste_active]


# ÉTAPE 8 : efface l'état mémorisé des widgets liés à une tâche
# (case à cocher, date et heure de l'échéance)
def oublier_widgets(id_tache):
    for cle in (id_tache, f"date_{id_tache}", f"heure_{id_tache}"):
        st.session_state.pop(cle, None)


# Fonction appelée automatiquement quand on coche ou décoche une case
# (on_change) : elle met à jour le champ "fait" AVANT que Streamlit
# relise le fichier, pour que le tri soit tout de suite correct.
def changer_etat(id_tache):
    for tache in taches_actives():
        if tache["id"] == id_tache:
            tache["fait"] = st.session_state[id_tache]


# ÉTAPE 6 : suppression d'une tâche à partir de son identifiant
def supprimer_tache(id_tache):
    taches = taches_actives()
    # ÉTAPE 7 : [:] modifie la liste sur place, dans le dictionnaire
    taches[:] = [t for t in taches if t["id"] != id_tache]
    oublier_widgets(id_tache)


# ÉTAPE 8 : enregistre la nouvelle échéance choisie pour une tâche
# (ajout ou modification). Appelée par on_click, AVANT la relecture.
def modifier_echeance(id_tache):
    date_choisie = st.session_state[f"date_{id_tache}"]
    heure_choisie = st.session_state[f"heure_{id_tache}"]
    for tache in taches_actives():
        if tache["id"] == id_tache:
            if date_choisie is None:
                # Pas de date : la tâche n'a pas d'échéance
                tache["echeance"] = None
            else:
                # Sans heure précisée, on prend la fin de la journée
                if heure_choisie is None:
                    heure_choisie = time(23, 59)
                tache["echeance"] = datetime.combine(date_choisie, heure_choisie).isoformat()


# ÉTAPE 8 : enlève l'échéance d'une tâche
def retirer_echeance(id_tache):
    for tache in taches_actives():
        if tache["id"] == id_tache:
            tache["echeance"] = None
    # On vide aussi les champs date et heure de cette tâche
    st.session_state.pop(f"date_{id_tache}", None)
    st.session_state.pop(f"heure_{id_tache}", None)


# ÉTAPE 5 et 7 : fonction appelée au clic sur « Importer »
def importer():
    fichier = st.session_state.fichier_import
    if fichier is None:
        st.toast("Aucun fichier choisi.")
        return
    # getvalue() lit tout le fichier, quelle que soit la position de lecture
    donnees = json.loads(fichier.getvalue().decode("utf-8"))
    # Ancien format (une seule liste) : on le range dans « Ma liste »
    if isinstance(donnees, list):
        donnees = {"Ma liste": donnees}
    # On efface l'ancien état des widgets pour afficher les données du fichier
    for taches in donnees.values():
        for t in taches:
            oublier_widgets(t["id"])
    st.session_state.listes = donnees
    # On affiche la première liste qui contient des tâches
    non_vides = [nom for nom, taches in donnees.items() if taches]
    st.session_state.liste_active = non_vides[0] if non_vides else list(donnees)[0]
    nb = sum(len(taches) for taches in donnees.values())
    st.toast(f"{nb} tâches importées dans {len(donnees)} liste(s).")


# Transforme un nombre de secondes en texte lisible
# Exemple : 183780 secondes -> "2 j 3 h"
def formater_duree(secondes):
    jours = secondes // 86400
    heures = (secondes % 86400) // 3600
    minutes = (secondes % 3600) // 60
    if jours > 0:
        return f"{jours} j {heures} h"
    if heures > 0:
        return f"{heures} h {minutes} min"
    return f"{minutes} min"


# Calcul du temps restant avant l'échéance d'une tâche
# Renvoie un petit texte, ou "" s'il n'y a pas de date
def temps_restant(echeance):
    if echeance is None:
        return ""
    reste = datetime.fromisoformat(echeance) - datetime.now()
    secondes = int(reste.total_seconds())
    if secondes < 0:
        return f":red[⚠ En retard de {formater_duree(-secondes)}]"
    return f"⏳ reste {formater_duree(secondes)}"


# ÉTAPE 7 : barre latérale pour créer et choisir une liste
with st.sidebar:
    st.header("Mes listes")
    with st.form("nouvelle_liste", clear_on_submit=True):
        nom_liste = st.text_input("Nouvelle liste")
        creer = st.form_submit_button("Créer")
    if creer and nom_liste.strip():
        if nom_liste.strip() in st.session_state.listes:
            st.warning("Cette liste existe déjà.")
        else:
            st.session_state.listes[nom_liste.strip()] = []
            st.session_state.liste_active = nom_liste.strip()
    st.selectbox("Liste affichée", list(st.session_state.listes), key="liste_active")

st.subheader(st.session_state.liste_active)

# Formulaire d'ajout d'une tâche
with st.form("ajout", clear_on_submit=True):
    libelle = st.text_input("Nouvelle tâche")
    col1, col2 = st.columns(2)
    with col1:
        date_limite = st.date_input("Date limite (facultatif)", value=None, format="DD/MM/YYYY")
    with col2:
        heure_limite = st.time_input("Heure limite (facultatif)", value=None)
    ajouter = st.form_submit_button("Ajouter")

if ajouter and libelle.strip():
    echeance = None
    if date_limite is not None:
        if heure_limite is None:
            heure_limite = time(23, 59)
        echeance = datetime.combine(date_limite, heure_limite).isoformat()
    taches_actives().append({
        "id": str(uuid.uuid4()),
        "libelle": libelle.strip(),
        "fait": False,
        "echeance": echeance,
    })

# Tri : les tâches à faire (False) avant les tâches faites (True)
taches_triees = sorted(taches_actives(), key=lambda t: t["fait"])

for tache in taches_triees:
    if tache["fait"]:
        # Tâche faite : barrée et grisée
        texte = f":gray[~~{tache['libelle']}~~]"
    else:
        # ÉTAPE 8 : le libellé vient EN PREMIER, le temps restant à DROITE,
        # pour que toutes les tâches soient alignées à gauche
        reste = temps_restant(tache["echeance"])
        if reste:
            texte = f"{tache['libelle']}   ·   {reste}"
        else:
            texte = tache["libelle"]

    # ÉTAPE 8 : trois colonnes : case + texte, échéance, poubelle
    col_case, col_date, col_suppr = st.columns([0.8, 0.1, 0.1])

    with col_case:
        st.checkbox(
            texte,
            value=tache["fait"],
            key=tache["id"],
            on_change=changer_etat,
            args=(tache["id"],),
        )

    with col_date:
        # ÉTAPE 8 : petite fenêtre qui s'ouvre au clic sur 📅
        # pour ajouter, modifier ou enlever l'échéance de CETTE tâche
        with st.popover("📅", help="Modifier l'échéance"):
            # Valeurs de départ : l'échéance actuelle, si elle existe
            if tache["echeance"]:
                actuelle = datetime.fromisoformat(tache["echeance"])
                date_defaut, heure_defaut = actuelle.date(), actuelle.time()
            else:
                date_defaut, heure_defaut = None, None
            st.date_input("Date", value=date_defaut, format="DD/MM/YYYY",
                          key=f"date_{tache['id']}")
            st.time_input("Heure", value=heure_defaut,
                          key=f"heure_{tache['id']}")
            st.button("Enregistrer", key=f"enreg_{tache['id']}",
                      on_click=modifier_echeance, args=(tache["id"],))
            st.button("Enlever l'échéance", key=f"retirer_{tache['id']}",
                      on_click=retirer_echeance, args=(tache["id"],))

    with col_suppr:
        st.button(
            "🗑",
            key=f"suppr_{tache['id']}",
            help="Supprimer cette tâche",
            on_click=supprimer_tache,
            args=(tache["id"],),
        )

# ÉTAPE 5 : export et import au format JSON
st.divider()
st.subheader("Sauvegarde")
col_export, col_import = st.columns(2)

with col_export:
    st.download_button(
        "Exporter les listes (JSON)",
        data=json.dumps(st.session_state.listes, ensure_ascii=False, indent=2),
        file_name="taches.json",
        mime="application/json",
    )

with col_import:
    fichier = st.file_uploader("Importer des listes", type="json", key="fichier_import")
    st.button("Importer", on_click=importer, disabled=fichier is None)