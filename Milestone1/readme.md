# CodeGenie AI Explainer and Code Generator

## Project Context

This project was created for the Infosys Virtual Springboard Internship 6.0 and represents the first of four milestones in the development of the "CodeGenie AI" tool.

## Project Overview

### The Goal
The primary objective of the CodeGenie project is to build an AI tool that can explain code snippets with a deep, contextual understanding of the entire project they belong to.

### The Problem
Standard AI code assistants possess general programming knowledge but lack specific context about an individual's unique codebase. This often results in generic or incorrect suggestions.

### Objective of this Milestone
This notebook (Milestone 1) focuses on foundational static analysis techniques. It demonstrates how to parse Python code to extract structural features, analyze token patterns, generate rule-based and model-based explanations, and visualize the code's characteristics. These steps are crucial for understanding and processing the source code that will later be used in the RAG pipeline.



## Table of Contents

1.  [Notebook Analysis Summary](#1-notebook-analysis-summary)
2.  [Comparison of AI Models Used](#2-comparison-of-the-Embedding-models-used)
3.  [Conclusion for Milestone 1](#3-conclusion)
4.  [How to Run](#4-how-to-run)



## 1. Notebook Analysis Summary

Here is a breakdown of the key sections within the Jupyter Notebook and their functions.

### **Setup & Data**
* **1. Setup & Imports**: Prepares the programming environment by installing and importing necessary Python libraries for parsing (`ast`), data handling (`pandas`), plotting (`matplotlib`), and natural language processing (`sentence-transformers`).
* **2. Sample Code**: Defines the dataset for the analysis, which consists of 20 simple Python code snippets that serve as the input for all subsequent analysis.

### **Structural Analysis (AST)**
* **3. Parse AST**: Converts each code snippet into an Abstract Syntax Tree (AST), which is a tree representation of the code's structure that allows for analysis without execution.
* **4. Extract Functions**: Inspects the ASTs to find all function definitions and extracts key information like the function's name, arguments, and whether it has a return statement.
* **5. Extract Classes**: Traverses the ASTs to identify any class definitions. For this dataset, none were found.
* **6. Extract Imports**: Analyzes the ASTs to find all `import` statements, identifying the external libraries each snippet depends on.

### **Tokenization & Pattern Analysis**
* **7. Tokenize Code**: Breaks down the source code into its fundamental components, called **tokens** (e.g., variable names, keywords, operators), and filters out non-essential items like comments.
* **8. Token Patterns**: Counts the frequency of specific token types, such as Python **keywords** (`if`, `for`) and **operators** (`=`, `+`), to provide a statistical overview.

### **Code Explanation & Visualization**
* **9. Line-by-Line Explanation**: Implements a simple, rule-based function to generate a plain-English explanation for each line of code based on pattern matching.
* **10. Keyword Frequency Visualization**: Uses `matplotlib` to create a **bar chart** that visually represents the frequency of each keyword found in the code.
* **11. Operator Frequency Visualization**: Generates a **bar chart** to visualize the frequency of different operators.
* **12. Token Type Distribution**: Classifies all tokens into four categories (`Identifier`, `Operator`, `Keyword`, `Other`) and creates a **pie chart** to show their proportions.
* **13. Line Length Distribution**: Calculates the length of every line of code and plots a **histogram** to show the distribution of line lengths.
* **14. Summary Report**: Compiles all key metrics (total functions, tokens, etc.) into a `pandas` DataFrame for a clean, tabular summary.

### **Advanced Analysis & NLP Models**
* **15. Multi-Model Code Explainer Module**: Introduces an advanced `CodeExplainer` class that uses three pre-trained **SentenceTransformer models** to generate varied, context-aware explanations. This is a foundational step for the project's goal of building a **Retrieval-Augmented Generation (RAG)** application.
* **16. Explanation Difference Visualization**: Counts the number of lines where explanations from two different models (`MiniLM` and `DistilRoBERTa`) do not match and plots the results on a bar chart.
* **17. Word Cloud for Three Models**: Generates a **word cloud** for the explanations from each AI model, offering insight into each model's descriptive style.
* **18. PCA of Code Snippet Embeddings**: Uses **Principal Component Analysis (PCA)** to convert each snippet into a numerical vector (embedding). These are then plotted on a **scatterplot** to visualize the semantic similarity between the code snippets.

---

## 2. Comparison of the Embedding Models Used

The `CodeExplainer` module in this notebook uses three different pre-trained **SentenceTransformer** models. Their selection demonstrates the trade-offs between performance, speed, size, and the style of generated text. The observations below are derived directly from the notebook's implementation and outputs (templates, word clouds, difference counts).

| Model Name | Architecture | Key Characteristics | Performance vs. Speed | Embedding Size | Explanation Style (Observed) | Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`all-MiniLM-L12-v2`** | Distilled Transformer | Very small and extremely fast; optimized for speed with good quality. | **Fastest.** Performance is generally lower than the other two. | 384 dimensions | **Direct and literal.** Uses core action verbs like "Assigns" and "Outputs." | Ideal for real-time applications or environments with limited computational resources. |
| **`all-distilroberta-v1`** | Distilled RoBERTa | A good balance between speed and performance. | **Balanced.** Faster than MPNet but slower than MiniLM. | 768 dimensions | **Balanced and descriptive.** Focuses on the "what" (e.g., "Creates a function for computation"). | A great general-purpose choice where both speed and quality are important. |
| **`all-mpnet-base-v2`** | MPNet | Offers the highest quality and most nuanced embeddings. | **Highest Performance.** The slowest and most resource-intensive. | 768 dimensions | **Action-oriented and formal.** Focuses on the "how" (e.g., "Sets up function to perform a task"). | Best for tasks requiring maximum accuracy where speed is less critical. |

### Summary of Model Differences

The analysis in the notebook (specifically the word clouds and difference visualizations) shows that while all three models produce useful explanations, their output varies in vocabulary and nuance. The **MPNet** model is likely to capture more subtle semantic relationships, whereas **MiniLM** provides a faster, lightweight alternative. This comparison is a crucial step in understanding which model would be best suited for the final **CodeGenie** tool, depending on whether the priority is speed or accuracy.

---

## 3. Conclusion 

The 1st milestone project successfully demonstrates a multi-faceted approach to static Python code analysis. By combining AST parsing, tokenization, and modern NLP techniques, it was possible to extract and quantify a rich set of structural and semantic features from a collection of code snippets.

The visualizations provide clear and intuitive insights into the code's composition, such as keyword frequency and line length distribution. The comparative analysis of different NLP models highlights the potential for generating diverse, context-sensitive code explanations, moving beyond simple rule-based systems. Finally, the PCA visualization of code embeddings effectively shows that code can be clustered based on its semantic meaning, opening up possibilities for tasks like code similarity detection and classification.

---

## 4. How to Run

1.  Ensure you have Python 3 and a virtual environment set up.
2.  Install the required dependencies by running the following commands:
    ```bash
    pip install astunparse tokenize-rt
    pip install transformers sentence-transformers torch
    pip install scikit-learn pandas numpy
    pip install matplotlib wordcloud nltk
    ```
3.  Execute the cells in the Jupyter Notebook `Milestone_1.ipynb` sequentially. The notebook will automatically download the necessary NLTK data and pre-trained models on its first run.
