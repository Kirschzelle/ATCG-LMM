

def get_council_response(message):
    system_message = """You are Bob, the adviser for King Charly, who rules over the Emperion.
    Give clear, wise, and respectful advice to the king."""

    user_message = "The king asks you if it is reasonable to prepare for a war that might come in the future."

    prompt = f"""[INSTRUCTION]
    {system_message}

    [INPUT]
    {user_message}

    [RESPONSE]"""
    
    print(resp['choices'][0]['text'].strip())
    return resp['choices'][0]['text'].strip()