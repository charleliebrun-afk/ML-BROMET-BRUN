import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Library Recommender", page_icon="📖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background-image: url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(10, 6, 2, 0.82);
    z-index: 0;
}

.block-container { position: relative; z-index: 1; padding-top: 3rem; }

h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 3rem !important;
    font-weight: 700 !important;
    color: #e8d5a3 !important;
    letter-spacing: -0.5px;
    margin-bottom: 0 !important;
}

.subtitle {
    color: #9a8a6a;
    font-size: 1rem;
    font-style: italic;
    margin-top: 6px;
    margin-bottom: 4px;
    font-family: 'Playfair Display', serif;
}

.stat { color: #6a5a3a; font-size: 0.78rem; margin-bottom: 28px; letter-spacing: 0.05em; }

.divider { border: none; border-top: 1px solid #3a2e1e; margin: 20px 0; }

.section-title {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6a5a3a;
    margin-bottom: 14px;
}

.history-tag {
    display: inline-block;
    background: rgba(232, 213, 163, 0.08);
    color: #9a8a6a;
    border: 1px solid #3a2e1e;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    margin: 3px;
}

.book-card {
    background: rgba(20, 14, 6, 0.85);
    border: 1px solid #3a2e1e;
    border-radius: 10px;
    padding: 14px;
    height: 580px;
    display: flex;
    flex-direction: column;
    transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease;
    cursor: pointer;
    backdrop-filter: blur(8px);
}

.book-card:hover {
    box-shadow: 0 12px 40px rgba(232, 213, 163, 0.12);
    transform: translateY(-4px);
    border-color: #6a5030;
}

.book-cover {
    width: 100%;
    height: 190px;
    object-fit: cover;
    border-radius: 6px;
    margin-bottom: 12px;
}

.no-cover {
    height: 190px;
    background: rgba(232, 213, 163, 0.04);
    border: 1px solid #2a1e0e;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4a3a20;
    font-size: 0.72rem;
    text-align: center;
    padding: 10px;
    margin-bottom: 12px;
    font-family: 'Playfair Display', serif;
    font-style: italic;
}

.book-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e8d5a3;
    line-height: 1.3;
    font-family: 'Playfair Display', serif;
}

.book-author { font-size: 0.73rem; color: #7a6a4a; margin-top: 4px; }
.book-meta { font-size: 0.7rem; color: #5a4a2a; margin-top: 3px; }
.book-description { font-size: 0.71rem; color: #7a6a4a; line-height: 1.5; margin-top: 6px; flex-grow: 1; overflow: hidden; }

.login-container {
    max-width: 420px;
    margin: 80px auto;
    background: rgba(15, 10, 4, 0.92);
    border: 1px solid #3a2e1e;
    border-radius: 16px;
    padding: 48px 40px;
    backdrop-filter: blur(12px);
    text-align: center;
}

.login-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #e8d5a3;
    margin-bottom: 6px;
}

.login-subtitle {
    color: #6a5a3a;
    font-size: 0.85rem;
    font-style: italic;
    margin-bottom: 32px;
    font-family: 'Playfair Display', serif;
}

div[data-testid="stTextInput"] input {
    background: rgba(232, 213, 163, 0.06) !important;
    border: 1px solid #3a2e1e !important;
    border-radius: 8px !important;
    color: #e8d5a3 !important;
    padding: 12px 16px !important;
}

div[data-testid="stTextInput"] label {
    color: #7a6a4a !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

div[data-testid="stButton"] button {
    background: #8a6a30 !important;
    color: #f5e8c0 !important;
    border: none !important;
    padding: 12px 28px !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    transition: background 0.2s !important;
    width: 100% !important;
}

div[data-testid="stButton"] button:hover { background: #a07840 !important; }

div[data-testid="stNumberInput"] input {
    background: rgba(232, 213, 163, 0.06) !important;
    border: 1px solid #3a2e1e !important;
    color: #e8d5a3 !important;
    border-radius: 8px !important;
}

.stRadio label { color: #9a8a6a !important; }
.stRadio div { gap: 12px !important; }
[data-testid="stMarkdownContainer"] p { color: #9a8a6a; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    base_url = "https://raw.githubusercontent.com/charleliebrun-afk/ML-BROMET-BRUN/main/kaggle_data"
    interactions = pd.read_csv(f"{base_url}/interactions_train.csv")
    items = pd.read_csv(f"{base_url}/items.csv")
    return interactions, items


@st.cache_data
def load_predictions():
    base_url = "https://raw.githubusercontent.com/charleliebrun-afk/ML-BROMET-BRUN/main/kaggle_data"
    try:
        preds = pd.read_csv(f"{base_url}/final_sub.csv")
        return preds
    except:
        return None


@st.cache_data
def get_google_books_info(isbn):
    if pd.isna(isbn) or isbn == "":
        return {}
    isbn = str(isbn).split(";")[0].strip().replace("-", "")
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
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


def get_recommendations(user_id, items_df, interactions_df, predictions_df):
    user_id = int(user_id)  # force int pour éviter les problèmes de type float vs int
    already_read = set(interactions_df[interactions_df["u"] == user_id]["i"].values)
    if predictions_df is not None:
        row = predictions_df[predictions_df["user_id"] == user_id]
        if not row.empty:
            rec_ids = list(map(int, row.iloc[0]["recommendation"].split()))
            return rec_ids, already_read
    popular = (
        interactions_df[~interactions_df["i"].isin(already_read)]
        .groupby("i").size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(10)
    )
    return popular["i"].tolist(), already_read


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "users_db" not in st.session_state:
    st.session_state.users_db = {}


if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-container">
        <div class="login-title">Library</div>
        <div class="login-subtitle">Your personal reading companion</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        mode = st.radio("", ["Sign in", "Register"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.markdown("<br>", unsafe_allow_html=True)

        if mode == "Register":
            if st.button("Create account"):
                if username and password:
                    if username in st.session_state.users_db:
                        st.error("Username already exists.")
                    else:
                        st.session_state.users_db[username] = password
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                else:
                    st.warning("Please fill in all fields.")
        else:
            if st.button("Sign in"):
                if username in st.session_state.users_db and st.session_state.users_db[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")


else:
    interactions, items = load_data()
    predictions = load_predictions()

    col_title, col_logout = st.columns([6, 1])
    with col_title:
        st.markdown("<h1>Library</h1>", unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Your personal reading companion</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="stat">A collection of {len(items):,} books · {len(interactions):,} reading records</p>', unsafe_allow_html=True)
    with col_logout:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Sign out"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.85rem; color:#6a5a3a; margin-bottom:6px; letter-spacing:0.05em;">ENTER YOUR USER ID</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        user_id = st.number_input("", min_value=0,
            max_value=int(interactions["u"].max()), value=42, step=1,
            label_visibility="collapsed",
            key="user_id_input")
    with col2:
        search = st.button("Get recommendations")

    if search:
        user_id = st.session_state["user_id_input"]
        recommended_ids, already_read = get_recommendations(user_id, items, interactions, predictions)

        st.markdown('<p class="section-title">Reading history</p>', unsafe_allow_html=True)
        history = items[items["i"].isin(already_read)].head(8)
        if history.empty:
            st.markdown('<p style="color:#4a3a20;font-size:0.85rem;font-style:italic;">No history found for this reader.</p>', unsafe_allow_html=True)
        else:
            tags_html = "".join([
                f'<span class="history-tag">{str(row["Title"]).rstrip("/").strip()[:35]}</span>'
                for _, row in history.iterrows()
            ])
            st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-title">Recommended for you</p>', unsafe_allow_html=True)

        rec_books = items[items["i"].isin(recommended_ids)].copy()
        rec_books = rec_books.set_index("i").reindex(recommended_ids).reset_index()

        cols = st.columns(5)
        for i, (_, book) in enumerate(rec_books.head(10).iterrows()):
            with cols[i % 5]:
                title = str(book.get("Title", "Unknown title")).rstrip("/").strip()
