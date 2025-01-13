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
flow_chart = graphviz.Digraph(
    format='png',
    engine='dot'  # You can experiment with different engines like 'circo' or 'neato' for alternative layouts
)

# Graph attributes for compactness
flow_chart.attr(
    rankdir='LR',          # Left to Right layout
    nodesep='0.5',         # Space between nodes
    ranksep='0.5',         # Space between ranks
    fontsize='10',         # Smaller font size
    size='8,5!',            # Fixed size with aspect ratio
    ratio='compress'       # Compress the layout to fit the size
)

# Node style configuration
node_style = {
    'shape': 'box',
    'style': 'filled',
    'color': 'lightblue',
    'fontname': 'Helvetica',
    'fontsize': '10',      # Smaller font size for nodes
    'width': '1.5',        # Fixed width
    'height': '0.75'       # Fixed height
}

# 6-Step Process Nodes (Rectangle)
flow_chart.node("A", "Process A\n(Material Collection)", **node_style)
flow_chart.node("B", "Process B\n(Processing)", **node_style)
flow_chart.node("C", "Process C\n(Assembly)", **node_style)
flow_chart.node("D", "Process D\n(Quality Inspection)", **node_style)
flow_chart.node("E", "Process E\n(Packaging)", **node_style)
flow_chart.node("F", "Process F\n(Shipping)", **node_style)

# Clockwise Connections (Left 3 → Right 3)
flow_chart.edge("A", "B", label="→", fontsize='8')
flow_chart.edge("B", "C", label="→", fontsize='8')
flow_chart.edge("C", "D", label="↓", fontsize='8')
flow_chart.edge("D", "E", label="→", fontsize='8')
flow_chart.edge("E", "F", label="→", fontsize='8')
flow_chart.edge("F", "A", label="↑", fontsize='8')  # Circular connection

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
        width=800,   # Adjust as needed
        height=400,  # Adjust as needed
        plot_bgcolor='white'
    )

    return fig

# Selected process description and time series chart
st.subheader(f"📌 {selected_process} Details and Data")

process_descriptions = {
    "1️⃣ Process A": "**Process A (Material Collection):** Collecting and inspecting raw materials for production.",
    "2️⃣ Process B": "**Process B (Processing):** Processing raw materials into suitable forms for production.",
    "3️⃣ Process C": "**Process C (Assembly):** Assembling processed parts into finished products.",
    "4️⃣ Process D": "**Process D (Quality Inspection):** Inspecting product quality and removing defective items.",
    "5️⃣ Process E": "**Process E (Packaging):** Packaging the inspected products for shipment.",
    "6️⃣ Process F": "**Process F (Shipping):** Shipping packaged products to customers."
}

st.write(process_descriptions.get(selected_process, "Select a process from the sidebar."))
st.plotly_chart(generate_random_timeseries(selected_process.split()[1]), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | Contact: sunghoonkim@kwater.or.kr")
