from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import re

api_key = st.secrets["GOOGLE_API_KEY"]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    # Handles both youtu.be and youtube.com URLs
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL.")

# load and create vector database from YouTube video using youtube-transcript-api
def create_db(video_url: str):
    video_id = extract_video_id(video_url)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise ValueError(f"Could not load transcript: {e}")

    # combine transcript into a single string
    transcript = " ".join([entry['text'] for entry in transcript_list])

    if not transcript.strip():
        raise ValueError("Transcript is empty or could not be processed.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.create_documents([transcript])

    if not docs:
        raise ValueError("Transcript could not be split into chunks.")

    db = FAISS.from_documents(docs, embeddings)
    return db

# query the database using Gemini model
def query_db(db, query, k):
    if not query.strip():
        return "No query provided."

    docs = db.similarity_search(query, k=k)
    if not docs:
        return "No relevant content found to answer your query."

    docs_content = " ".join([doc.page_content for doc in docs])
    if not docs_content.strip():
        return "Transcript is empty or could not be processed."

    docs_content = docs_content[:3000]  # Truncate to prevent token overload

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
    )

    prompt = PromptTemplate(
        input_variables=["docs", "question"],
        template="""
You are a helpful YouTube assistant. Use the following transcript context to answer the user's question.

Context:
{docs}

Question:
{question}

If you don't know the answer, respond with "Hmm, I'm not sure." Do not make up any information.
Answer concisely and accurately.
"""
    )

    chain = prompt | llm
    response = chain.invoke({"docs": docs_content, "question": query})
    return response.content.replace("\n", " ")


# Example usage
if __name__ == "__main__":
    db = create_db("https://youtu.be/lG7Uxts9SXs?si=MGVJFH1akk8Zl75B")
    response = query_db(db, "whats the video title", k=1)
    print(response)