# YouTube Assistant 

A Streamlit app that turns any YouTube video into an interactive assistant.  
Just enter a YouTube video URL, ask a question, and get accurate answers based on the video’s transcript.  

Deployed successfully on streamlit, access here -> https://ytassistantbydp.streamlit.app/

Built with [LangChain](https://www.langchain.com/), Gemini (Google Generative AI), Hugging Face embeddings, and FAISS.

---

## Features

- 🔗 Enter any YouTube video URL
- 💬 Ask natural language questions about the video content
- 🤖 Powered by Gemini and LangChain for smart responses
- 🗂️ Uses FAISS for efficient similarity search on transcripts
- 🌐 Deployed easily on Streamlit Cloud

---

## Tech Stack
- [Streamlit](https://streamlit.io/) - UI for user interaction
- [LangChain](https://www.langchain.com/) - LLM chaining and orchestration
- [Google Gemini](https://ai.google.dev/) - Answer generation
- [Hugging Face Transformers](https://huggingface.co/) - Sentence embeddings
- [FAISS](https://faiss.ai/) - Vector database for similarity search
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/) - Fetching video transcripts

---

## Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/devanshpursnanii/youtube-assistant.git
   cd youtube-assistant
