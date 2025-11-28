import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel, BitsAndBytesConfig
import os
from dotenv import load_dotenv

load_dotenv()

# Models Configuration
MODELS_CONFIG = {
    "gemma": "google/gemma-2b-it",
    "deepseek": "deepseek-ai/deepseek-coder-1.3b-instruct",
    "phi-2": "microsoft/phi-2"
}

@st.cache_resource
def load_models():
    models = {}
    tokenizers = {}
    
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("HF_TOKEN not found in environment variables.")
        # In a real app, we might want to fail gracefully or log this
        # return None, None

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading models on {device}...")

    # Quantization Config (4-bit)
    if device == "cuda":
        qconf = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4"
        )
    else:
        qconf = None

    for name, model_id in MODELS_CONFIG.items():
        try:
            print(f"Loading {name} ({model_id})...")
            tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token, trust_remote_code=True)
            
            # Apply specific chat template for Gemma
            if name == "gemma":
                tokenizer.chat_template = (
                    "{% for message in messages %}"
                    "{% if message['role'] == 'user' %}"
                    "<start_of_turn>user\n{{ message['content'] }}<end_of_turn>\n"
                    "{% elif message['role'] == 'model' %}"
                    "<start_of_turn>model\n{{ message['content'] }}<end_of_turn>\n"
                    "{% endif %}"
                    "{% endfor %}"
                    "{% if add_generation_prompt %}"
                    "<start_of_turn>model\n"
                    "{% endif %}"
                )

            # Load Model
            if device == "cuda":
                model = AutoModelForCausalLM.from_pretrained(
                    model_id, 
                    token=hf_token,
                    quantization_config=qconf,
                    device_map="auto",
                    trust_remote_code=True
                )
            else:
                model = AutoModelForCausalLM.from_pretrained(
                    model_id, 
                    token=hf_token,
                    trust_remote_code=True
                ).to(device)

            models[name] = model
            tokenizers[name] = tokenizer
            print(f"✅ {name} loaded successfully.")
            
        except Exception as e:
            print(f"❌ Failed to load {name}: {e}")
            # st.error(f"Failed to load {name}: {e}")

    return models, tokenizers

def get_model(model_name):
    models, tokenizers = load_models()
    if models and model_name in models:
        return models[model_name], tokenizers[model_name]
    return None, None
