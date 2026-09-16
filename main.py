import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
    "1년간 박스오피스 10위권에 든 영화 중 해당 기간 개봉작 216편의 데이터 시각화 도감입니다."
)


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: '|' 기호로 구분된 복수 장르 중 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0])

    return df


df = load_data()

st.divider()

# --- Section 1: 장르별 영화 편수 (도넛 그래프) ---
st.header("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    title="장르별 영화 편수 비율",
)
fig1.update_traces(
    hoverinfo="label+value+percent", textinfo="label+percent"
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True, key="plotly_donut_chart")

# 그래프 분석 텍스트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 특정 장르에 개봉작이 집중되어 있는지, 혹은 다양한 장르가 균등하게 분포되어 있는지 비율을 통해 직관적으로 확인할 수 있습니다."
)

st.divider()

# --- Section 2: 장르 및 영화별 총 관객 수 (트리맵 그래프) ---
st.header("2. 장르 및 영화별 총 관객 수 트리맵")

# Plotly 트리맵 그래프 생성
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객 수 분포",
    hover_data={"total_audi": ":,f"},
)

# 툴팁 서식 커스텀 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True, key="plotly_treemap_chart")

# 그래프 분석 텍스트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 어떤 장르가 전체 관객 수의 큰 비중을 차지하는지, 그리고 해당 장르 내에서 어떤 영화가 관객 동원을 주도했는지 한눈에 파악할 수 있습니다."
)

st.divider()

# --- Section 3: 총 관객 수 분포 (히스토그램) ---
st.header("3. 총 관객 수 히스토그램")

# 최다 관객 영화 정보 동적 계산
top_movie = df.sort_values(by="total_audi", ascending=False).iloc[0]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

# Plotly 히스토그램 그래프 생성
fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객 수 분포 현황",
    labels={"total_audi": "총 관객 수 (명)", "count": "영화 수"},
)
fig3.update_traces(
    hovertemplate="총 관객 수 구간: %{x:,}명<br>영화 수: %{y}편<extra></extra>"
)

# X축 단위 설정 및 레이아웃 다듬기
fig3.update_layout(xaxis_title="총 관객 수 (명)", yaxis_title="영화 수 (편)")

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True, key="plotly_histogram_chart")

# 그래프 분석 텍스트 구역
st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 박스오피스 10위권 영화는 하위 구간(약 100만~300만 명 이하)에 밀집되어 있으며, 상위 흥행작으로 갈수록 영화 수가 급격히 줄어드는 전형적인 비대칭(L자형) 분포를 보입니다. "
    f"가장 관객이 많은 영화는 **'{top_movie_name}'** (약 {top_movie_audi:,.0f}명)입니다."
)
