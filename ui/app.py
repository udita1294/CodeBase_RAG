import streamlit as st

from ingestion.indexer import RepositoryIndexer
from retrieval.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="Codebase RAG",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Codebase RAG")
st.subheader("AI Software Engineer")

st.write(
    "Understand GitHub repositories using "
    "Retrieval-Augmented Generation."
)


st.divider()


# ============================================================
# Repository
# ============================================================

st.subheader("📦 Repository")

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/psf/requests"
)


if st.button("Analyze Repository"):

    if not repo_url:
        st.warning(
            "Please enter a GitHub repository URL."
        )

    else:

        with st.spinner(
            "Cloning and indexing repository..."
        ):

            collection_name = "requests_codebase"

            indexer = RepositoryIndexer(
                collection_name=collection_name
            )

            try:

                result = indexer.index_repository(
                    repo_url
                )

                st.session_state[
                    "collection_name"
                ] = collection_name

                st.session_state[
                    "repository_indexed"
                ] = True

                st.success(
                    "Repository indexed successfully!"
                )

                st.write(
                    f"📁 Files: {result['files']}"
                )

                st.write(
                    f"🧩 Chunks: {result['chunks']}"
                )

            except Exception as e:

                st.error(
                    f"Indexing failed: {str(e)}"
                )


st.divider()


# ============================================================
# Question
# ============================================================

st.subheader("💬 Ask About the Codebase")


question = st.text_input(
    "Your question",
    placeholder=(
        "How does the requests library "
        "send an HTTP request?"
    )
)


if st.button("Ask AI"):

    if not question:

        st.warning(
            "Please enter a question."
        )

    elif not st.session_state.get(
        "repository_indexed",
        False
    ):

        st.warning(
            "Please analyze a repository first."
        )

    else:

        collection_name = st.session_state[
            "collection_name"
        ]

        with st.spinner(
            "Analyzing the codebase..."
        ):

            try:

                rag = RAGPipeline(
                    collection_name=collection_name
                )

                result = rag.answer(
                    question
                )

                st.subheader("🤖 Answer")

                st.write(
                    result["answer"]
                )

                st.subheader("📚 Sources")

                for source in result["sources"]:

                    st.markdown(
                        f"""
**File:** `{source['file_path']}`

**Type:** `{source['type']}`

**Name:** `{source['name']}`

**Lines:** `{source['start_line']}-{source['end_line']}`

**Score:** `{source['score']:.4f}`
"""
                    )

                    st.divider()

            except Exception as e:

                st.error(
                    f"Failed to answer question: {str(e)}"
                )