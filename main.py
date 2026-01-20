import streamlit as st
import lang
import textwrap

# ---------- Page config ----------
st.set_page_config(
    page_title="YouTube Assistant",
    page_icon="▶️",
    layout="centered"
)

# ---------- Custom CSS (safe, minimal) ----------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }
    .title-text {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .subtitle-text {
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .answer-box {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.25rem;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown('<div class="title-text">YouTube Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Ask precise questions about any YouTube video transcript</div>',
    unsafe_allow_html=True,
)

# ---------- Sidebar (Inputs) ----------
with st.sidebar:
    st.header("Input")
    with st.form(key="query-form"):
        yt_url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        query = st.text_input(
            "Question",
            placeholder="What is the main argument of the video?"
        )
        submit_button = st.form_submit_button("Analyze")

    st.markdown("---")
    st.caption(
        "• Uses video transcripts only\n"
        "• Answers are grounded in the transcript\n"
        "• No hallucinated content"
    )

# ---------- Main logic ----------
if submit_button:
    if not yt_url or not query:
        st.warning("Please provide both a YouTube URL and a question.")
    else:
        with st.spinner("Analyzing transcript and generating answer..."):
            try:
                db = lang.create_db(yt_url)
                response = lang.query_db(db, query, k=5)

                st.subheader("Answer")
                st.markdown(
                    f'<div class="answer-box">{textwrap.fill(response, width=90)}</div>',
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error("An error occurred while processing the video.")
                st.exception(e)

# ---------- Footer ----------
st.markdown("---")
st.caption("Built with Streamlit · LangChain · Gemini")
