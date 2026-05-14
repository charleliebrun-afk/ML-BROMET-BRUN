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
    height: 660px;
    display: flex;
    flex-direction: column;
    transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease;
    backdrop-filter: blur(8px);
}

.book-card:hover {
    box-shadow: 0 12px 40px rgba(232, 213, 163, 0.12);
    transform: translateY(-4px);
    border-color: #6a5030;
}

.book-cover {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 6px;
    margin-bottom: 12px;
}

.no-cover {
    height: 200px;
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
.book-description {
    font-size: 0.71rem;
    color: #8a7a5a;
    line-height: 1.55;
    margin-top: 8px;
    flex-grow: 1;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
}

.reserved-badge {
    margin-top: 10px;
    background: rgba(232, 213, 163, 0.1);
    border: 1px solid #6a5030 !important;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 0.7rem;
    color: #c8a87a;
    text-align: center;
    letter-spacing: 0.05em;
    outline: none !important;
    box-shadow: none !important;
}

.reservation-card {
    background: rgba(20, 14, 6, 0.85);
    border: 1px solid #3a2e1e;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.reservation-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.82rem;
    color: #e8d5a3;
}

.reservation-info {
    font-size: 0.7rem;
    color: #6a5a3a;
    margin-top: 2px;
}

.reservation-status {
    font-size: 0.68rem;
    color: #c8a87a;
    border: 1px solid #6a5030;
    border-radius: 20px;
    padding: 3px 10px;
    white-space: nowrap;
}

.login-container {
    max-width: 440px;
    margin: 60px auto;
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

div[data-testid="stNumberInput"] input {
    background: rgba(232, 213, 163, 0.06) !important;
    border: 1px solid #3a2e1e !important;
    color: #e8d5a3 !important;
    border-radius: 8px !important;
}

div[data-testid="stNumberInput"] label {
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

div[data-testid="stMarkdownContainer"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

div[data-testid="stMarkdownContainer"] > div {
    border: none !important;
    box-shadow: none !important;
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
    base_url = "https://raw.githubusercontent.com/charleliebrun-afk/ML-BROMET-BRUN/main"
    try:
        return pd.read_csv(f"{base_url}/final_sub.csv")
    except:
        return None


@st.cache_data
def get_google_books_info(isbn=None, title=None, author=None):
    try:
        if isbn and not pd.isna(isbn) and isbn != "":
            isbn_clean = str(isbn).split(";")[0].strip().replace("-", "")
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_clean}"
            r = requests.get(url, timeout=3).json()
            items_gb = r.get("items", [])
            if items_gb:
                info = items_gb[0]["volumeInfo"]
                return {
                    "cover": info.get("imageLinks", {}).get("thumbnail"),
                    "description": info.get("description", ""),
                    "pages": info.get("pageCount"),
                    "rating": info.get("averageRating"),
                }
        if title:
            query = f"intitle:{title}"
            if author and str(author) != "nan":
                query += f"+inauthor:{author}"
            url = f"https://www.googleapis.com/books/v1/volumes?q={requests.utils.quote(query)}&maxResults=1"
            r = requests.get(url, timeout=3).json()
            items_gb = r.get("items", [])
            if items_gb:
                info = items_gb[0]["volumeInfo"]
                return {
                    "cover": info.get("imageLinks", {}).get("thumbnail"),
                    "description": info.get("description", ""),
                    "pages": info.get("pageCount"),
                    "rating": info.get("averageRating"),
                }
    except:
        pass
    return {}


@st.cache_data
def get_cover_url(isbn=None, title=None, author=None):
    if isbn and not pd.isna(isbn) and isbn != "":
        isbn_clean = str(isbn).split(";")[0].strip().replace("-", "")
        try:
            url = f"https://covers.openlibrary.org/b/isbn/{isbn_clean}-M.jpg?default=false"
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                return url
        except:
            pass
    info = get_google_books_info(isbn=isbn, title=title, author=author)
    return info.get("cover")


def get_isbn(book, items_df):
    for col in items_df.columns:
        if "isbn" in col.lower():
            val = book.get(col, "")
            if val and str(val) != "nan":
                return val
    return ""


def clean(val):
    if val is None:
        return ""
    s = str(val).strip()
    return "" if s == "nan" else s


def get_recommendations(user_id, items_df, interactions_df, predictions_df):
    user_id = int(user_id)
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


for key, val in {
    "logged_in": False,
    "username": "",
    "user_id": None,
    "users_db": {},
    "reservations": [],
    "show_reservations": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── LOGIN ─────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-container">
        <div class="login-title">Library</div>
        <div class="login-subtitle">Your personal reading companion</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        mode = st.radio("", ["Sign in", "Create account"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        if mode == "Create account":
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_password2 = st.text_input("Confirm password", type="password")
            new_uid = st.number_input("Library card number", min_value=0, step=1,
                                      help="Your library card number links your account to your reading history.")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create my account"):
                if not new_username or not new_password:
                    st.error("Please fill in all fields.")
                elif new_password != new_password2:
                    st.error("Passwords do not match.")
                elif new_username in st.session_state.users_db:
                    st.error("This username is already taken.")
                else:
                    st.session_state.users_db[new_username] = {
                        "password": new_password,
                        "user_id": int(new_uid),
                    }
                    st.session_state.logged_in = True
                    st.session_state.username = new_username
                    st.session_state.user_id = int(new_uid)
                    st.rerun()
        else:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign in"):
                user = st.session_state.users_db.get(username)
                if user and user["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_id = user["user_id"]
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")


# ── MAIN APP ──────────────────────────────────────────────────────────────────
else:
    interactions, items = load_data()
    predictions = load_predictions()
    user_id = st.session_state.user_id

    col_title, col_res, col_logout = st.columns([5, 1.5, 1])
    with col_title:
        st.markdown("<h1>Library</h1>", unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Your personal reading companion</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="stat">Welcome, {st.session_state.username} · Card #{user_id}</p>', unsafe_allow_html=True)
    with col_res:
        st.markdown("<br><br>", unsafe_allow_html=True)
        res_count = len(st.session_state.reservations)
        label = f"My reservations ({res_count})" if res_count else "My reservations"
        if st.button(label):
            st.session_state.show_reservations = not st.session_state.show_reservations
    with col_logout:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Sign out"):
            st.session_state.logged_in = False
            st.session_state.reservations = []
            st.session_state.show_reservations = False
            st.rerun()

    if st.session_state.show_reservations:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">My reservations</p>', unsafe_allow_html=True)
        if not st.session_state.reservations:
            st.markdown('<p style="color:#4a3a20;font-size:0.85rem;font-style:italic;">No reservations yet.</p>', unsafe_allow_html=True)
        else:
            for r in st.session_state.reservations:
                st.markdown(f"""
                <div class="reservation-card">
                    <div>
                        <div class="reservation-title">{r['title']}</div>
                        <div class="reservation-info">{r['author']} · Reserved for pick-up within 7 days</div>
                    </div>
                    <div class="reservation-status">⏳ Awaiting pick-up</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    recommended_ids, already_read = get_recommendations(user_id, items, interactions, predictions)

    st.markdown('<p class="section-title">Reading history</p>', unsafe_allow_html=True)
    history = items[items["i"].isin(already_read)].head(8)
    if history.empty:
        st.markdown('<p style="color:#4a3a20;font-size:0.85rem;font-style:italic;">No history found for this reader.</p>', unsafe_allow_html=True)
    else:
        tags_html = "".join([
            f'<span class="history-tag">{clean(row["Title"])[:35]}</span>'
            for _, row in history.iterrows()
        ])
        st.markdown(tags_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Recommended for you</p>', unsafe_allow_html=True)

    rec_books = items[items["i"].isin(recommended_ids)].copy()
    rec_books = rec_books.set_index("i").reindex(recommended_ids).reset_index()

    already_reserved = {r["title"] for r in st.session_state.reservations}

    cols = st.columns(5)
    for idx, (_, book) in enumerate(rec_books.head(10).iterrows()):
        with cols[idx % 5]:
            title = clean(book.get("Title", "Unknown title")) or "Unknown title"
            author = clean(book.get("Author", ""))
            year = clean(book.get("Year", ""))
            isbn = get_isbn(book, items)

            cover_url = get_cover_url(isbn=isbn, title=title, author=author)
            gb_info = get_google_books_info(isbn=isbn, title=title, author=author)
            description = clean(gb_info.get("description", ""))
            rating = gb_info.get("rating")
            pages = gb_info.get("pages")

            cover_html = (
                f'<img class="book-cover" src="{cover_url}" alt="">'
                if cover_url
                else f'<div class="no-cover">{title[:40]}</div>'
            )

            meta_parts = []
            if year:
                meta_parts.append(str(int(float(year))) if year.replace(".", "").isdigit() else year)
            if pages:
                meta_parts.append(f"{pages} pages")
            if rating:
                meta_parts.append(f"★ {rating}")
            meta_str = " · ".join(meta_parts)

            is_reserved = title in already_reserved

            st.markdown(f"""
            <div class="book-card">
                {cover_html}
                <div class="book-title">{title[:60]}</div>
                <div class="book-author">{author[:40]}</div>
                <div class="book-meta">{meta_str}</div>
                <div class="book-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)

            if is_reserved:
                st.markdown('<div class="reserved-badge">✓ Reserved — awaiting pick-up</div>', unsafe_allow_html=True)
            else:
                if st.button("Reserve in store", key=f"reserve_{idx}"):
                    st.session_state.reservations.append({
                        "title": title,
                        "author": author,
                        "isbn": isbn,
                    })
                    st.rerun()
