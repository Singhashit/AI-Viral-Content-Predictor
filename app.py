import streamlit as st
import pandas as pd
import re
from googleapiclient.discovery import build
from openai import OpenAI

# ================= CONFIG =================
YOUTUBE_API_KEY = "AIzaSyASlMAt59Xkz_CTOQ7Yf-bBqZoG49QLocY"
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

st.set_page_config(page_title="AI Viral Lab", layout="wide")

# ================= NEW GEN UI =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}
.main-title {
    font-size:42px;
    text-align:center;
    color:#00ffe7;
    font-weight:bold;
}
.glass {
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    margin-bottom:20px;
}
.book {
    background:#111;
    color:#00ffe7;
    padding:20px;
    border-radius:12px;
    font-family:monospace;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 AI Viral Intelligence Lab</div>', unsafe_allow_html=True)

# ================= FUNCTIONS =================
def extract_video_id(url):
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_details(video_id):
    request = youtube.videos().list(part="snippet,statistics", id=video_id)
    response = request.execute()

    if not response["items"]:
        return None

    data = response["items"][0]

    return {
        "title": data["snippet"]["title"],
        "views": int(data["statistics"].get("viewCount", 0)),
        "likes": int(data["statistics"].get("likeCount", 0)),
        "comments": int(data["statistics"].get("commentCount", 0))
    }

# ================= SMART SCORE =================
def smart_score(views, likes, comments):
    engagement = (likes + comments) / views if views else 0
    score = 0

    if views > 1_000_000:
        score += 40
    elif views > 100_000:
        score += 25
    else:
        score += 10

    if engagement > 0.08:
        score += 40
    elif engagement > 0.05:
        score += 30
    else:
        score += 10

    if comments > 10000:
        score += 20

    return min(score, 100), engagement

# ================= EXPLAINABLE AI =================
def explain_viral(views, likes, comments, engagement):
    reasons = []

    if views > 1_000_000:
        reasons.append("🔥 High reach indicates strong algorithm push")
    if engagement > 0.06:
        reasons.append("💡 Strong engagement shows audience interest")
    if comments > 5000:
        reasons.append("💬 High comments boost visibility")

    if not reasons:
        reasons.append("⚠️ Low engagement and reach reducing viral chances")

    return reasons

# ================= HASHTAG GENERATOR =================
def generate_hashtags(title):
    words = title.split()
    base = [w.lower() for w in words if len(w) > 3][:5]

    hashtags = ["#viral", "#trending", "#youtube"]

    for w in base:
        hashtags.append(f"#{w}")

    return hashtags

# ================= SAFE AI INSIGHTS =================
def generate_insights(title):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": f"Give viral strategy for: {title}"}]
        )
        return response.choices[0].message.content
    except:
        return "Focus on strong hook, high engagement, fast pacing, and curiosity-driven content."

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs([
    "📺 Analyzer",
    "📊 Manual",
    "🆚 Compare",
    "🧠 AI Studio"
])

# ================= TAB 1 =================
with tab1:

    url = st.text_input("Paste YouTube Link")

    if st.button("Analyze"):

        vid = extract_video_id(url)

        if vid:
            data = get_video_details(vid)

            if data:
                st.image(f"https://img.youtube.com/vi/{vid}/0.jpg")

                st.write(data)

                score, engagement = smart_score(
                    data["views"], data["likes"], data["comments"]
                )

                st.progress(score)
                st.write(f"🔥 Score: {score}%")

                # Explainable AI
                st.subheader("🧠 WHY this video performs")
                reasons = explain_viral(
                    data["views"], data["likes"], data["comments"], engagement
                )

                for r in reasons:
                    st.write("👉", r)

                # Graph
                st.subheader("📈 Engagement Graph")
                df = pd.DataFrame({
                    "Metric": ["Views", "Likes", "Comments"],
                    "Value": [data["views"], data["likes"], data["comments"]]
                })
                st.bar_chart(df.set_index("Metric"))

                # Hashtags
                st.subheader("🏷️ Suggested Hashtags")
                tags = generate_hashtags(data["title"])
                st.write(" ".join(tags))

                # Insights
                st.subheader("📖 AI Strategy")
                st.markdown(f"<div class='book'>{generate_insights(data['title'])}</div>", unsafe_allow_html=True)

# ================= TAB 2 =================
with tab2:

    views = st.number_input("Views", 0)
    likes = st.number_input("Likes", 0)
    comments = st.number_input("Comments", 0)

    if st.button("Predict"):

        score, engagement = smart_score(views, likes, comments)

        st.progress(score)
        st.write(f"🔥 Score: {score}%")

        reasons = explain_viral(views, likes, comments, engagement)
        for r in reasons:
            st.write("👉", r)

# ================= TAB 3 =================
with tab3:

    url1 = st.text_input("Video 1 URL")
    url2 = st.text_input("Video 2 URL")

    if st.button("Compare"):

        v1 = extract_video_id(url1)
        v2 = extract_video_id(url2)

        if v1 and v2:
            d1 = get_video_details(v1)
            d2 = get_video_details(v2)

            if d1 and d2:
                s1, _ = smart_score(d1["views"], d1["likes"], d1["comments"])
                s2, _ = smart_score(d2["views"], d2["likes"], d2["comments"])

                df = pd.DataFrame({
                    "Metric": ["Views", "Likes", "Comments", "Score"],
                    "Video 1": [d1["views"], d1["likes"], d1["comments"], s1],
                    "Video 2": [d2["views"], d2["likes"], d2["comments"], s2]
                })

                st.table(df)

# ================= TAB 4 =================
with tab4:

    topic = st.text_input("Enter Topic")

    if st.button("Generate Titles"):

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": f"Generate viral titles for {topic}"}]
            )
            titles = response.choices[0].message.content.split("\n")
        except:
            titles = [
                f"🔥 You Won’t Believe This About {topic}",
                f"{topic} Will Shock You 🤯",
                f"Secrets of {topic}",
                f"{topic} Explained Fast",
                f"Why {topic} is Trending"
            ]

        for t in titles:
            st.write("👉", t)