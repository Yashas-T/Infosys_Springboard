import torch
import logging
from .model_loader import get_model

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def explain_code(code: str, style: str, model_name: str = "deepseek") -> str:
    """
    Explain code using the specified model and style.
    """
    model, tokenizer = get_model(model_name)
    if not model or not tokenizer:
        return "Error: Model not loaded."

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        prompt_content = f"Explain this {style} code:\n\n{code}"
        
        if model_name == 'gemma':
            messages = [{"role": "user", "content": prompt_content}]
            formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        elif model_name == 'deepseek':
            messages = [{"role": "user", "content": prompt_content}]
            formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        elif model_name == 'phi-2':
            formatted_prompt = f"Instruct: {prompt_content}\nOutput:"
        else:
            formatted_prompt = prompt_content

        inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=250, 
                temperature=0.7, 
                do_sample=True, 
                pad_token_id=tokenizer.eos_token_id
            )

        text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        
        # Post-processing
        if model_name == 'gemma':
            if "<start_of_turn>model" in text:
                text = text.split("<start_of_turn>model")[-1].strip()
        elif model_name == 'phi-2':
             if "Output:" in text:
                text = text.split("Output:")[-1].strip()
                
        return text.strip()

    except Exception as e:
        logger.error(f"Error explaining code: {e}")
        return f"Error: {str(e)}"
