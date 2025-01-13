import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(
    page_title="6-Step Process Flow Chart",
    page_icon="🔄",
    layout="wide"
)

# 노드 정의
nodes = [
    Node(id="A", label="Process A\n(Material Collection)", size=30, color="#ADD8E6"),
    Node(id="B", label="Process B\n(Processing)", size=30, color="#ADD8E6"),
    Node(id="C", label="Process C\n(Assembly)", size=30, color="#ADD8E6"),
    Node(id="D", label="Process D\n(Quality Inspection)", size=30, color="#ADD8E6"),
    Node(id="E", label="Process E\n(Packaging)", size=30, color="#ADD8E6"),
    Node(id="F", label="Process F\n(Shipping)", size=30, color="#ADD8E6"),
]

# 엣지 정의
edges = [
    Edge(source="A", target="B", label="→"),
    Edge(source="B", target="C", label="→"),
    Edge(source="C", target="D", label="↓"),
    Edge(source="D", target="E", label="→"),
    Edge(source="E", target="F", label="→"),
    Edge(source="F", target="A", label="↑"),
]

# 그래프 설정
config = Config(
    height=600,
    width=800,
    directed=True,
    physics=True,
    hierarchical=False,
    nodeHighlightBehavior=True,
    node={'color': '#ADD8E6'},
    link={'color': '#808080', 'labelHighlightBold': True},
)

# 상호작용 가능한 그래프 표시
response = agraph(nodes=nodes, edges=edges, config=config)

# 선택된 노드 처리
selected_node = None
if response and 'clickedNodes' in response and len(response['clickedNodes']) > 0:
    selected_node = response['clickedNodes'][0]['id']

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ Select Process")
    if selected_node:
        selected_process = f"{selected_node}️⃣ Process {selected_node}"
    else:
        selected_process = st.radio(
            "Choose a process to explore:",
            ["1️⃣ Process A", "2️⃣ Process B", "3️⃣ Process C", "4️⃣ Process D", "5️⃣ Process E", "6️⃣ Process F"]
        )
    st.write("---")
    st.info(f"🔍 **Selected Process:** {selected_process}")

# 메인 타이틀
st.title("📊 6-Step Process Flow Chart & Random Time Series Data")

# 함수: 랜덤 시계열 데이터 생성
def generate_random_timeseries(process_name, points=50):
    np.random.seed()
    dates = pd.date_range(start='2023-01-01', periods=points)
    values = np.random.randn(points).cumsum()  # 랜덤 누적 합

    df = pd.DataFrame({
        'Date': dates,
        'Value': values
    })

    # Plotly 차트
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
        width=800,   # 필요에 따라 조정
        height=400,  # 필요에 따라 조정
        plot_bgcolor='white'
    )

    return fig

# 선택된 프로세스에 따른 상세 정보 및 시계열 차트
st.subheader(f"📌 {selected_process} Details and Data")

process_descriptions = {
    "1️⃣ Process A": "**Process A (Material Collection):** Collecting and inspecting raw materials for production.",
    "2️⃣ Process B": "**Process B (Processing):** Processing raw materials into suitable forms for production.",
    "3️⃣ Process C": "**Process C (Assembly):** Assembling processed parts into finished products.",
    "4️⃣ Process D": "**Process D (Quality Inspection):** Inspecting product quality and removing defective items.",
    "5️⃣ Process E": "**Process E (Packaging):** Packaging the inspected products for shipment.",
    "6️⃣ Process F": "**Process F (Shipping):** Shipping packaged products to customers.",
    "A": "**Process A (Material Collection):** Collecting and inspecting raw materials for production.",
    "B": "**Process B (Processing):** Processing raw materials into suitable forms for production.",
    "C": "**Process C (Assembly):** Assembling processed parts into finished products.",
    "D": "**Process D (Quality Inspection):** Inspecting product quality and removing defective items.",
    "E": "**Process E (Packaging):** Packaging the inspected products for shipment.",
    "F": "**Process F (Shipping):** Shipping packaged products to customers."
}

# 프로세스 이름 추출
if selected_process.startswith("1️⃣") or selected_process.startswith("2️⃣") or selected_process.startswith("3️⃣") \
   or selected_process.startswith("4️⃣") or selected_process.startswith("5️⃣") or selected_process.startswith("6️⃣"):
    process_key = selected_process.split()[1]  # "Process A" 등
    process_id = selected_process.split()[1][-1]  # "A" 등
else:
    process_key = selected_process
    process_id = selected_process

st.markdown(process_descriptions.get(selected_process, process_descriptions.get(process_id, "Select a process from the sidebar.")))
st.plotly_chart(generate_random_timeseries(process_key), use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | Contact: sunghoonkim@kwater.or.kr")
