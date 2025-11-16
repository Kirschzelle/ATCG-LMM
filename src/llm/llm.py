import threading
from llama_cpp import Llama
from main import get_model

class LLM():
    def __init__(self) -> None:
        self.lmm = Llama(
            model_path=get_model(),
            n_gpu_layers=-1,
            n_ctx=4096*2,
            verbose=False
            )
        
    def get_response(self, prompt, on_finish=None):
        def worker():
            result = self.lmm(
                prompt,
                max_tokens=200,
                temperature=0.7,
                top_p=0.9,
                repeat_penalty=1.1
            )
            text = result["choices"][0]["text"].strip() # type: ignore
            if on_finish:
                print(f"[DEBUG] Finished LLM execution: {text}")
                on_finish(text)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()