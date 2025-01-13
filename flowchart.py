import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from PIL import Image  # Image 모듈 임포트

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
        # 랜덤 시드 고정 (일관된 데이터 생성)
        seed = hash(process_name) % (2**32)  # 프로세스 이름을 기반으로 시드 설정
        np.random.seed(seed)
        dates = pd.date_range(start='2023-01-01', periods=points)
        values = np.random.randn(points).cumsum()  # 랜덤 누적 합

        df = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        st.session_state.timeseries_data[process_name] = df
    
    return st.session_state.timeseries_data[process_name]

# Plotly 시계열 차트 생성 함수
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

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ Select Process")
    
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
    
    # Disinfection 선택 시 추가 입력 슬라이더 표시
    if st.session_state.selected_process.startswith("4️⃣"):
        st.write("---")
        st.header("모델 인풋 설정")
        
        # 이미지 불러오기
        try:
            im = Image.open("AI_Lab_logo.jpg")
            st.image(im, caption=" ", use_column_width=True)  # 사이드바에 이미지 표시
        except FileNotFoundError:
            st.write("Logo image not found.")  # 이미지가 없을 때의 처리
        
        # 사용자 입력 받기
        DOC = st.slider("DOC (mg/L)", 0.0, 10.0, 5.0)
        NH3 = st.slider("Surrogate Variable (mg/L)", 0.0, 5.0, 0.5)
        Cl0 = st.slider("현재농도 Cl0 (mg/L)", 0.0, 5.0, 1.5)
        Temp = st.slider("Temperature (°C)", 0.0, 35.0, 20.0)
        max_time = st.slider("최대예측시간 (hrs)", 1, 24, 5)
        
        # 추가적인 사이드바 입력 (k1, k2 범위)
        st.header("EPA 모델 k1, k2 범위 설정")
        k1_low = st.slider("AI High1 (k1 최대 적정범위)", 0.01, 5.0, 3.5)
        k1_high = st.slider("AI Low1 (k1 최소 적정범위)", 0.01, 5.0, 2.0)
        k2_low = st.slider("AI High2 (k2 최대 적정범위)", 0.01, 5.0, 0.1)
        k2_high = st.slider
