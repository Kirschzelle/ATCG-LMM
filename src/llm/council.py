from llama_cpp import Llama

def get_council_response(message):
    llm = Llama(
        model_path="gemma-2-2b-it-Q8_0.gguf",
        n_gpu_layers=-1,
        )

    system_message = """You are Bob, the adviser for King Charly, who rules over the Emperion.
    Give clear, wise, and respectful advice to the king."""

    user_message = "The king asks you if it is reasonable to prepare for a war that might come in the future."

    prompt = f"""[INSTRUCTION]
    {system_message}

    [INPUT]
    {user_message}

    [RESPONSE]"""

    resp = llm(
        prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1
        )
    
    print(resp['choices'][0]['text'].strip())
    return resp['choices'][0]['text'].strip()