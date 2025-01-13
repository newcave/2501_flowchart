import streamlit as st
import graphviz
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# 페이지 기본 설정
st.set_page_config(
    page_title="공정 흐름도 및 시계열 차트",
    page_icon="📈",
    layout="wide"
)

# 사이드바 메뉴
with st.sidebar:
    st.title("⚙️ 공정 선택")
    selected_process = st.radio(
        "확장할 공정을 선택하세요:",
        ["A 공정", "B 공정", "C 공정"]
    )
    st.write("---")
    st.info(f"🔍 **선택된 공정:** {selected_process}")

# 메인 타이틀
st.title("📊 공정 흐름도 및 시계열 데이터")

# 공정 흐름도(Flow Chart) - Graphviz 사용
st.subheader("🔗 전체 공정 개요")
flow_chart = graphviz.Digraph()

# 노드 추가 (A → B → C 공정)
flow_chart.node("A", "A 공정\n(원자재 준비)")
flow_chart.node("B", "B 공정\n(가공 및 조립)")
flow_chart.node("C", "C 공정\n(품질 검사 및 포장)")

# 연결 (Edge)
flow_chart.edge("A", "B", label="재료 이송")
flow_chart.edge("B", "C", label="제품 이동")

st.graphviz_chart(flow_chart, use_container_width=True)

# 임의의 시계열 데이터 생성 함수
def generate_random_timeseries(process_name):
    np.random.seed(42)  # 랜덤 고정
    dates = pd.date_range(start='2023-01-01', periods=100)
    values = np.random.normal(loc=0, scale=1, size=100).cumsum()  # 누적합 (시계열 패턴)
    
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
        marker=dict(size=6),
        name=f'{process_name} 공정 시계열'
    ))
    
    fig.update_layout(
        title=f"{process_name} 공정의 임의의 시계열 데이터",
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

if selected_process == "A 공정":
    st.write("""
    **A 공정(원자재 준비)**는 생산의 첫 단계로, 필요한 원자재를 준비하고 
    품질 검사 및 보관 과정을 포함합니다.
    """)
    st.plotly_chart(generate_random_timeseries("A 공정"), use_container_width=True)

elif selected_process == "B 공정":
    st.write("""
    **B 공정(가공 및 조립)**은 준비된 원자재를 가공하고, 
    조립하는 단계로 주요 생산 활동이 이루어집니다.
    """)
    st.plotly_chart(generate_random_timeseries("B 공정"), use_container_width=True)

elif selected_process == "C 공정":
    st.write("""
    **C 공정(품질 검사 및 포장)**은 완제품의 품질 검사를 거쳐 
    포장 및 출고 준비를 마치는 단계입니다.
    """)
    st.plotly_chart(generate_random_timeseries("C 공정"), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("ⓒ 2025 K-water AI Lab | 문의: sunghoonkim@kwater.or.kr")
