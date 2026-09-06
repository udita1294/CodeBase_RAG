from retrieval.retriever import CodeRetriever
from retrieval.context_builder import ContextBuilder
from llm.client import LLMClient


class RAGPipeline:

    def __init__(self,collection_name="codebase"):
        self.retriever = CodeRetriever(collection_name=collection_name)
        self.context_builder = ContextBuilder()
        self.llm = LLMClient()

    def answer(self,question,top_k=5):
        # 1. Retrieve relevant code
        results = self.retriever.retrieve(query=question,top_k=top_k)

        # 2. Build context
        context = self.context_builder.build(results)

        # 3. Generate answer
        answer = self.llm.generate(question=question,context=context)

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "file_path": result.payload.get("file_path"),
                    "name": result.payload.get("name"),
                    "type": result.payload.get("type"),
                    "start_line": result.payload.get("start_line"),
                    "end_line": result.payload.get("end_line"),
                    "score": result.score,
                }
                for result in results
            ]
        }