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

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig_donut = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 비율 및 편수"
)

fig_donut.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig_donut, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("박스오피스 상위권 영화 중 특정 장르의 비중이 얼마나 높은지 전체적인 분포 형태를 확인할 수 있습니다.")

st.divider()

# ==============================================================================
# Section 2: 장르 및 영화별 총 관객 수 (트리맵)
# ==============================================================================
st.header("2. 장르 및 영화별 총 관객 수 분포")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 및 영화별 관객 수 (칸 크기: 총 관객 수)"
)

fig_treemap.update_traces(
    hovertemplate="<b>영화명: %{label}</b><br>총 관객 수: %{value:,}명"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("장르별 전체 관객 점유율뿐만 아니라, 특정 장르 내에서 어떤 흥행작이 총 관객 수를 주도했는지 한눈에 비교할 수 있습니다.")

st.divider()

# ==============================================================================
# Section 3: 총 관객 수 분포 (히스토그램)
# ==============================================================================
st.header("3. 총 관객 수 분포")

# 히스토그램 생성
fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=20,
    title="총 관객 수(total_audi) 히스토그램",
    labels={'total_audi': '총 관객 수(명)'}
)

fig_hist.update_traces(
    hovertemplate="<b>관객 수 구간: %{x}</b><br>영화 수: %{y}편"
)

fig_hist.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 수 (편)"
)

st.plotly_chart(fig_hist, use_container_width=True)

# 주요 데이터 계산 (최고 흥행작 분석)
max_audi_row = df.loc[df['total_audi'].idxmax()]
max_movie_name = max_audi_row['movieNm']
max_audi_val = max_audi_row['total_audi']

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 박스오피스 상위권 영화는 **하위 구간(대략 100만~300만 명대)**에 밀집되어 있으며, "
    f"오른쪽으로 갈수록 편수가 급격히 줄어드는 전형적인 오른쪽 꼬리가 긴(Right-skewed) 분포를 보입니다.\n\n"
    f"🎬 **가장 관객 수가 많은 영화**: **{max_movie_name}** ({max_audi_val:,}명)"
)

st.divider()

# 원본 데이터 미리보기
with st.expander("원본 데이터 보기"):
    st.dataframe(df)
