import streamlit as st

# Apply page-wide styles
def set_page_style():
    st.markdown(
        """
        <style>
        /* Overall page background and text color */
        .stApp {
            background-color: #e0e0e0;  /* light grey */
            color: #000000 !important;  /* force black text */
        }

        /* Sidebar background and text */
        .css-1d391kg {
            background-color: #c0c0c0;
            color: #000000 !important;
        }

        /* Score cards text color */
        div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] h1, div[data-testid="stMarkdownContainer"] h2 {
            color: #000000 !important;
        }

        /* Hide Streamlit default footer and menu */
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Custom header
def app_header(title):
    st.markdown(f"<h1 style='text-align:center;color:black;'>{title}</h1>", unsafe_allow_html=True)

# Score card (per subject)
def score_card(subject, score, max_score=20):
    st.markdown(
        f"""
        <div style="
            background-color:#b0b0b0;
            padding:10px;
            margin:5px 0;
            border-radius:10px;
            text-align:center;
            font-weight:bold;
            font-size:16px;
            color:black;">
            {subject}: {score}/{max_score}
        </div>
        """,
        unsafe_allow_html=True
    )

# Progress bar helper (keeps default but text is black above)
def progress_bar(score, max_score=20):
    st.progress(min(score/max_score,1.0))
