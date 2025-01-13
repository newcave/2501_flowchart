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

# 리디렉션 플래그 초기화
if 'redirected' not in st.session_state:
    st.session_state.redirected = False

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
        k2_high = st.slider("AI Low2 (k2 최소 적정범위)", 0.01, 5.0, 0.5)
        
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

# Streamlit Columns: 메인 플로우 차트과 리디렉션 또는 기타 기능을 위한 공간 배치
col1, col2 = st.columns([3, 1])  # 비율을 조정하여 공간 배분

with col1:
    # Flow-Chart 항상 표시
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
        process_name = process_labels.get(clicked_node_id, "Unknown Process")
        st.session_state.selected_process = f"{process_number}️⃣ {process_name}"

with col2:
    # 기존의 Plotly 원 그래프 대신 리디렉션 기능 추가
    # **프로세스 A 선택 시 리디렉션**
    if st.session_state.selected_process.startswith("1️⃣"):
        if not st.session_state.redirected:
            redirect_script = """
            <script>
                window.location.href = "https://mn-prediction-kwaterailab.streamlit.app/";
            </script>
            """
            st.markdown(redirect_script, unsafe_allow_html=True)
            st.session_state.redirected = True
    else:
        # **프로세스 A가 아닐 때**
        st.markdown("### 🔵🟢🔴 프로세스 상태")
        # 여기에 다른 내용을 추가할 수 있습니다. 현재는 빈 공간으로 유지합니다.
        st.write("")

# 메인 타이틀
st.title("📊 Connected Process Flow Chart & Simulator")

# **프로세스 A 선택 시 다른 앱으로 리디렉션**
# col2에서 이미 리디렉션을 처리했으므로, 추가로 메인 영역에서 다시 처리하지 않습니다.

