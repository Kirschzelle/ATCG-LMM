from llama_cpp import Llama

def get_council_response():
    llm = Llama(model_path="gemma-2-2b-it-Q8_0.gguf", gpu_layers=99)

    system_message = """You are Bob, the adviser for King Charly, who rules over the Emperion.
    Give clear, wise, and respectful advice to the king, considering political and military implications."""

    user_message = "The king asks you if it is reasonable to prepare for a war that might come in the future."

    prompt = f"""[INSTRUCTION]
    {system_message}

    [INPUT]
    {user_message}

    [RESPONSE]"""

    resp = llm(prompt, max_tokens=200, temperature=0.7)
    print(resp['choices'][0]['text'].strip())
    return resp['choices'][0]['text'].strip()