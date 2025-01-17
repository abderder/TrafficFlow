import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Charger le fichier Excel
uploaded_file = st.file_uploader("Téléchargez le fichier Excel", type="xlsx")
if uploaded_file:
    # Lire les données
    df = pd.read_excel(uploaded_file)

    # Afficher les données brutes
    st.write("### Aperçu des données :", df.head())

    # Calcul des KPI de base
    avg_duration = df['duration (s)'].mean()
    avg_time_loss = df['timeLoss (s)'].mean()
    congestion_routes = df.groupby('departLane (edge id)')['timeLoss (s)'].mean().sort_values(ascending=False)

    st.metric("Durée moyenne des trajets (s)", round(avg_duration, 2))
    st.metric("Perte de temps moyenne (s)", round(avg_time_loss, 2))

    # Visualisation : Temps de trajet moyen par route
    st.write("### Temps de trajet moyen par segment de route")
    fig = px.bar(congestion_routes.head(10), x=congestion_routes.head(10).index, y=congestion_routes.head(10).values,
                 labels={'x': 'Segment de route', 'y': 'Temps de trajet moyen (s)'})
    st.plotly_chart(fig)

    # Filtrer les données pour n'afficher que les segments les plus impactants
    heatmap_data = df.groupby(['departLane (edge id)', 'arrivalLane (edge id)'])['timeLoss (s)'].sum().reset_index()
    top_heatmap_data = heatmap_data.sort_values(by='timeLoss (s)', ascending=False).head(20)  # Top 20 segments

    # Générer la carte thermique
    heatmap_fig = px.density_heatmap(
        top_heatmap_data,
        x='departLane (edge id)',
        y='arrivalLane (edge id)',
        z='timeLoss (s)',
        color_continuous_scale='Viridis',
        title="Carte thermique des pertes de temps (Top 20 segments)"
    )
    heatmap_fig.update_layout(
        xaxis=dict(title="Segment de départ", tickangle=45),
        yaxis=dict(title="Segment d'arrivée"),
        height=700,
        width=900
    )
    st.plotly_chart(heatmap_fig)
