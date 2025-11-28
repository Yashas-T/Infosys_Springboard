import torch
import logging
from .model_loader import get_model

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_code(prompt: str, language: str, model_name: str = "gemma") -> str:
    """
    Generate code using the specified model.
    """
    model, tokenizer = get_model(model_name)
    if not model or not tokenizer:
        return "Error: Model not loaded. Please check logs."

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if model_name == 'gemma':
            messages = [{"role": "user", "content": f"Write {language} code for:\n{prompt}"}]
            formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        elif model_name == 'deepseek':
            messages = [{"role": "user", "content": f"You are an expert coding assistant. Write {language} code for: {prompt}"}]
            formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        elif model_name == 'phi-2':
            formatted_prompt = f"Instruct: Write {language} code for {prompt}\nOutput:"
        else:
            formatted_prompt = f"Generate {language} code: {prompt}"

        inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=300, 
                do_sample=True, 
                temperature=0.2,
                pad_token_id=tokenizer.eos_token_id
            )

        text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        
        # Post-processing to clean up the output
        if model_name == 'gemma':
            # Gemma chat template output usually contains the prompt, we might want to strip it if needed
            # But apply_chat_template usually handles it. 
            # Sometimes we need to split by <start_of_turn>model
            if "<start_of_turn>model" in text:
                text = text.split("<start_of_turn>model")[-1].strip()
        elif model_name == 'phi-2':
             if "Output:" in text:
                text = text.split("Output:")[-1].strip()

        return text.strip()

    except Exception as e:
        logger.error(f"Error generating code: {e}")
        return f"Error: {str(e)}"
