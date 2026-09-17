import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 열 전처리: '|' 구분자로 나눈 후 첫 번째 장르만 추출
    df['genre'] = df['genre'].fillna('기타').astype(str).str.split('|').str[0]
    return df

df = load_data()

# 데이터 요약 정보 표시
st.sidebar.header("데이터 정보")
st.sidebar.write(f"총 영화 수: **{len(df)}편**")

# ==============================================================================
# Section 1: 장르별 영화 편수 (도넛 그래프)
# ==============================================================================
st.header("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 비율 및 편수"
)

# 마우스 오버 시 편수와 비율이 함께 표시되도록 설정
fig_donut.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("박스오피스 상위권 영화 중 특정 장르의 비중이 얼마나 높은지 전체적인 분포 형태를 확인할 수 있습니다.")

st.divider()

# ==============================================================================
# Section 2: 장르 및 영화별 총 관객 수 (트리맵)
# ==============================================================================
st.header("2. 장르 및 영화별 총 관객 수 분포")

# Plotly 트리맵 그래프 생성 (계층 구조: genre -> movieNm)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 및 영화별 관객 수 (칸 크기: 총 관객 수)"
)

# 마우스 오버 시 영화명과 총 관객 수가 명확히 보이도록 설정
fig_treemap.update_traces(
    hovertemplate="<b>영화명: %{label}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 그래프 해석 구역
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("장르별 전체 관객 점유율뿐만 아니라, 특정 장르 내에서 어떤 흥행작이 총 관객 수를 주도했는지 한눈에 비교할 수 있습니다.")

st.divider()

# 원본 데이터 미리보기
with st.expander("원본 데이터 보기"):
    st.dataframe(df)
