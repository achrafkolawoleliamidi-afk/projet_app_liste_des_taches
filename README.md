Pour ressoudre ce projet nous allons posseder en 6 étapes

Etape 1: Ajouter et afficher des taches 
L'objectif de cette étape était de construire la base de l'application : permettre à l'utilisateur de saisir une tâche et de la voir apparaître dans une liste.
Une liste stockée dans une variable ordinaire serait donc remise à zéro à chaque clic. Pour la conserver, on l'a rangée dans st.session_state, la mémoire de l'application, en la créant une seule fois au premier lancement grâce au test if "taches" not in st.session_state.
On a ensuite créé un formulaire (st.form) contenant une zone de saisie et un bouton « Ajouter ». Quand l'utilisateur clique et que le texte n'est pas vide, une nouvelle tâche est ajoutée à la liste sous la forme d'un dictionnaire à quatre champs : un identifiant unique (id), le texte (libelle), son état (fait) et sa date limite (echeance). Les deux derniers champs ne servent pas encore mais sont prévus pour les étapes suivantes.
Enfin, une boucle parcourt la liste et affiche chaque libellé avec st.markdown