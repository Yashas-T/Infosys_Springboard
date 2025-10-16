# Infosys CodeGenie: AI Explainer and Code Generator  
### **Milestone 2: Code Generation with Interactive UIs and Visualizations**

---

## **Overview**

This project is part of the *Infosys CodeGenie AI Explainer and Code Generator Program (Milestone 2)*.  
It focuses on developing an intelligent system for **code generation**, **evaluation**, and **benchmarking** using **pretrained transformer models** from [Hugging Face](https://huggingface.co/).  

The notebook implements:  
- Code generation using multiple pretrained LLMs  
- Evaluation using metrics such as **Cyclomatic Complexity**, **Maintainability Index**, and **Lines of Code (LOC)**  
- Two interactive UIs for benchmarking and model inspection  
- Visualization of model performance  

---

## **Objectives**

1. **Code Generation Models**
   - [DeepSeek-Coder-1.3B](https://huggingface.co/deepseek-ai/deepseek-coder-1.3b-instruct)       
   - [Gemma-2B-IT](https://huggingface.co/google/gemma-2b-it)  
   - [Stable-Code-3B](https://huggingface.co/stabilityai/stable-code-3b)  

2. **Evaluation Metrics**
   - Cyclomatic Complexity  
   - Maintainability Index  
   - Lines of Code (LOC)

3. **Interactive UIs**
   - **UI #1:** Benchmark All Models  
   - **UI #2:** Inspect Selected Models via Checkboxes

4. **Testing and Visualization**
   - Evaluation across **10 diverse code prompts**  
   - **Performance plots** comparing metrics across models  

---

## **Project Structure**


```plaintext
milestone-2/
│
├── Section 1: Setup and Installations
│   ├── Installs dependencies (transformers, torch, accelerate, radon, matplotlib)
│   └── Imports necessary Python libraries
│
├── Section 2: Configuration & Backend Engine
│   ├── Defines MODELS_TO_TEST dictionary
│   ├── Implements helper functions:
│   │   ├── clean_generated_code()
│   │   ├── is_syntactically_valid()
│   │   ├── calculate_advanced_metrics()
│   │   └── generate_code()
│   └── Handles GPU/CPU device management
│
├── Section 3: Pre-Loading All AI Models
│   ├── Downloads and caches all Hugging Face models
│   └── Stores them for reuse in benchmarking
│
├── Section 4: UI #1 - Benchmark All Models
│   ├── Accepts a code prompt input
│   ├── Generates code from all models
│   ├── Displays code, generation time, and metrics
│   └── Renders results using pandas DataFrame
│
├── Section 5: UI #2 - Inspect Models with Checkboxes
│   ├── Allows selective model benchmarking
│   ├── Uses checkboxes for user input
│   ├── Displays results interactively
│   └── Visualizes performance metrics
│
├── Section 6: Visualization and Analysis
│   ├── Generates comparative performance plots
│   ├── Uses matplotlib for graphical evaluation
│   └── Highlights top-performing models
│
└── Section 7: Conclusion and Observations
    ├── Summarizes results
    └── Lists insights from benchmarking process

```
## **Setup Instructions**

**1. Environment Setup**

Use **Google Colab** with GPU runtime:  

### **2. Required Libraries**

Install all dependencies:
```bash
!pip install transformers torch accelerate radon matplotlib ipywidgets
```
### 3. Hugging Face Authentication

1. Create a Hugging Face account: [https://huggingface.co/](https://huggingface.co/)  

2. Generate a **Read Access Token**:  
   - Go to **Profile → Settings → Access Tokens**

3. Accept model license terms for Gemma:  
   - [Gemma License Page](https://huggingface.co/google/gemma-2b-it)

4. Store your token in Google Colab secrets:
```python
from google.colab import userdata
userdata.set('HF_TOKEN', 'your_huggingface_token_here')
```
## Usage

### UI #1: Benchmark All Models

1. Enter a coding prompt in the text area.  
2. Click **"Run Benchmark"**.  
3. The notebook will:
   - Generate code from all five models  
   - Compute complexity, maintainability, and LOC  
   - Display results in a comparison table  

---

### UI #2: Inspect Models with Checkboxes

1. Select desired models via checkboxes.  
2. Enter a code prompt.  
3. Click **"Generate"** to compare outputs and metrics for the chosen models.  

| Metric                    | Description                                        |
| -------------------------- | -------------------------------------------------- |
| **Cyclomatic Complexity**  | Measures logical decision points in code           |
| **Maintainability Index**  | Estimates code readability and ease of maintenance |
| **Lines of Code (LOC)**    | Counts the number of executable lines              |

# Visualization

The notebook uses **matplotlib** to produce visual plots:

- **Comparison of complexity, maintainability, and LOC**
- **Aggregated performance scores across models**
- **Highlighting the top-performing code generator**

# Results and Observations

- Models exhibit varying trade-offs between complexity and maintainability.
- **Gemma-2B-IT** and **DeepSeek-Coder-1.3B** generally produce readable, efficient code.
- **Stable-Code** excels at compact code but sometimes sacrifices maintainability.
- Visual analysis enables quick assessment of performance patterns across domains.

# References

- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index)
- [Radon Documentation](https://radon.readthedocs.io/)
- Infosys CodeGenie Program Portal
- [Google Colab Documentation](https://colab.research.google.com/notebooks/intro.ipynb)

