import tiktoken
import openai

encoding = tiktoken.get_encoding("cl100k_base")
openai.api_key = "OPENAIKEY"

def count_tokens(string: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The text string.

    Returns:
        int: The number of tokens.
    """
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_embedding(text_to_embed):
    """
    Retrieves the embedding for a given text.

    Args:
        text_to_embed (str): The text to embed.

    Returns:
        str: The embedding.
    """
    response = openai.Embedding.create(model="text-embedding-ada-002", input=[text_to_embed])
    embedding = response["data"][0]["embedding"]
    return embedding