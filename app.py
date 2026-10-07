import streamlit as st
import uuid

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


#"clear_on_submit=True": demande de vider automatriquemenent la zone vidéé après chaque clique sur le bouton
with st.form("ajout", clear_on_submit=True):
    libelle = st.text_input("Nouvelle tâche")
    ajouter = st.form_submit_button("Ajouter")

if ajouter and libelle.strip():
    st.session_state.taches.append({
        "id": str(uuid.uuid4()),
        "libelle": libelle.strip(),
        "fait": False,
        "echeance": None,
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
        texte = tache["libelle"]

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