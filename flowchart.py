import streamlit as st
import graphviz
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# Page configuration
st.set_page_config(
    page_title="6-Step Process Flow Chart",
    page_icon="🔄",
    layout="wide"
)

# Sidebar for process selection
with st.sidebar:
    st.title("⚙️ Select Process")
    selected_process = st.radio(
        "Choose a process to explore:",
        ["1️⃣ Process A", "2️⃣ Process B", "3️⃣ Process C", "4️⃣ Process D", "5️⃣ Process E", "6️⃣ Process F"]
    )
    st.write("---")
    st.info(f"🔍 **Selected Process:** {selected_process}")

# Main Title
st.title("📊 6-Step Process Flow Chart & Random Time Series Data")

# Process Flow Chart - Graphviz
st.subheader("🔗 Overall Process Overview")
flow_chart = graphviz.Digraph(format='png')

# Node style configuration
node_style = {
    'shape': 'box',
    'style': 'filled',
    'color': 'lightblue',
    'fontname': 'Helvetica'
}

# 6-Step Pro
