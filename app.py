import streamlit as st
st.title(' 1 Factoriel')

def fact(n):
    if n <= 0:
        return 1
    return n * fact(n-1)
col1, col2 = st.columns(2)
with col1:
    n = int(st.number_input('Valeur de $n$', 0, step=1))
with col2:
    st.write(f"Factorielle$(n)$ = {fact(n)}")


st.header(' 2 Fichier animaux')
import pandas as pd
file = st.file_uploader("animaux.csv", type="csv")
if file is not None:
    df = pd.read_csv(file, index_col='id')
    st.subheader('Le DataFrame')
    st.write(df)
    st.subheader('Statistiques descriptives')
    st.write(df.describe())
else:
    st.info(":point_up_2: Téléchargez un fichier CSV")

st.header(' 3 Les courbes')
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, np.pi, 200)
fig = plt.figure()
for i in range(4):
    plt.plot(x, x * np.sin(2**i * x), label=f'$x \sin(2^{i}x)$')
plt.legend()
st.write(fig)

st.header(' 4 Simulation')
x = np.linspace(0, np.pi, 200)
data_plot = pd.DataFrame(x, columns=['x'])
for i in range(4):
    data_plot[f'x * sin(2^{i} * x)'] = x * np.sin(2**i * x)
st.line_chart(data_plot, x='x')