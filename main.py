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
    "💡 **이 그래프로 알 수 있는 것:** 무슨 장르 영화가 제일 많이 나왔고, 어떤 장르가 인기 있어서 많이 만들어졌는지를 한눈에 볼 수 있다"
)
# ── 그래프 2. 장르 안의 영화 (트리맵) ──
st.header("2. 장르 안의 영화 (트리맵)")
fig2 = px.treemap(df, path=["장르", "movieNm"], values="total_audi",
                  hover_data=["total_audi"])
st.plotly_chart(fig2, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 네모 칸이 클수록 사람들이 많이 봤다는 것을 알 수 있다. 어떤 장르가 흥행했고 그 안에서 어떤 영화가 잘 나갔는지를 볼 수 있다.")

# ── 그래프 3. 총 관객의 분포 (히스토그램) ──
st.header("3. 총 관객의 분포 (히스토그램)")
fig3 = px.histogram(df, x="total_audi", nbins=40)
st.plotly_chart(fig3, width="stretch")
under_1m = (df["total_audi"] < 1_000_000).sum()
best = df.loc[df["total_audi"].idxmax()]
st.write(f"216편 가운데 {under_1m}편이 100만 명 미만입니다. "
         f"가장 많이 본 영화는 {best['movieNm']}({best['total_audi']:,}명)입니다.")
st.caption("이 그래프로 알 수 있는 것: 대부분의 영화는 관객 수가 왼쪽 밑에 몰려있고, 진짜 흥행한 영화는 몇 개 안된다는 것을 알 수 있다.")

# ── 그래프 4. 스크린 수와 총 관객 (산점도) ──
st.header("4. 개봉일 스크린 수와 총 관객 (산점도)")
fig4 = px.scatter(df, x="first_scrn", y="total_audi", color="장르",
                  hover_name="movieNm")
st.plotly_chart(fig4, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 처음 틀어주는 영화관(스크린) 수가 많을수록 사람도 많다는 것을 알 수 있다.")

# ── 그래프 5. 장르별 총 관객 (박스플롯) ──
st.header("5. 장르별 총 관객 (박스플롯)")
big = df["장르"].value_counts()
big = big[big >= 10].index
fig5 = px.box(df[df["장르"].isin(big)], x="장르", y="total_audi", points="outliers",
              hover_name="movieNm")
st.plotly_chart(fig5, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 영화가 많이 개봉하는 대표 장르들끼리 비교해 볼 수 있다. 상자 위로 톡 튀어나온 점들은 같은 장르 안에서도 흥행에 성공한 영화들이다.")

# ── 그래프 6. 첫 주 관객을 점 크기로 (버블) ──
st.header("6. 첫 주 관객을 점 크기로 (버블)")
fig6 = px.scatter(df, x="first_scrn", y="total_audi", color="장르",
                  size="first_week_audi", size_max=40, hover_name="movieNm")
st.plotly_chart(fig6, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 산점도의 두 축을 통해 첫 주에 이미 관객수의 승부가 난다는 것을 알 수 있다.")

# ── 그래프 7. 국가에서 장르로 (선버스트) ──
st.header("7. 국가에서 장르로 (선버스트)")
df["대표국가"] = df["nation"].str.split("|").str[0]
counted = (df.groupby(["대표국가", "장르"], as_index=False)
             .agg(편수=("movieNm", "count")))
fig7 = px.sunburst(counted, path=["대표국가", "장르"], values="편수")
st.plotly_chart(fig7, width="stretch")
st.caption("이 그래프로 알 수 있는 것: 그래프에서 어떤 나라의 영화가 더 많고 어떤 장르가 더 많은지를 고리로 한눈에 이해할 수 있다.")

st.divider()

# --- Section 8: 10위권에 머문 날수와 총 관객 수 (막대그래프) ---
st.header("8. 10위권 아래의 영화 상영관의 관객수는 몇명인가")

# Plotly 막대그래프 생성
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

# 툴팁 서식 커스텀 설정 (막대에 마우스 올렸을 때 영화명 표시)
fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>10위권 머문 날수: %{x}일<br>총 관객 수: %{y:,}명<extra></extra>"
)

# 그래프 출력 (key 지정)
st.plotly_chart(fig8, use_container_width=True, key="plotly_bar_chart")

# 그래프 분석 텍스트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** TOP 10에 오래오래 남아있던 영화일수록 사람들이 훨씬 많이 찾아와서 총 관객 수가 엄청나게 커진 것을 볼 수 있어요!"
)
