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

# Session State 초기화
if 'selected_process' not in st.session_state:
    st.session_state.selected_process = "1️⃣ Process A"

# 함수: 노드 색상 업데이트
def get_nodes(selected):
    node_colors = {}
    for node_id in ["A", "B", "C", "D", "E", "F"]:
        if node_id == selected[-1]:  # 선택된 프로세스의 마지막 문자 (A-F)
            node_colors[node_id] = "#FFA07A"  # 선택된 노드 색상 (연어색)
        else:
            node_colors[node_id] = "#ADD8E6"  # 기본 노드 색상 (연한 파랑)
    
    nodes = [
        Node(id="A", label="Process A\n(Material Collection)", size=30, color=node_colors["A"]),
        Node(id="B", label="Process B\n(Processing)", size=30, color=node_colors["B"]),
        Node(id="C", label="Process C\n(Assembly)", size=30, color=node_colors["C"]),
        Node(id="D", label="Process D\n(Quality Inspection)", size=30, color=node_colors["D"]),
        Node(id="E", label="Process E\n(Packaging)", size=30, color=node_colors["E"]),
        Node(id="F", label="Process F\n(Shipping)", size=30, color=node_colors["F"]),
    ]
    return nodes

# 함수: 엣지 정의
def get_edges():
    edges = [
        Edge(source="A", target="B", label="→"),
        Edge(source="B", target="C", label="→"),
        Edge(source="C", target="D", label="↓"),
        Edge(source="D", target="E", label="→"),
        Edge(source="E", target="F", label="→"),
        Edge(source="F", target="A", label="↑"),
    ]
    return edges

# 그래프 설정
def get_config():
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
    return config

# 상호작용 가능한 그래프 표시
nodes = get_nodes(st.session_state.selected_process)
edges = get_edges()
config = get_config()

response = agraph(nodes=nodes, edges=edges, config=config)

# 선택된 노드 처리
if response and 'clickedNodes' in response and len(response['clickedNodes']) > 0:
    clicked_node_id = response['clickedNodes'][0]['id']
    st.session_state.selected_process = f"{['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣'][ord(clicked_node_id)-65]} Process {clicked_node_id}"

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ Select Process")
    # 사이드바의 라디오 버튼으로도 선택 가능하게 설정
    selected_process_sidebar = st.radio(
        "Choose a process to explore:",
        ["1️⃣ Process A", "2️⃣ Process B", "3️⃣ Process C", "4️⃣ Process D", "5️⃣ Process E", "6️⃣ Process F"],
        index=["1️⃣ Process A", "2️⃣ Process B", "3️⃣ Process C", "4️⃣ Process D", "5️⃣ Process E", "6️⃣ Process F"].index(st.session_state.selected_process)
    )
    
    # 사이드바에서 선택된 경우, 세션 상태 업데이트
    if selected_process_sidebar != st.session_state.selected_process:
        st.session_state.selected_process = selected_process_sidebar
    
    st.write("---")
    st.info(f"🔍 **Selected Process:** {st.session_state.selected_process}")

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
st.subheader(f"📌 {st.session_state.selected_process} Details and Data")

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
if st.session_state.selected_process.startswith(("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣")):
    process_id = st.session_state.selected_process[-1]  # "A" 등
    process_key = f"Process {process_id}"
else:
    process_key = st.session_state.selected_process
    process_id = st.session_state.selected_process[-1]

# 상세 설명 및 시계열 데이터 표시
st.markdown(process_descriptions.get(st.session_state.selected_process, process_descriptions.get(process_id, "Select a process from the sidebar.")))
st.plotly_chart(generate_random_timeseries(process_key), use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | Contact: sunghoonkim@kwater.or.kr")
