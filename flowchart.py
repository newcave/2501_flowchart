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
    st.session_state.selected_process = "1️⃣ Raw Water Quality Prediction"

# 프로세스 레이블 업데이트
process_labels = {
    "A": "Raw Water Quality Prediction",
    "B": "Coagulation/Flocculation",
    "C": "Filtration",
    "D": "Disinfection",
    "E": "DPBs",
    "F": "Water Demand"
}

# 프로세스 설명 업데이트
process_descriptions = {
    "1️⃣ Raw Water Quality Prediction": "**Raw Water Quality Prediction:** Predicting the quality of raw water before processing.",
    "2️⃣ Coagulation/Flocculation": "**Coagulation/Flocculation:** Combining chemicals to remove suspended solids from water.",
    "3️⃣ Filtration": "**Filtration:** Filtering out remaining particles from water.",
    "4️⃣ Disinfection": "**Disinfection:** Eliminating pathogens to ensure water safety.",
    "5️⃣ DPBs": "**DPBs:** Managing Deposits, Pitting, and Corrosion in water systems.",
    "6️⃣ Water Demand": "**Water Demand:** Assessing and meeting the water demand requirements.",
    "A": "**Raw Water Quality Prediction:** Predicting the quality of raw water before processing.",
    "B": "**Coagulation/Flocculation:** Combining chemicals to remove suspended solids from water.",
    "C": "**Filtration:** Filtering out remaining particles from water.",
    "D": "**Disinfection:** Eliminating pathogens to ensure water safety.",
    "E": "**DPBs:** Managing Deposits, Pitting, and Corrosion in water systems.",
    "F": "**Water Demand:** Assessing and meeting the water demand requirements."
}

# 함수: 노드 색상 및 테두리 업데이트
def get_nodes(selected):
    # selected = "1️⃣ Raw Water Quality Prediction"
    try:
        # 첫 번째 단어에서 숫자 추출 (예: "1️⃣"에서 "1" 추출)
        number_str = selected.split()[0][0]
        number = int(number_str)
        selected_id = chr(64 + number)  # 1 -> 'A', 2 -> 'B', ..., 6 -> 'F'
    except (IndexError, ValueError):
        selected_id = 'A'  # 기본값 설정 (필요에 따라 변경 가능)
    
    nodes = []
    for node_id in ["A", "B", "C", "D", "E", "F"]:
        if node_id == selected_id:
            # 선택된 노드: 배경색 주황색 및 테두리 색상 진하게 변경
            node_color = {
                "background": "#FFA500",  # 주황색
                "border": "#FF8C00",      # 어두운 주황색 (테두리 색상)
                "highlight": {
                    "background": "#FFB347",  # 밝은 주황색 (마우스 오버 시)
                    "border": "#FF8C00"       # 어두운 주황색
                }
            }
        else:
            # 기본 노드 색상
            node_color = {
                "background": "#ADD8E6",  # 연한 파랑
                "border": "#000000",      # 검정 테두리
                "highlight": {
                    "background": "#87CEFA",  # 밝은 파랑 (마우스 오버 시)
                    "border": "#000000"       # 검정 테두리
                }
            }
        
        nodes.append(
            Node(
                id=node_id,
                label=f"Process {node_id}\n({process_labels[node_id]})",
                size=30,
                color=node_color
            )
        )
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

# 함수: 랜덤 시계열 데이터 생성 및 세션 상태에 저장
def get_timeseries_data(process_name, points=50):
    if 'timeseries_data' not in st.session_state:
        st.session_state.timeseries_data = {}
    
    if process_name not in st.session_state.timeseries_data:
        np.random.seed()  # 랜덤 시드 설정 (필요 시 고정 가능)
        dates = pd.date_range(start='2023-01-01', periods=points)
        values = np.random.randn(points).cumsum()  # 랜덤 누적 합

        df = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        st.session_state.timeseries_data[process_name] = df
    
    return st.session_state.timeseries_data[process_name]

# 상호작용 가능한 그래프 및 원의 집합을 나란히 배치
col1, col2 = st.columns([3, 1])  # 비율을 조정하여 공간 배분

