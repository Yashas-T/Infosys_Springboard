# Code Analysis and Explanation with Multiple Models

This notebook provides a comprehensive analysis of Python code snippets, employing techniques from AST parsing and tokenization to generating explanations using different SentenceTransformer models. It also includes various visualizations to understand code characteristics and compare the outputs of different models.

## Table of Contents

- [Setup & Imports](#section-1--setup--imports)
- [Sample Code](#section-2--sample-code)
- [Parse AST](#section-3--parse-ast)
- [Extract Functions](#section-4--extract-functions)
- [Extract Classes](#section-5--extract-classes)
- [Extract Imports](#section-6--extract-imports)
- [Tokenize Code](#section-7--tokenize-code)
- [Token Patterns](#section-8--token-patterns)
- [Line-by-Line Explanation](#section-9--line-by-line-explanation)
- [Keyword Frequency Visualization](#section-10--keyword-frequency-visualization)
- [Operator Frequency Visualization](#section-11--operator-frequency-visualization)
- [Token Type Distribution](#section-12--token-type-distribution)
- [Line Length Distribution](#section-13--line-length-distribution)
- [Summary Report](#section-14--summary-report)
- [Multi-Model Code Explainer Module](#section-15--multi-model-code-explainer-module)
- [Explanation Difference Visualization](#section-16--explanation-difference-visualization)
- [Wordcloud for three models](#section-17--wordcloud-for-three-models)
- [PCA of Code Snippet Embeddings](#section-18--keyword-frequency-heatmap)
- [Keyword Frequency Heatmap](#section-19--pca-of-code-snippet-embeddings)


## How to Run

1. Open the notebook in Google Colab.
2. Run all the cells in sequence. The necessary libraries will be installed automatically.

## Notebook Sections Explained

- **Section 1: Setup & Imports**: Installs required libraries and imports necessary modules for code analysis and visualization.
- **Section 2: Sample Code**: Defines the list of Python code snippets that will be analyzed. You can replace these with your own code.
- **Section 3: Parse AST**: Parses each code snippet into its Abstract Syntax Tree (AST) representation for structural analysis.
- **Section 4: Extract Functions**: Identifies and extracts information about functions defined in the code snippets.
- **Section 5: Extract Classes**: Identifies and extracts information about classes defined in the code snippets.
- **Section 6: Extract Imports**: Identifies and extracts information about imported modules in the code snippets.
- **Section 7: Tokenize Code**: Breaks down the code into individual tokens (words, operators, etc.) for further analysis.
- **Section 8: Token Patterns**: Analyzes the frequency of keywords and operators used in the code.
- **Section 9: Line-by-Line Explanation**: Generates a basic explanation for each significant line of code.
- **Section 10: Keyword Frequency Visualization**: Visualizes the frequency of Python keywords using a bar chart.
- **Section 11: Operator Frequency Visualization**: Visualizes the frequency of operators used in the code using a bar chart.
- **Section 12: Token Type Distribution**: Shows the distribution of different token types (keywords, identifiers, operators, etc.) in a pie chart.
- **Section 13: Line Length Distribution**: Displays the distribution of line lengths in the code using a histogram.
- **Section 14: Summary Report**: Provides a summary of key metrics from the code analysis, such as the total number of functions, classes, imports, and tokens.
- **Section 15: Multi-Model Code Explainer Module**: Defines a class to generate code explanations using multiple pre-trained SentenceTransformer models and compares their outputs.
- **Section 16: Explanation Difference Visualization**: Visualizes the number of lines for which different models provided different explanations using a bar chart.
- **Section 17: Wordcloud for three models**: Generates word clouds for the explanations produced by each SentenceTransformer model to visualize the most frequent terms used.
- **Section 18: PCA of Code Snippet Embeddings**: Performs Principal Component Analysis (PCA) on the embeddings of the code snippets to visualize them in a reduced-dimensionality space.
- **Section 19: Keyword Frequency Heatmap**: Visualizes the frequency of keywords across different code snippets using a heatmap.
