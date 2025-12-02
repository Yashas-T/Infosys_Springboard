# CodeGenie AI Assistant

## Project Overview

CodeGenie is an advanced AI-powered coding assistant designed to help developers generate, debug, and understand code across multiple programming languages. It leverages state-of-the-art Large Language Models (LLMs) such as Gemma, DeepSeek Coder, and Phi-2 to provide accurate and context-aware code suggestions. The application is built with a modular architecture, featuring a secure user management system, a dynamic frontend using Streamlit, and a robust backend powered by FastAPI.

## Features

### User Management
-   **Secure Authentication:** User registration and login with hashed passwords and salt.
-   **Role-Based Access Control (RBAC):** Distinct roles for standard Users and Administrators.
-   **Password Policy:** Enforces strong passwords (minimum 8 characters, alphanumeric, and special symbols).
-   **Email Validation:** Strict validation allowing only specific domains and TLDs (e.g., gmail.com, .edu, .in).
-   **Security Questions:** Account recovery mechanism using security questions.

### Code Generation & Explanation
-   **Multi-Model Support:** Users can choose between different LLMs (Gemma-2b, DeepSeek-Coder, Phi-2) for code generation.
-   **Multi-Language Support:** Supports Python, C++, JavaScript, SQL, HTML, CSS, and Java.
-   **Code Explanation:** Provides detailed explanations for code snippets to aid understanding.

### Admin Dashboard
-   **Analytics:** View total queries, active users, and feedback statistics.
-   **User Management:** Promote users to admin roles or delete accounts.
-   **Model Evaluation:** Compare the performance of different models side-by-side.
-   **Global Search:** Search through user activity, feedback, and registered users.

### User History
-   **Activity Logging:** Tracks all user queries, generated code, and feedback.
-   **Download History:** Users can download their activity history in CSV format.

## Prerequisites

To run this project, you need:
-   **Google Colab:** The project is optimized to run in a Google Colab environment with GPU support (T4 recommended).
-   **Hugging Face Account:** An access token is required to download the models.
-   **Ngrok Account:** An authentication token is required to expose the Streamlit app publicly.

## Installation and Setup

1.  **Open the Notebook:** Upload the `CodeGenie_Colab_Complete.ipynb` file to Google Colab.
2.  **Set Runtime Type:** Go to `Runtime` > `Change runtime type` and select `T4 GPU`.
3.  **Configure Environment:**
    -   Run the "Setup Environment Variables" cell.
    -   Enter your Hugging Face Token and Ngrok Token when prompted.
4.  **Run All Cells:** Execute all cells in the notebook sequentially.
    -   This will install dependencies, set up the directory structure, create backend modules, and start the server.
5.  **Access the App:**
    -   Locate the cell running the Streamlit app (usually the last cell).
    -   Click the public URL provided by Ngrok (e.g., `https://xxxx-xx-xx-xx-xx.ngrok-free.app`).

## Usage Guide

### Registration
1.  Navigate to the "Sign up" tab on the landing page.
2.  Enter a Username, Email, and Password.
3.  Select a Security Question and provide an Answer.
4.  Click "Sign up" to create your account.

### Generating Code
1.  Log in with your credentials.
2.  Select "CodeGenie" from the sidebar navigation.
3.  Enter your coding prompt in the text area.
4.  Select the desired Programming Language and AI Model.
5.  Click "Generate Code" to receive the output.

### Admin Functions
1.  Log in with an account that has Admin privileges.
2.  Navigate to "Admin Dashboard" in the sidebar.
3.  Use the tabs to view metrics, manage members, or evaluate models.

## Project Structure

-   **backend/**: Contains Python modules for core logic (user management, JWT, model loading, etc.).
-   **streamlit_app/**: Contains the main frontend application (`app.py`) and styling assets.
-   **users.json**: Stores user credentials and profile information.
-   **user_activity.json**: Logs user interactions and history.

## Technologies Used

-   **Frontend:** Streamlit
-   **Backend:** FastAPI, Uvicorn
-   **AI/ML:** PyTorch, Transformers, BitsAndBytes
-   **Authentication:** PyJWT
-   **Utilities:** Pandas, Matplotlib
