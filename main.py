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
st.plotly_chart(fig1, use_container_width=True)

# 그래프 분석 텍스트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 특정 장르에 개봉작이 집중되어 있는지, 혹은 다양한 장르가 균등하게 분포되어 있는지 비율을 통해 직관적으로 확인할 수 있습니다."
)

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

# 그래프 출력 (key 추가)
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

# 그래프 출력 (key 추가)
st.plotly_chart(fig2, use_container_width=True, key="plotly_treemap_chart")

# 그래프 분석 텍스트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 어떤 장르가 전체 관객 수의 큰 비중을 차지하는지, 그리고 해당 장르 내에서 어떤 영화가 관객 동원을 주도했는지 한눈에 파악할 수 있습니다."
)
