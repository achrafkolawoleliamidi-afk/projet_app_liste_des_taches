import streamlit as st
import uuid

st.title(" Ma liste des taches ")

if "taches" not in st.session_state: 
# st.session_state est la memoire fournitpar streamlit
        st.session_state.taches = []
with st.form("ajout", clear_on_submit=True):
#"clear_on_submit=True": demande de vider automatriquemenent la zone vidéé après chaque clique sur le bouton 
            libelle = st.text_input("Nouvelle tâche")
            ajouter = st.form_submit_button("Ajouter")
if ajouter and libelle.strip():
        st.session_state.taches.append({
            "id": str(uuid.uuid4()),
            "libelle": libelle.strip(),
            "fait": False,
            "echeance": None,
    })
for tache in st.session_state.taches:
    st.markdown(tache["libelle"])