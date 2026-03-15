import litellm

def summarize_text(text: str, task: str, model: str) -> str:
    """
    Condense extracted document into highly relevant context for a specific user task.
    """
    messages = [
        {"role": "system", "content": f"You are a helpful assistant. Your task is to extract highly relevant context from the given document to fulfill this user task: '{task}'."},
        {"role": "user", "content": f"Here is the document text:\n\n{text}"}
    ]

    response = litellm.completion(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content
