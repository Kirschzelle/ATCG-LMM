from llama_cpp import Llama
from main import get_model

class LLM():
    def __init__(self) -> None:
        self.lmm = Llama(
            model_path=get_model(),
            n_gpu_layers=-1,
            n_ctx=2048
            )
        
    def get_response(self, prompt):
        return self.lmm(
            prompt,
            max_tokens=200,
            temperature=0.7,
            top_p=0.9,
            repeat_penalty=1.1
            )