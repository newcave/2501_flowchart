import streamlit as st
import graphviz
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# 페이지 기본 설정
st.set_page_config(
    page_title="6단계 공정 플로우 차트",
    page_icon="🔄",
    layout="wide"
)

# 사이드바 메뉴
with st.sidebar:
    st.title("⚙️ 공정 선택")
    selected_process = st.radio(
        "확장할 공정을 선택하세요:",
        ["1️⃣ 공정 A", "2️⃣ 공정 B", "3️⃣ 공정 C", "4️⃣ 공정 D", "5️⃣ 공정 E", "6️⃣ 공정 F"]
    )
    st.write("---")
    st.info(f"🔍 **선택된 공정:** {selected_process}")

# 메인 타이틀
st.title("📊 6단계 공정 플로우 차트 및 랜덤 시계열 데이터")

# 공정 흐름도(Flow Chart) - Graphviz 사용
st.subheader("🔗 전체 공정 개요")
flow_chart = graphviz.Digraph(format='png')

# 노드 스타일 설정
node_style = {
    'shape': 'box',
    'style': 'filled',
    'color': 'lightblue',
    'fontname': 'Helvetica'
}

# 6개의 공정 노드 추가 (네모 박스)
flow_chart.node("A", "공정 A\n(원자재 수집)", **node_style)
flow_chart.node("B", "공정 B\n(가공)", **node_style)
flow_chart.node("C", "공정 C\n(조립)", **node_style)
flow_chart.node("D", "공정 D\n(품질 검사)", **node_style)
flow_chart.node("E", "공정 E\n(포장)", **node_style)
flow_chart.node("F", "공정 F\n(출고)", **node_style)

# 시계방향 연결 (좌측 3개, 우측 3개)
flow_chart.edge("A", "B", label="→")
flow_chart.edge("B", "C", label="→")
flow_chart.edge("C", "D", label="↓")
flow_chart.edge("D", "E", label="→")
flow_chart.edge("E", "F", label="→")
flow_chart.edge("F", "A", label="↑")  # 순환 연결

st.graphviz_chart(flow_chart, use_container_width=True)

# 임의의 시계열 데이터 생성 함수
def generate_random_timeseries(process_name, points=100):
    np.random.seed()  # 매번 다른 랜덤 값을 위해 seed 초기화
    dates = pd.date_range(start='2023-01-01', periods=points)
    values = np.random.randn(points).cumsum()  # 임의의 누적합 시계열 데이터

    df = pd.DataFrame({
        'Date': dates,
        'Value': values
    })

    # Plotly 차트 생성
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Value'],
        mode='lines+markers',
        line=dict(color='royalblue'),
        marker=dict(size=6),
        name=f'{process_name} 공정 시계열'
    ))

    fig.update_layout(
        title=f"📈 {process_name} 공정의 임의의 시계열 데이터",
        xaxis_title="날짜",
        yaxis_title="측정 값",
        autosize=True,
        width=1000,
        height=500,
        plot_bgcolor='white'
    )

    return fig

# 선택된 공정에 대한 설명 및 시계열 차트
st.subheader(f"📌 {selected_process} 상세 설명 및 데이터")

if selected_process == "1️⃣ 공정 A":
    st.write("**공정 A (원자재 수집)**: 생산을 위한 원자재를 수집하고 검수하는 단계입니다.")
    st.plotly_chart(generate_random_timeseries("공정 A"), use_container_width=True)

elif selected_process == "2️⃣ 공정 B":
    st.write("**공정 B (가공)**: 원자재를 가공하여 생산에 적합한 형태로 만드는 단계입니다.")
    st.plotly_chart(generate_random_timeseries("공정 B"), use_container_width=True)

elif selected_process == "3️⃣ 공정 C":
    st.write("**공정 C (조립)**: 가공된 부품을 조립하여 제품을 완성하는 단계입니다.")
    st.plotly_chart(generate_random_timeseries("공정 C"), use_container_width=True)

elif selected_process == "4️⃣ 공정 D":
    st.write("**공정 D (품질 검사)**: 조립된 제품의 품질을 검사하여 불량품을 걸러내는 단계입니다.")
    st.plotly_chart(generate_random_timeseries("공정 D"), use_container_width=True)

elif selected_process == "5️⃣ 공정 E":
    st.write("**공정 E (포장)**: 검사 완료된 제품을 포장하여 출고 준비를 마치는 단계입니다.")
    st.plotly_chart(generate_random_timeseries("공정 E"), use_container_width=True)

elif selected_process == "6️⃣ 공정 F":
    st.write("**공정 F (출고)**: 포장된 제품을 고객에게 출고하는 최종 단계입니다.")
    st.plotly_chart(generate_random_timeseries("공정 F"), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | 문의: sunghoonkim@kwater.or.kr")
