import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ShopSense", layout="wide")
st.markdown("""<style>
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
.stApp {background:#0F1226;}
[data-testid="stSidebar"] {background:#0B0E20;}
.block-container {padding-top:1.5rem; max-width:1200px;}
.hero {display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:30px; color:#fff;}
.hero span {color:#9A9DBF; font-size:14px;}
.pill {background:#2A2455; color:#C9BCFF; padding:4px 12px; border-radius:20px; font-size:12px;}
.kpi {background:#1B1F3D; border-radius:14px; padding:16px 18px; border:1px solid #2A2F55;}
.kl {color:#9A9DBF; font-size:13px;}
.kv {font-size:32px; font-weight:600; margin-top:2px;}
.ks {color:#9A9DBF; font-size:12px;}
.ins {background:#1B1F3D; border-radius:14px; padding:14px 16px; border-left:4px solid #8B6CFF; color:#E8E9F5; font-size:14px;}
.sec {color:#fff; font-size:17px; font-weight:600; margin:18px 0 6px;}
</style>""", unsafe_allow_html=True)

all_df = pd.read_csv("data/processed/reviews_with_sentiment.csv")
all_asp = pd.read_csv("data/processed/aspect_sentiment.csv")

st.sidebar.markdown("### ShopSense")
st.sidebar.caption("Review analyzer")
choice = st.sidebar.selectbox("Product", ["All"] + sorted(all_df["product_name"].unique()))
df, asp = all_df, all_asp
if choice != "All":
    df = all_df[all_df["product_name"] == choice]
    asp = all_asp[all_asp["product_name"] == choice]

st.markdown(f'<div class="hero"><div><h1>ShopSense</h1><span>E-commerce product intelligence and review analyzer</span></div><div class="pill">{choice} | practice sample</div></div>', unsafe_allow_html=True)

colors = {"positive": "#8B6CFF", "neutral": "#4F5B93", "negative": "#FF6B8B"}

def kpi(label, value, sub="", color="#fff"):
    return f'<div class="kpi"><div class="kl">{label}</div><div class="kv" style="color:{color}">{value}</div><div class="ks">{sub}</div></div>'

def style(fig, h=340):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=h, margin=dict(t=30, b=10, l=10, r=10), legend_title_text="",
                      legend=dict(orientation="h", y=1.12, x=0),
                      font=dict(color="#C9CBE6", size=12), bargap=0.35)
    fig.update_xaxes(gridcolor="#23284A", zeroline=False)
    fig.update_yaxes(gridcolor="#23284A", zeroline=False)
    return fig

def show(fig, h=340):
    st.plotly_chart(style(fig, h), use_container_width=True, config={"displayModeBar": False})

avg = df["rating"].mean()
pos = (df["sentiment"] == "positive").mean() * 100
tab1, tab2, tab3 = st.tabs(["Overview", "Products", "Reviews"])

with tab1:
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Total reviews", len(df), "in current view"), unsafe_allow_html=True)
    k2.markdown(kpi("Average rating", "n/a" if pd.isna(avg) else round(avg, 2), "out of 5"), unsafe_allow_html=True)
    k3.markdown(kpi("Positive %", round(pos, 1), "VADER baseline", "#8B6CFF"), unsafe_allow_html=True)
    k4.markdown(kpi("Products", df["product_name"].nunique(), "in current view", "#E8E9F5"), unsafe_allow_html=True)

    left, right = st.columns([2, 3])
    with left:
        st.markdown('<div class="sec">Sentiment distribution</div>', unsafe_allow_html=True)
        counts = df["sentiment"].value_counts().reset_index()
        counts.columns = ["sentiment", "count"]
        fig = px.pie(counts, names="sentiment", values="count", hole=0.62,
                     color="sentiment", color_discrete_map=colors)
        fig.update_traces(textfont_color="#ffffff", marker=dict(line=dict(color="#0F1226", width=3)))
        show(fig)
    with right:
        st.markdown('<div class="sec">Aspect-based sentiment</div>', unsafe_allow_html=True)
        table = asp.groupby(["aspect", "sentiment"]).size().reset_index(name="count")
        order = table.groupby("aspect")["count"].sum().sort_values().index.tolist()
        fig = px.bar(table, y="aspect", x="count", color="sentiment", orientation="h",
                     barmode="stack", color_discrete_map=colors, category_orders={"aspect": order})
        show(fig)

    st.markdown('<div class="sec">Key insights</div>', unsafe_allow_html=True)
    neg = asp[asp["sentiment"] == "negative"]["aspect"].value_counts()
    tot = asp["aspect"].value_counts()
    posr = asp.assign(p=asp["sentiment"] == "positive").groupby("aspect")["p"].agg(["mean", "count"])
    posr = posr[posr["count"] >= 5].sort_values("mean", ascending=False)
    i1, i2, i3 = st.columns(3)
    if len(neg) > 0:
        i1.markdown(f'<div class="ins">Most negative mentions: <b>{neg.index[0]}</b> ({neg.iloc[0]} of {tot[neg.index[0]]})</div>', unsafe_allow_html=True)
    if len(posr) > 0:
        i2.markdown(f'<div class="ins">Best liked aspect (5+ mentions): <b>{posr.index[0]}</b> ({round(posr.iloc[0]["mean"] * 100)}% positive)</div>', unsafe_allow_html=True)
    i3.markdown('<div class="ins">Small sample: treat these as hints, not conclusions.</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sec">Product explorer</div>', unsafe_allow_html=True)
    prod = all_df.groupby("product_name").agg(price=("price", "first"), avg_rating=("rating", "mean"),
                                              reviews=("review_text", "count"),
                                              positive_pct=("sentiment", lambda s: round((s == "positive").mean() * 100)))
    prod["avg_rating"] = prod["avg_rating"].round(2)
    st.dataframe(prod.sort_values("avg_rating", ascending=False), use_container_width=True)
    st.markdown('<div class="sec">Price vs average rating</div>', unsafe_allow_html=True)
    fig = px.scatter(prod.reset_index(), x="price", y="avg_rating", hover_name="product_name",
                     color_discrete_sequence=["#8B6CFF"])
    fig.update_traces(marker=dict(size=11))
    show(fig, 360)
    st.caption("Each product has only 1-2 ratings, so averages are unstable.")

with tab3:
    st.markdown('<div class="sec">Reviews</div>', unsafe_allow_html=True)
    st.dataframe(df[["product_name", "rating", "sentiment", "review_text"]], use_container_width=True)
    st.download_button("Download filtered reviews (CSV)", df.to_csv(index=False), "reviews_filtered.csv", "text/csv")