import streamlit as st

st.set_page_config(page_title="Codebase RAG",page_icon="🤖",layout="wide")

st.title("🤖 Codebase RAG")
st.subheader("AI Software Engineer")

st.write(
    "Ask questions about a GitHub repository using Retrieval-Augmented Generation."
)

st.divider()

repo_url = st.text_input("GitHub Repository URL",placeholder="Repo URL")

if st.button("Analyze Repository"):
    if not repo_url:
        st.warning("Please enter a GitHub repository URL.")
    else:
        st.success(f"Repository received: {repo_url}")

st.divider()
st.subheader("Ask a Question")

question = st.text_input(
    "What would you like to know about the codebase?",
    placeholder="Where is HTTP authentication handled?"
)


if st.button("Ask AI"):
    if not question:
        st.warning("Please enter a question.")
    else:
        st.info(f"Question received: {question}")