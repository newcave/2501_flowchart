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
        np.random.seed()  # 랜덤 시드 설정 (필요 시 고정 가능)
        dates = pd.date_range(start='2023-01-01', periods=points)
        values = np.random.randn(points).cumsum()  # 랜덤 누적 합

        df = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        st.session_state.timeseries_data[process_name] = df
    
    return st.session_state.timeseries_data[process_name]

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ Select Process")
    
    if st.session_state.selected_process.startswith("4️⃣"):
        # Disinfection 프로세스가 선택된 경우, 특정 입력 슬라이더와 이미지 표시
        # 이미지 불러오기
        try:
            im = Image.open("AI_Lab_logo.jpg")
            st.sidebar.image(im, caption=" ")  # 사이드바에 이미지 표시
        except FileNotFoundError:
            st.sidebar.write("Logo image not found.")  # 이미지가 없을 때의 처리
        
        st.sidebar.header("모델 인풋 설정")
        
        # 사용자 입력 받기
        DOC = st.sidebar.slider("DOC (mg/L)", 0.0, 10.0, 5.0)
        NH3 = st.sidebar.slider("surrogate var. (mg/L)", 0.0, 5.0, 0.5)
        Cl0 = st.sidebar.slider("현재농도 Cl0 (mg/L)", 0.0, 5.0, 1.5)
        Temp = st.sidebar.slider("Temperature (°C)", 0.0, 35.0, 20.0)
        max_time = st.sidebar.slider("최대예측시간 (hrs)", 1, 24, 5)
        
        # 추가적인 사이드바 입력 (k1, k2 범위)
        st.sidebar.header("EPA 모델 k1, k2 범위 설정")
        k1_low = st.sidebar.slider("AI High1 (k1최대 적정범위)", 0.01, 5.0, 3.5)
        k1_high = st.sidebar.slider("AI Low1 (k1최소 적정범위)", 0.01, 5.0, 2.0)
        k2_low = st.sidebar.slider("AI High2 (k2최대 적정범위)", 0.01, 5.0, 0.1)
        k2_high = st.sidebar.slider("AI Low2 (k1최소 적정범위)", 0.01, 5.0, 0.5)
        
        # Assign to session state
        if 'disinfection_inputs' not in st.session_state:
            st.session_state.disinfection_inputs = {}
        
        st.session_state.disinfection_inputs['DOC'] = DOC
        st.session_state.disinfection_inputs['NH3'] = NH3
        st.session_state.disinfection_inputs['Cl0'] = Cl0
        st.session_state.disinfection_inputs['Temp'] = Temp
        st.session_state.disinfection_inputs['max_time'] = max_time
        st.session_state.disinfection_inputs['k1_low'] = k1_low
        st.session_state.disinfection_inputs['k1_high'] = k1_high
        st.session_state.disinfection_inputs['k2_low'] = k2_low
        st.session_state.disinfection_inputs['k2_high'] = k2_high
        
        st.write("---")
        st.info(f"🔍 **Selected Process:** {st.session_state.selected_process}")
    else:
        # 다른 프로세스가 선택된 경우, 기존 라디오 버튼 표시
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

# Streamlit Columns: 메인 플로우 차트와 원의 집합을 나란히 배치
col1, col2 = st.columns([3, 1])  # 비율을 조정하여 공간 배분

with col1:
    # Show flow chart only if not 'Disinfection'
    if not st.session_state.selected_process.startswith("4️⃣"):
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

with col
