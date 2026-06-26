from groq import Groq
from utils.retriever import retrieve_context


class CustomerSupportBot:

    def __init__(self, api_key):

        self.client = Groq(
            api_key=api_key
        )

    def generate_answer(
        self,
        question,
        vector_store
    ):

        context = retrieve_context(
            question,
            vector_store
        )

        if not context.strip():

            return "Information not found in the knowledge base."

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI Customer Support Assistant.

Rules:
1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. Do NOT make assumptions.
4. If the answer is not available in the context, reply exactly:

Information not found in the knowledge base.

5. Keep answers clear and professional.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{question}
"""
                }
            ],

            temperature=0
        )

        answer = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        # Prevent explanations for out-of-context questions
        blocked_phrases = [
            "provided context",
            "given context",
            "does not mention",
            "does not contain",
            "not available in the context",
            "i don't have information",
            "i do not have information"
        ]

        if any(
            phrase in answer.lower()
            for phrase in blocked_phrases
        ):
            return "Information not found in the knowledge base."

        return answer