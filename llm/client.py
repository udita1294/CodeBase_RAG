import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLMClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in .env")
        self.client = Groq(api_key=api_key)


    def generate(self,question,context):

        system_prompt = """
                            You are an AI software engineer specialized in understanding codebases.

                            Answer the user's question using the provided repository context.

                            Rules:

                            1. Use the provided code context as the primary source of truth.

                            2. Do not invent files, functions, classes, or behavior.

                            3. If the context does not contain enough information, say so clearly.

                            4. Mention relevant file paths.

                            5. Mention function or class names when useful.

                            6. Explain the reasoning clearly.

                            7. Keep the answer concise but useful.
                        """

        user_prompt = f"""
                            Repository Context: {context}
                            
                            User Question: {question}
                        """

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0
        )
        return response.choices[0].message.content