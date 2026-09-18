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

    # 문자열 처리 오류 방지를 위한 .str 접근자 사용
    df["genre"] = df["genre"].fillna("기타").astype(str).str.split("|").str[0]

    return df


df = load_data()

st.divider()

# --- Section 1: 장르별 영화 편수 (도넛 그래프) ---
st.header("1. 장르별 영화 편수 분포")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    title="장르별 영화 편수 비율",
)
fig1.update_traces(hoverinfo="label+value+percent", textinfo="label+percent")

st.plotly_chart(fig1, use_container_width=True, key="plotly_donut_chart")

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 무슨 장르 영화가 제일 많이 나왔고, 어떤 장르가 인기 있어서 많이 만들어졌는지를 한눈에 볼 수 있다.
"
)

st.divider()

# --- Section 2: 장르 및 영화별 총 관객 수 (트리맵 그래프) ---
st.header("2. 장르 및 영화별 총 관객 수 트리맵")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객 수 분포",
    hover_data={"total_audi": ":,f"},
)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True, key="plotly_treemap_chart")

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 네모 칸이 클수록 사람들이 많이 봤다는 것을 알 수 있다. 어떤 장르가 흥행했고 그 안에서 어떤 영화가 잘 나갔는지를 볼 수 있다."
)

st.divider()

# --- Section 3: 총 관객 수 분포 (히스토그램) ---
st.header("3. 총 관객 수 히스토그램")

top_movie = df.sort_values(by="total_audi", ascending=False).iloc[0]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

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
fig3.update_layout(xaxis_title="총 관객 수 (명)", yaxis_title="영화 수 (편)")

st.plotly_chart(fig3, use_container_width=True, key="plotly_histogram_chart")

st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 관객 수가 왼쪽 밑에 몰려있고, 진짜 흥행한 영화는 몇 개 안된다는 것을 알 수 있다.
"
)

st.divider()

# --- Section 4: 개봉일 스크린 수와 총 관객 수의 관계 (산점도) ---
st.header("4. 개봉일 스크린 수와 총 관객 수 산점도")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수 대 총 관객 수 관계",
    labels={
        "first_scrn": "개봉일 스크린 수 (개)",
        "total_audi": "총 관객 수 (명)",
        "genre": "장르",
    },
)
fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True, key="plotly_scatter_chart")

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 처음 틀어주는 영화관(스크린) 수가 많을수록 사람도 많다는 것을 알 수 있다."
)

st.divider()

# --- Section 5: 주요 장르별 총 관객 수 분포 (박스플롯) ---
st.header("5. 주요 장르별 총 관객 수 박스플롯")

# 10편 이상인 장르만 필터링
genre_counts_series = df["genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_major = df[df["genre"].isin(major_genres)]

fig5 = px.box(
    df_major,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",
    title="영화 10편 이상 장르의 총 관객 수 분포 (이상치 포함)",
    labels={"genre": "장르", "total_audi": "총 관객 수 (명)"},
)
fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True, key="plotly_box_chart")

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 영화가 많이 개봉하는 대표 장르들끼리 비교해 볼 수 있다. 상자 위로 톡 튀어나온 점들은 같은 장르 안에서도 흥행에 성공한 영화들이다."
)
