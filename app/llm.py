import ollama


def ask_llm(context, question):

    prompt = f"""

    Answer only from given context.

    If answer is not found,
    say "Answer not found".

    Context:
    {context}

    Question:
    {question}

    """

    response = ollama.chat(

        model="llama3",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]