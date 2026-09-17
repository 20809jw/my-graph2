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

max_audi_row = df.loc[df['total_audi'].idxmax()]
max_movie_name = max_audi_row['movieNm']
max_audi_val = max_audi_row['total_audi']

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 박스오피스 상위권 영화는 하위 구간(대략 100만~300만 명대)에 밀집되어 있으며, "
    f"오른쪽으로 갈수록 편수가 급격히 줄어드는 전형적인 오른쪽 꼬리가 긴(Right-skewed) 분포를 보입니다.\n\n"
    f"🎬 **가장 관객 수가 많은 영화**: **{max_movie_name}** ({max_audi_val:,}명)"
)

st.divider()

# ==============================================================================
# Section 4: 개봉일 스크린수와 총 관객 수의 관계 (산점도)
# ==============================================================================
st.header("4. 개봉일 스크린 수 vs 총 관객 수 관계 (산점도)")

fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린 수 대비 총 관객 수 관계",
    labels={
        'first_scrn': '개봉일 스크린 수(개)',
        'total_audi': '총 관객 수(명)',
        'genre': '장르'
    }
)

fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명"
)

fig_scatter.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("개봉일 스크린 수가 많을수록 대체로 총 관객 수도 증가하는 양의 상관관계를 보이지만, 스크린 수가 적음에도 불구하고 높은 총 관객 수를 기록한 입소문 흥행작(아웃라이어)도 확인할 수 있습니다.")

st.divider()

# ==============================================================================
# Section 5: 주요 장르별 총 관객 수 분포 (박스플롯)
# ==============================================================================
st.header("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

genre_counts_series = df['genre'].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df['genre'].isin(top_genres)]

fig_box = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points='outliers',
    title="영화 수 10편 이상 장르의 총 관객 수 상자 그림",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수(명)'
    }
)

fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명"
)

fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_box, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("장르별 관객 수의 중간값과 편차 범위(IQR)를 한눈에 비교할 수 있으며, 상자 밖으로 벗어난 이상치 점들을 통해 해당 장르 내 독보적인 스매시 히트작을 파악할 수 있습니다.")

st.divider()

# ==============================================================================
# Section 6: 개봉일 스크린 수 vs 총 관객 수 vs 개봉 첫 주 관객 (버블 그래프)
# ==============================================================================
st.header("6. 개봉일 스크린 수 vs 총 관객 수 (버블: 개봉 첫 주 관객)")

fig_bubble = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=60,
    title="개봉일 스크린 수 대비 총 관객 수 (점 크기: 개봉 첫 주 관객)",
    labels={
        'first_scrn': '개봉일 스크린 수(개)',
        'total_audi': '총 관객 수(명)',
        'genre': '장르',
        'first_week_audi': '개봉 첫 주 관객 수(명)'
    }
)

fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<br>개봉 첫 주 관객 수: %{size:,}명"
)

fig_bubble.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)"
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("네 번째 그래프에 '개봉 첫 주 관객 수'라는 변수를 버블의 크기로 추가했습니다. 개봉일 스크린 수가 많을수록 초기 흥행(버블 크기)에 유리하며, 이것이 최종 흥행(Y축 위치)까지 이어지는 경향을 시각적으로 확인할 수 있습니다.")

st.divider()

# ==============================================================================
# Section 7: 제작 국가 및 장르별 영화 편수 (선버스트)
# ==============================================================================
st.header("7. 제작 국가 및 장르별 영화 편수 (선버스트)")

# 계층 구조 표현을 위해 국가 및 장르별로 영화 편수 사전 집계
sunburst_df = df.groupby(['nation', 'genre']).size().reset_index(name='count')

fig_sunburst = px.sunburst(
    sunburst_df,
    path=['nation', 'genre'],
    values='count',
    color='nation',
    title="제작 국가 및 장르별 영화 편수 (칸 크기: 영화 편수)"
)

fig_sunburst.update_traces(
    hovertemplate="<b>국가/장르: %{label}</b><br>영화 편수: %{value}편<br>상위 항목 대비 비율: %{percentParent:.1%}"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

st.subheader("💡 이 그래프로 알 수 있는 것")
st.info("제작 국가별 영화 비중과 함께, 각 국가 내부에서 어떤 장르가 주로 주를 이루는지 동심원 형태의 계층 구조로 파악할 수 있습니다.")

st.divider()

# 원본 데이터 미리보기
with st.expander("원본 데이터 보기"):
    st.dataframe(df)
