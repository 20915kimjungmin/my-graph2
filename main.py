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

    # 문자열 처리 및 결측치 방지
    df["genre"] = df["genre"].fillna("기타").astype(str).str.split("|").str[0]
    df["nation"] = df["nation"].fillna("기타").astype(str)

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
    "💡 **이 그래프로 알 수 있는 것:** 무슨 장르 영화가 제일 많이 나왔는지, 어떤 장르가 인기 있어서 많이 만들어졌는지 동그라미 조각 크기로 딱 보여요!"
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
    "💡 **이 그래프로 알 수 있는 것:** 네모 칸이 클수록 손님이 엄청 많이 온 영화예요! 어떤 장르가 대박 났고 그 안에서 제일 잘나간 영화가 뭔지 보여요."
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
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 관객 수가 왼쪽 밑에 몰려있고, 진짜 대박 난 영화는 몇 개 안 돼요! 제일 대박 난 영화는 **'{top_movie_name}'** (약 {top_movie_audi:,.0f}명)이에요."
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
    "💡 **이 그래프로 알 수 있는 것:** 처음 틀어주는 영화관(스크린) 수가 많을수록 손님도 많은 편이에요. 하지만 영화관 수가 적었어도 입소문 타고 대박 난 대단한 영화들도 보여요!"
)

st.divider()

# --- Section 5: 주요 장르별 총 관객 수 분포 (박스플롯) ---
st.header("5. 주요 장르별 총 관객 수 박스플롯")

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
    "💡 **이 그래프로 알 수 있는 것:** 영화가 많이 나오는 대표 장르들끼리 비교해 볼 수 있어요! 상자 위로 톡 튀어나온 점들은 같은 장르 안에서도 혼자 엄청 대박 난 특출난 영화들이에요."
)

st.divider()

# --- Section 6: 스크린 수, 총 관객 수, 첫 주 관객 수의 관계 (버블 차트) ---
st.header("6. 스크린 수와 총 관객 수, 첫 주 관객 수 버블 차트")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
    title="개봉일 스크린 수 대 총 관객 수 (원 크기: 개봉 첫 주 관객 수)",
    labels={
        "first_scrn": "개봉일 스크린 수 (개)",
        "total_audi": "총 관객 수 (명)",
        "first_week_audi": "개봉 첫 주 관객 수 (명)",
        "genre": "장르",
    },
)
fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<br>첫 주 관객 수: %{marker.size:,}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True, key="plotly_bubble_chart")

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 동그라미 크기가 클수록 개봉하자마자 첫 주에 손님이 구름처럼 몰려든 영화예요! 첫 주에 엄청나게 몰린 영화가 최종 관객 수도 많은지 한눈에 비교해 볼 수 있어요."
)

st.divider()

# --- Section 7: 제작 국가 및 장르별 영화 편수 (선버스트 그래프) ---
st.header("7. 제작 국가 및 장르별 영화 편수 선버스트")

# 계층 데이터 사전 집계로 ValueError 오류 방지
df_sunburst = (
    df.groupby(["nation", "genre"]).size().reset_index(name="count")
)

fig7 = px.sunburst(
    df_sunburst,
    path=["nation", "genre"],
    values="count",
    title="제작 국가 및 장르별 영화 편수 구조",
)
fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True, key="plotly_sunburst_chart")

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 알록달록한 과녁 모양 알맹이예요! 안쪽 원(나라)을 먼저 보고, 밖으로 뻗어 나간 조각(장르)을 보면서 어느 나라에서 어떤 종류의 영화를 많이 만들었는지 한눈에 알 수 있어요."
)

st.divider()

# --- Section 8: 10위권에 머문 날수와 총 관객 수 (막대그래프) ---
st.header("8. 10위권 아래의 영화 상영관의 관객수는 몇명인가")

fig8 = px.bar(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="10위권 아래의 영화 상영관의 관객수는 몇명인가",
    labels={
        "days_in_top10": "10위권에 머문 날수 (일)",
        "total_audi": "총 관객 수 (명)",
        "genre": "장르",
    },
)
fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>10위권 머문 날수: %{x}일<br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig8, use_container_width=True, key="plotly_bar_chart")

st.info(
    "💡 **이 그래프로 알 수 있는 것:** TOP 10에 오래오래 남아있던 영화일수록 사람들이 훨씬 많이 찾아와서 총 관객 수가 엄청나게 커진 것을 볼 수 있어요!"
)
