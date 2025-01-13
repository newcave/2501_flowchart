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

# 6-Step Process Nodes (Rectangle)
flow_chart.node("A", "Process A\n(Material Collection)", **node_style)
flow_chart.node("B", "Process B\n(Processing)", **node_style)
flow_chart.node("C", "Process C\n(Assembly)", **node_style)
flow_chart.node("D", "Process D\n(Quality Inspection)", **node_style)
flow_chart.node("E", "Process E\n(Packaging)", **node_style)
flow_chart.node("F", "Process F\n(Shipping)", **node_style)

# Clockwise Connections (Left 3 → Right 3)
flow_chart.edge("A", "B", label="→")
flow_chart.edge("B", "C", label="→")
flow_chart.edge("C", "D", label="↓")
flow_chart.edge("D", "E", label="→")
flow_chart.edge("E", "F", label="→")
flow_chart.edge("F", "A", label="↑")  # Circular connection

# Display the flow chart
st.graphviz_chart(flow_chart, use_container_width=True)

# Function to generate random time series data
def generate_random_timeseries(process_name, points=50):
    np.random.seed()
    dates = pd.date_range(start='2023-01-01', periods=points)
    values = np.random.randn(points).cumsum()  # Random cumulative sum

    df = pd.DataFrame({
        'Date': dates,
        'Value': values
    })

    # Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Value'],
        mode='lines+markers',
        line=dict(color='royalblue'),
        marker=dict(size=4),
        name=f'{process_name} Time Series'
    ))

    fig.update_layout(
        title=f"📈 {process_name} - Random Time Series Data",
        xaxis_title="Date",
        yaxis_title="Measurement Value",
        autosize=True,
        width=800,   # Reduced width for better fit
        height=400,  # Reduced height for better fit
        plot_bgcolor='white'
    )

    return fig

# Selected process description and time series chart
st.subheader(f"📌 {selected_process} Details and Data")

if selected_process == "1️⃣ Process A":
    st.write("**Process A (Material Collection):** Collecting and inspecting raw materials for production.")
    st.plotly_chart(generate_random_timeseries("Process A"), use_container_width=True)

elif selected_process == "2️⃣ Process B":
    st.write("**Process B (Processing):** Processing raw materials into suitable forms for production.")
    st.plotly_chart(generate_random_timeseries("Process B"), use_container_width=True)

elif selected_process == "3️⃣ Process C":
    st.write("**Process C (Assembly):** Assembling processed parts into finished products.")
    st.plotly_chart(generate_random_timeseries("Process C"), use_container_width=True)

elif selected_process == "4️⃣ Process D":
    st.write("**Process D (Quality Inspection):** Inspecting product quality and removing defective items.")
    st.plotly_chart(generate_random_timeseries("Process D"), use_container_width=True)

elif selected_process == "5️⃣ Process E":
    st.write("**Process E (Packaging):** Packaging the inspected products for shipment.")
    st.plotly_chart(generate_random_timeseries("Process E"), use_container_width=True)

elif selected_process == "6️⃣ Process F":
    st.write("**Process F (Shipping):** Shipping packaged products to customers.")
    st.plotly_chart(generate_random_timeseries("Process F"), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | Contact: sunghoonkim@kwater.or.kr")
