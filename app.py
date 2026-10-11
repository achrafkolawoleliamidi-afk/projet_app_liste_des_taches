import streamlit as st
import uuid
# NOUVEAU : outils pour manipuler les dates et les heures
from datetime import datetime, time

st.title(" Ma liste des taches ")

# st.session_state est la memoire fournitpar streamlit
if "taches" not in st.session_state:
    st.session_state.taches = []


# Fonction appelée automatiquement quand on coche ou décoche une case
# (on_change) : elle met à jour le champ "fait" AVANT que Streamlit
# relise le fichier, pour que le tri soit tout de suite correct.
def changer_etat(id_tache):
    for tache in st.session_state.taches:
        if tache["id"] == id_tache:
            # st.session_state[id_tache] contient l'état de la case
            # (True si cochée, False sinon), car sa clé est l'id de la tâche
            tache["fait"] = st.session_state[id_tache]


# NOUVEAU : transforme un nombre de secondes en texte lisible
# Exemple : 183780 secondes -> "2 j 3 h"
def formater_duree(secondes):
    jours = secondes // 86400                 # 86400 secondes dans un jour
    heures = (secondes % 86400) // 3600       # 3600 secondes dans une heure
    minutes = (secondes % 3600) // 60         # 60 secondes dans une minute

    if jours > 0:
        return f"{jours} j {heures} h"
    if heures > 0:
        return f"{heures} h {minutes} min"
    return f"{minutes} min"


# NOUVEAU : calcul du temps restant avant l'échéance d'une tâche
# Renvoie un petit texte à afficher avant le libellé, ou "" s'il n'y a pas de date
def temps_restant(echeance):
    if echeance is None:
        return ""

    # L'échéance est stockée en texte (format ISO) : on la reconvertit en date
    reste = datetime.fromisoformat(echeance) - datetime.now()
    secondes = int(reste.total_seconds())

    # Durée négative : l'échéance est dépassée
    # -secondes rend la durée positive pour afficher le temps de retard
    if secondes < 0:
        return f":red[⚠️ En retard de {formater_duree(-secondes)}]"

    return f"⏳ {formater_duree(secondes)}"


#"clear_on_submit=True": demande de vider automatriquemenent la zone vidéé après chaque clique sur le bouton
with st.form("ajout", clear_on_submit=True):
    libelle = st.text_input("Nouvelle tâche")

    # NOUVEAU : date et heure limites, facultatives (value=None : champ vide)
    col1, col2 = st.columns(2)
    with col1:
        date_limite = st.date_input("Date limite (facultatif)", value=None, format="DD/MM/YYYY")
    with col2:
        heure_limite = st.time_input("Heure limite (facultatif)", value=None)

    ajouter = st.form_submit_button("Ajouter")

if ajouter and libelle.strip():
    # NOUVEAU : construction de l'échéance (None si aucune date choisie)
    echeance = None
    if date_limite is not None:
        # Sans heure précisée, on prend la fin de la journée (23h59)
        if heure_limite is None:
            heure_limite = time(23, 59)
        # On assemble date + heure, puis on stocke en texte pour l'export JSON
        echeance = datetime.combine(date_limite, heure_limite).isoformat()

    st.session_state.taches.append({
        "id": str(uuid.uuid4()),
        "libelle": libelle.strip(),
        "fait": False,
        "echeance": echeance,   # NOUVEAU : la date limite (ou None)
    })

#Tri des tâches
# False (à faire) passe avant True (faite) : les tâches faites vont à la fin
taches_triees = sorted(st.session_state.taches, key=lambda t: t["fait"])

#Affichage des tâches avec une case à cocher à gauche
for tache in taches_triees:
    # Étape 4 : une tâche faite est barrée (~~...~~) et grisée (:gray[...])
    if tache["fait"]:
        texte = f":gray[~~{tache['libelle']}~~]"
    else:
        # NOUVEAU : le temps restant s'affiche AVANT le libellé
        reste = temps_restant(tache["echeance"])
        if tache["echeance"] is None:
            # Pas de date : on affiche seulement le libellé
            texte = tache["libelle"]
        elif "En retard" in reste:
            # Échéance dépassée : « Il vous reste » n'a plus de sens
            texte = f"{reste} : {tache['libelle']}"
        else:
            # Échéance future : on affiche la phrase complète
            texte = f"Il vous reste {reste} pour : {tache['libelle']}"

    # La case affiche le libellé (Markdown accepté) ;
    # la clé unique relie la case à sa tâche.
    st.checkbox(  #st.checkbox : une case + le texte
        texte,
        value=tache["fait"],
        key=tache["id"],
        # On enregistre l'état de la case dans la tâche
        # grâce à la fonction changer_etat, appelée à chaque clic
        on_change=changer_etat,
        args=(tache["id"],),
    )