with col1:
    nodes = get_nodes(st.session_state.selected_process)
    edges = get_edges()
    config = get_config()
    
    response = agraph(nodes=nodes, edges=edges, config=config)

    # 선택된 노드 처리
    if response and 'clickedNodes' in response and len(response['clickedNodes']) > 0:
        clicked_node_id = response['clickedNodes'][0]['id']
        # 프로세스 번호 매핑 (A-F -> 1-6)
        process_number = ord(clicked_node_id) - 64  # 'A'->1, 'B'->2, ...
        # 프로세스 이름 가져오기
        process_name = process_labels[clicked_node_id]
        st.session_state.selected_process = f"{process_number}️⃣ {process_name}"
        # 선택 변경 시 기존 시계열 데이터 초기화 (필요 시)
        # Optional: Uncomment the following line if you want to reset the data when process changes
        # if process_name in st.session_state.timeseries_data:
        #     del st.session_state.timeseries_data[process_name]

with col2:
    st.markdown("### 🔵🟢🔴 프로세스 상태")
    
    # Plotly를 사용하여 세 개의 색깔 다른 원 그리기
    fig_circles = go.Figure()

    # 각 원의 위치와 색상 정의
    circles = [
        {"x_center": 0.5, "y_center": 0.7, "radius": 0.1, "color": "blue", "label": "프로세스 1"},
        {"x_center": 0.3, "y_center": 0.3, "radius": 0.1, "color": "green", "label": "프로세스 2"},
        {"x_center": 0.7, "y_center": 0.3, "radius": 0.1, "color": "red", "label": "프로세스 3"},
    ]

    for circle in circles:
        fig_circles.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=circle["x_center"] - circle["radius"],
            y0=circle["y_center"] - circle["radius"],
            x1=circle["x_center"] + circle["radius"],
            y1=circle["y_center"] + circle["radius"],
            fillcolor=circle["color"],
            line=dict(color=circle["color"]),
        )
        # 라벨 추가
        fig_circles.add_annotation(
            x=circle["x_center"],
            y=circle["y_center"],
            text=circle["label"],
            showarrow=False,
            font=dict(color="white", size=12),
            xanchor="center",
            yanchor="middle"
        )

    # 레이아웃 설정
    fig_circles.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=300,
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
    )

    st.plotly_chart(fig_circles, use_container_width=True)

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ Select Process")
    # 사이드바의 라디오 버튼으로도 선택 가능하게 설정
    selected_process_sidebar = st.radio(
        "Choose a process to explore:",
        [
            "1️⃣ Raw Water Quality Prediction",
            "2️⃣ Coagulation/Flocculation",
            "3️⃣ Filtration",
            "4️⃣ Disinfection",
            "5️⃣ DPBs",
            "6️⃣ Water Demand"
        ],
        index=[
            "1️⃣ Raw Water Quality Prediction",
            "2️⃣ Coagulation/Flocculation",
            "3️⃣ Filtration",
            "4️⃣ Disinfection",
            "5️⃣ DPBs",
            "6️⃣ Water Demand"
        ].index(st.session_state.selected_process)
    )
    
    # 사이드바에서 선택된 경우, 세션 상태 업데이트
    if selected_process_sidebar != st.session_state.selected_process:
        st.session_state.selected_process = selected_process_sidebar
    
    st.write("---")
    st.info(f"🔍 **Selected Process:** {st.session_state.selected_process}")

# 메인 타이틀
st.title("📊 Connected Process Flow Chart & Simulator")

# 선택된 프로세스 이름 추출
selected_process_name = st.session_state.selected_process.split(" ", 1)[1]

# 시계열 데이터 가져오기
timeseries_df = get_timeseries_data(selected_process_name)

# Plotly 차트 생성
def create_timeseries_chart(df, process_name):
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

# 상세 설명 및 시계열 데이터 표시
st.markdown(process_descriptions.get(st.session_state.selected_process, "Select a process from the sidebar."))
st.plotly_chart(create_timeseries_chart(timeseries_df, selected_process_name), use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | Contact: sunghoonkim@kwater.or.kr
