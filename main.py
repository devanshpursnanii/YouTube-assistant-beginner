import streamlit as st
import lang
import textwrap

st.set_page_config(page_title="YouTube Assistant")

st.title("YouTube Assistant")

with st.sidebar:
    with st.form(key="my-form"):
        yt_url = st.text_input("YouTube Video URL", placeholder="Enter YouTube video URL here")
        query = st.text_input("Query", placeholder="Enter your question here")
        submit_button = st.form_submit_button(label="Submit")

if submit_button and yt_url and query:
    with st.spinner("Processing..."):
        try:
            db = lang.create_db(yt_url)
            response = lang.query_db(db, query, k=5)

            st.subheader("Answer:")
            st.text(textwrap.fill(response, width=85))
        except Exception as e:
            st.error(f"An error occurred: {e}")
