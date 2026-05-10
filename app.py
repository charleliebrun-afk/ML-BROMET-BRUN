import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Library Recommender", page_icon="📖", layout="wide")

st.markdown("""
<style>
    .main { background-color: #fafaf8; }
    h1 { font-size: 2rem; font-weight: 600; color: #1a1a1a; letter-spacing: -0.5px; }
    .subtitle { color: #888; font-size: 1rem; margin-top: -10px; margin-bottom: 30px; }
    .section-title { font-size: 0.85rem; font-weight: 600; letter-spacing: 0.1em;
        text-transform: uppercase; color: #aaa; margin-bottom: 15px; }
    .history-tag { display: inline-block; background: #f0ede8; color: #555;
        padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; margin: 3px; }
    .book-card { background: #fff; border: 1px solid #f0ede8; border-radius: 10px;
        padding: 12px; height: 480px; display: flex; flex-direction: column; }
    .book-cover { width: 100%; height: 180px; object-fit: cover;
        border-radius: 6px; margin-bottom: 10px; }
    .no-cover { height: 180px; background: #f0ede8; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        color: #bbb; font-size: 0.75rem; text-align: center;
        padding: 10px; margin-bottom: 10px; }
    .book-title { font-size: 0.82rem; font-weight: 600; color: #1a1a1a; line-height: 1.3; }
    .book-author { font-size: 0.75rem; color: #999; margin-top: 3px; }
    .book-meta { font-size: 0.72rem; color: #bbb; margin-top: 3px; }
    .book-description { font-size: 0.73rem; color: #777; line-height: 1.5;
        margin-top: 6px; flex-grow: 1; overflow: hidden; }
    div[data-testid="stButton"] button {
        background: #1a1a1a; color: white; border: none;
        padding: 10px 24px; border-radius: 6px; font-size: 0.9rem;
        font-weight: 500; cursor: pointer; }
    div[data-testid="stButton"] button:hover { background: #333; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base_url = "https://raw.githubusercontent.com/charleliebrun-afk/ML-BROMET-BRUN/87b14e8d13483b707fc94db41bc47da4f8469bf6/kaggle_data"
    interactions = pd.read_csv(f"{base_url}/interactions_train.csv")
    items = pd.read_csv(f"{base_url}/items.csv")
    return interactions, items

interactions, items = load_data()

@st.cache_data
def get_google_books_info(isbn):
    if pd.isna(isbn) or isbn == "":
        return {}
    isbn = str(isbn).split(";")[0].strip().replace("-", "")
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&langRestrict=en"
        r = requests.get(url, timeout=3).json()
        items_gb = r.get("items", [])
        if items_gb:
            info = items_gb[0]["volumeInfo"]
            return {
                "cover": info.get("imageLinks", {}).get("thumbnail"),
                "description": info.get("description", ""),
                "pages": info.get("pageCount"),
                "categories": info.get("categories", []),
                "rating": info.get("averageRating"),
            }
    except:
        pass
    return {}

def get_cover_url(isbn):
    if pd.isna(isbn) or isbn == "":
        return None
    isbn = str(isbn).split(";")[0].strip().replace("-", "")
    try:
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return url
    except:
        pass
    info = get_google_books_info(isbn)
    return info.get("cover")

def get_recommendations(user_id, n=10):
    already_read = set(interactions[interactions["u"] == user_id]["i"].values)
    popular = (
        interactions[~interactions["i"].isin(already_read)]
        .groupby("i").size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(n)
    )
    return popular["i"].tolist(), already_read

# Header
st.markdown("<h1>Library Recommender</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover books you might love, based on your reading history.</p>',
    unsafe_allow_html=True)

st.markdown('<p style="font-size:0.9rem; color:#aaa; margin-bottom:6px;">Enter your user ID to get personalised book recommendations</p>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    user_id = st.number_input("User ID", min_value=0,
        max_value=int(interactions["u"].max()), value=42, step=1,
        label_visibility="collapsed")
with col2:
    search = st.button("Get recommendations")

if search:
    recommended_ids, already_read = get_recommendations(user_id)

    st.markdown('<p class="section-title">Reading history</p>', unsafe_allow_html=True)
    history = items[items["i"].isin(already_read)].head(8)
    if history.empty:
        st.markdown('<p style="color:#aaa;font-size:0.85rem;">No history found for this user.</p>',
            unsafe_allow_html=True)
    else:
        tags_html = "".join([
            f'<span class="history-tag">{str(row["Title"]).rstrip("/").strip()[:35]}</span>'
            for _, row in history.iterrows()
        ])
        st.markdown(tags_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">You might also like</p>', unsafe_allow_html=True)

    rec_books = items[items["i"].isin(recommended_ids)].head(10)
    cols = st.columns(5)
    for i, (_, book) in enumerate(rec_books.iterrows()):
        with cols[i % 5]:
            title = str(book.get("Title", "Unknown title")).rstrip("/").strip()
            author = str(book.get("Author", "Unknown author")).rstrip("/").strip()
            isbn = book.get("ISBN Valid", None)

            cover_url = get_cover_url(isbn)
            gb_info = get_google_books_info(isbn) if not pd.isna(str(isbn)) else {}

            if cover_url:
                cover_html = f'<img src="{cover_url}" class="book-cover"/>'
            else:
                cover_html = f'<div class="no-cover">{title[:40]}</div>'

            meta = ""
            if gb_info.get("pages"):
                meta += f'{gb_info["pages"]} pages'
            if gb_info.get("categories"):
                meta += f' · {gb_info["categories"][0]}'

            desc = ""
            if gb_info.get("description"):
                desc = gb_info["description"][:120] + "..."

            stars = ""
            if gb_info.get("rating"):
                stars = "★" * int(gb_info["rating"]) + "☆" * (5 - int(gb_info["rating"]))

            card_html = f"""
            <div class="book-card">
                {cover_html}
                <div class="book-title">{title[:40]}</div>
                <div class="book-author">{author[:35]}</div>
                <div class="book-meta">{meta}</div>
                <div class="book-meta">{stars}</div>
                <div class="book-description">{desc}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