# Disinfection 프로세스가 선택된 경우
if st.session_state.selected_process.startswith("4️⃣"):
    # Disinfection 프로세스에 대한 특정 그래프 표시
    # 'disinfection_inputs'가 세션 상태에 있는지 확인
    if 'disinfection_inputs' not in st.session_state:
        st.warning("사이드바에서 Disinfection 프로세스의 입력을 설정해 주세요.")
    else:
        # 사용자 입력 값 가져오기
        inputs = st.session_state.disinfection_inputs
        DOC = inputs['DOC']
        NH3 = inputs['NH3']
        Cl0 = inputs['Cl0']
        Temp = inputs['Temp']
        max_time = inputs['max_time']
        k1_low = inputs['k1_low']
        k1_high = inputs['k1_high']
        k2_low = inputs['k2_low']
        k2_high = inputs['k2_high']
        
        # EPA 모델에서 k1, k2 계산
        try:
            k1_EPA = np.exp(-0.442 + 0.889 * np.log(DOC) + 0.345 * np.log(7.6 * NH3) - 1.082 * np.log(Cl0) + 0.192 * np.log(Cl0 / DOC))
            k2_EPA = np.exp(-4.817 + 1.187 * np.log(DOC) + 0.102 * np.log(7.6 * NH3) - 0.821 * np.log(Cl0) - 0.271 * np.log(Cl0 / DOC))
        except:
            st.error("EPA 모델 계산을 위한 입력값이 유효하지 않습니다.")
            st.stop()
        
        # Two-phase 모델에서 A, k1, k2 계산
        try:
            A_Two_phase = np.exp(0.168 - 0.148 * np.log(Cl0 / DOC) + 0.29 * np.log(1) - 0.41 * np.log(Cl0) + 0.038 * np.log(1) + 0.0554 * np.log(NH3) + 0.185 * np.log(Temp))
            k1_Two_phase = np.exp(5.41 - 0.38 * np.log(Cl0 / DOC) + 0.274 * np.log(NH3) - 1.12 * np.log(Temp) + 0.05 * np.log(1) - 0.854 * np.log(7))
            k2_Two_phase = np.exp(-7.13 + 0.864 * np.log(Cl0 / DOC) + 2.63 * np.log(DOC) - 2.55 * np.log(Cl0) + 0.62 * np.log(1) + 0.16 * np.log(1) + 0.48 * np.log(NH3) + 1.03 * np.log(Temp))
        except:
            st.error("Two-phase 모델 계산을 위한 입력값이 유효하지 않습니다.")
            st.stop()
        
        # 시간에 따른 농도 계산
        time_range = np.linspace(0, max_time, 100)
        
        # EPA 모델 (원래 입력값으로 계산)
        C_EPA = np.where(time_range <= 5,
                         Cl0 * np.exp(-k1_EPA * time_range),
                         Cl0 * np.exp(5 * (k2_EPA - k1_EPA)) * np.exp(-k2_EPA * time_range))
        
        # 시간에 비례한 랜덤 변동 추가 (최대 20%)
        def apply_time_based_variation(array, max_time):
            variation_factors = 1 + (time_range / max_time * 2) * np.random.uniform(-0.2, 0.4, size=array.shape)
            varied_array = array * variation_factors
            return varied_array
        
        C_EPA_varied = apply_time_based_variation(C_EPA, max_time)
        
        # Two-phase 모델 (원래 입력값으로 계산)
        C_Two_phase = Cl0 * (A_Two_phase * np.exp(-k1_Two_phase * time_range) + (1 - A_Two_phase) * np.exp(-k2_Two_phase * time_range))
        
        # EPA 모델 (사용자가 설정한 k1, k2 범위로 High, Low 계산)
        C_EPA_low = np.where(time_range <= 5,
                             Cl0 * np.exp(-k1_low * time_range),
                             Cl0 * np.exp(5 * (k2_low - k1_low)) * np.exp(-k2_low * time_range))
        
        C_EPA_high = np.where(time_range <= 5,
                              Cl0 * np.exp(-k1_high * time_range),
                              Cl0 * np.exp(5 * (k2_high - k1_high)) * np.exp(-k2_high * time_range))
        
        # 그래프 그리기
        plt.figure(figsize=(10, 6))
        plt.plot(time_range, C_EPA_varied, label='실측데이터 (Virtually Generated)', color='blue', linewidth=3.5)
        #plt.plot(time_range, C_Two_phase, label='Two-phase Model (Original Input)', color='green', linewidth=2.5)
        plt.plot(time_range, C_EPA_low, label='EPA Model Low (User Input)', color='orange', linestyle='--', linewidth=2.5)
        plt.plot(time_range, C_EPA_high, label='EPA Model High (User Input)', color='red', linestyle='--', linewidth=2.5)
        plt.xlabel('Time (hrs)')
        plt.ylabel('Residual Chlorine (mg/L)')
        plt.title('EPA and Two-phase Models of Residual Chlorine')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
        
        # 결과가 범위 내에 있는지 여부를 체크 (0.5시간 이후만)
        is_normal = np.all((C_EPA_varied >= C_EPA_low) & (C_EPA_varied <= C_EPA_high))
        is_initial_phase = time_range <= 0.5
        if is_normal or np.all(is_initial_phase):
            st.subheader("결과: 정상")
            st.markdown("<h1 style='text-align: center; color: green;'>정상</h1>", unsafe_allow_html=True)
        else:
            st.subheader("결과: 비정상")
            st.markdown("<h1 style='text-align: center; color: red;'>비정상</h1>", unsafe_allow_html=True)
else:
    # Disinfection 외의 프로세스가 선택된 경우, 기존의 상세 정보 및 시계열 데이터 표시
    # 시계열 데이터 가져오기
    selected_process_name = st.session_state.selected_process.split(" ", 1)[1]
    timeseries_df = get_timeseries_data(selected_process_name)
    
    # 선택된 프로세스에 따른 상세 정보 및 시계열 차트
    st.subheader(f"📌 {st.session_state.selected_process} Details and Data")
    
    # 상세 설명 및 시계열 데이터 표시
    st.markdown(process_descriptions.get(st.session_state.selected_process, "Select a process from the sidebar."))
    st.plotly_chart(create_timeseries_chart(timeseries_df, selected_process_name), use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | Contact: sunghoonkim@kwater.or.kr")
