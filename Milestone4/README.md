# CodeGenie AI Assistant

![CodeGenie Banner](https://img.shields.io/badge/AI-CodeGenie-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=flat-square&logo=streamlit)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=flat-square&logo=fastapi)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-yellow?style=flat-square&logo=huggingface)

**CodeGenie** is a comprehensive, enterprise-grade AI-powered coding assistant designed to enhance software development workflows. By integrating state-of-the-art Large Language Models (LLMs) such as **Gemma**, **DeepSeek Coder**, and **Phi-2**, CodeGenie offers robust capabilities including automated code generation, detailed technical explanations, and a sophisticated administrative dashboard for analytics and user management.

---

## Codebase & Notebook Structure

The CodeGenie project is originally encapsulated in a comprehensive Jupyter Notebook (`CodeGenie_Colab_Complete.ipynb`). For production and modularity, the codebase is structured into distinct modules, each handling specific aspects of the application logic. Below is a detailed description of the components extracted from the notebook:

### Backend Modules (`backend/`)

The core logic of the application resides in the `backend` directory. These modules handle everything from model inference to user authentication.

*   **`model_loader.py`**:
    *   **Purpose**: Manages the initialization and loading of Large Language Models (LLMs).
    *   **Key Functionality**: Loads `google/gemma-2b-it`, `deepseek-ai/deepseek-coder-1.3b-instruct`, and `microsoft/phi-2` using the Hugging Face `transformers` library. It applies **4-bit quantization (NF4)** via `bitsandbytes` to optimize memory usage on GPUs. It also configures specific chat templates for models like Gemma.

*   **`user_management_module.py`**:
    *   **Purpose**: Handles all user-related operations, ensuring secure authentication and role management.
    *   **Key Functionality**: Implements **RBAC (Role-Based Access Control)** for Admin and User roles. It manages user registration, login verification using **PBKDF2-HMAC-SHA256** password hashing, and secure session handling. It also includes advanced account recovery features like **Email OTP** (via SMTP) and encrypted security questions.

*   **`code_generator_module.py`**:
    *   **Purpose**: The engine behind the code generation feature.
    *   **Key Functionality**: Interfaces with the loaded models to generate code based on user prompts. It constructs model-specific prompts (e.g., using chat templates for Gemma/DeepSeek or instruction formats for Phi-2) and handles the generation parameters (temperature, max tokens).

*   **`code_explainer_module.py`**:
    *   **Purpose**: Powers the "Code Explainer" feature.
    *   **Key Functionality**: Wraps user-provided code in specialized prompt templates to generate explanations. It supports different explanation styles: "Beginner-Friendly", "Technical Deep-Dive", and "Step-by-Step Guide".

*   **`admin_dashboard_module.py`**:
    *   **Purpose**: Aggregates data for the Admin Dashboard.
    *   **Key Functionality**: Reads from JSON log files (`user_history.json`, `feedback_log.json`, `users.json`) to compute analytics. It calculates metrics like total queries, average user rating, and active users. It also provides a **Global Search** function to query across all application data.

*   **`feedback_analysis_module.py`**:
    *   **Purpose**: Analyzes user feedback and manages user profiles.
    *   **Key Functionality**: Uses **VADER Sentiment Analysis** to score user feedback. It also includes utilities for generating **Word Clouds** from feedback comments and creating/managing user avatars (including Gravatar integration).

*   **`jwt_utils.py`**:
    *   **Purpose**: Provides utilities for JSON Web Token (JWT) handling.
    *   **Key Functionality**: Generates and verifies JWTs signed with `HS256` for stateless authentication.

### Frontend Application (`streamlit_app/`)

The user interface is built with Streamlit, providing a responsive and interactive experience.

*   **`app.py`**:
    *   **Purpose**: The main entry point for the frontend application.
    *   **Key Functionality**: Orchestrates the UI flow. It handles:
        *   **Authentication Views**: Login, Sign Up, and Forgot Password forms.
        *   **Navigation**: Sidebar routing between CodeGenie, Code Explainer, Profile, and Admin Dashboard.
        *   **State Management**: Manages user sessions and chat history using `st.session_state`.
        *   **API Integration**: Communicates with the backend FastAPI server to request code generation and explanations.

*   **`style.css`**:
    *   **Purpose**: Custom styling for the application.
    *   **Key Functionality**: Overrides default Streamlit styles to provide a polished, professional look (custom buttons, chat bubbles, metrics).

### Model Server

*   **`backend/model_server.py`**:
    *   **Purpose**: Exposes the AI models via a REST API.
    *   **Key Functionality**: A **FastAPI** application that serves endpoints (`/generate`, `/explain`). It decouples the heavy model inference from the UI thread, allowing for better scalability and separation of concerns.

---

## Key Features

### Multi-Model Intelligence
CodeGenie employs a diverse set of specialized models to ensure optimal performance across various tasks:
- **Google Gemma-2b-it**: A lightweight, high-efficiency model suitable for general-purpose coding inquiries and rapid prototyping.
- **DeepSeek-Coder-1.3b**: A model specifically trained on over 2 trillion tokens of code, providing superior understanding of syntax, logic, and complex programming structures.
- **Microsoft Phi-2**: A reasoning-focused model designed to handle complex logical problems and algorithmic challenges with high accuracy.

### Advanced Code Generation
Users can leverage natural language prompts to generate syntactically correct and functional code snippets in a wide array of programming languages, including Python, C++, JavaScript, and SQL. The system supports context-aware generation to align with specific project requirements.

### Deep Code Explainer
The Code Explainer module provides detailed analyses of existing codebases. Users can select from multiple explanation styles tailored to their proficiency level:
- **Beginner-Friendly**: Simplified concepts and analogies.
- **Technical Deep-Dive**: In-depth analysis of memory management, time complexity, and underlying logic.
- **Step-by-Step Guide**: Sequential breakdown of execution flow.

### Enterprise-Grade User Management
- **Role-Based Access Control (RBAC)**: Strict separation of duties between Administrators and Standard Users to ensure system integrity.
- **Secure Authentication**: Implementation of stateless session management using JSON Web Tokens (JWT).
- **Profile Customization**: Users can personalize their experience with custom avatars, including support for Gravatar integration.
- **Advanced Account Recovery**: Secure password reset functionality utilizing Email OTP (via SMTP) and encrypted security questions.

### Comprehensive Admin Dashboard
Administrators are provided with a powerful suite of analytics and management tools:
- **Usage Metrics**: Real-time tracking of total queries, active user counts, and system engagement.
- **Visual Analytics**: Generation of word clouds to visualize common themes in user feedback.
- **Sentiment Analysis**: Automated evaluation of user feedback using VADER sentiment scoring to gauge user satisfaction.
- **Code Quality Heuristics**: Monitoring of execution success rates and syntax validity to ensure model reliability.
- **Global Search**: Capability to search across all user records, activity history, and feedback logs for auditing and support.
- **User Lifecycle Management**: Full control over user accounts, including the ability to promote users to administrative roles or delete accounts as necessary.

---

## Technical Architecture

### Model Ecosystem
The platform utilizes a hybrid model approach to balance computational efficiency with output quality:
- **Quantization**: To optimize resource utilization, all models are loaded using **4-bit NormalFloat (NF4)** quantization via the `bitsandbytes` library. This technique reduces VRAM consumption by approximately 75% while maintaining inference quality comparable to 16-bit precision.

### Security and Cryptography
Data security is paramount within the CodeGenie architecture:
- **Password Hashing**: User passwords are secured using **PBKDF2-HMAC-SHA256** with 100,000 iterations and a unique, randomly generated salt for each user.
- **Security Answers**: Answers to security questions are hashed using **SHA-256** prior to storage, ensuring that sensitive personal information is never stored in plaintext.
- **Authentication**: The system employs **JSON Web Tokens (JWT)** signed with the `HS256` algorithm for secure, tamper-proof authentication.

### API and Data Flow
The application follows a modern, microservices-oriented architecture:
1.  **User Request**: Interactions originate from the Streamlit frontend interface (default port 8501).
2.  **Frontend Processing**: The frontend serializes requests and transmits them to the FastAPI backend.
3.  **Backend Routing**:
    - `/generate`: Directs prompts to the appropriate LLM based on user selection.
    - `/explain`: Encapsulates code snippets within specialized prompt templates for explanation.
4.  **Inference Engine**: The `transformers` pipeline executes the forward pass on the available GPU hardware.
5.  **Response Delivery**: Generated content is decoded and returned to the user interface for display.

### Operational Procedures
- **User Registration**:
    1.  Validation of input fields (User ID, Username, Password complexity).
    2.  Generation of a cryptographically secure 16-byte random salt.
    3.  Computation of the password hash.
    4.  Atomic persistence of the user record to the `users.json` data store.
- **Admin Promotion**:
    - Existing administrators can promote standard users to the Admin role via the `promote_user_to_admin` function, with a system-enforced limit of two administrators.
- **Feedback Loop**:
    - Users submit ratings (1-5 stars) and qualitative comments.
    - The system computes a compound sentiment score (-1.0 to +1.0) using VADER analysis.
    - All data is logged to `feedback_log.json` for aggregation in the Admin Dashboard.

---

## Prerequisites

- **Python 3.10 or higher**
- **NVIDIA GPU** (Strongly recommended for efficient model inference)
- **Hugging Face Account** (Required for accessing model weights)
- **ngrok Account** (Required for public tunneling capabilities)

---

## Installation and Usage

### Option 1: Local Deployment with Docker (Recommended)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/codegenie.git
    cd codegenie
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the root directory with the following credentials:
    ```env
    HF_TOKEN=your_hugging_face_token
    NGROK_TOKEN=your_ngrok_token
    JWT_SECRET_KEY=your_super_secret_key
    SMTP_EMAIL=your_email@gmail.com
    SMTP_PASSWORD=your_app_password
    ```

3.  **Build and Run the Container:**
    ```bash
    docker build -t codegenie .
    docker run --gpus all -p 8501:8501 -p 8000:8000 --env-file .env codegenie
    ```
    *Note: The `--gpus all` flag requires the NVIDIA Container Toolkit to be installed on the host machine.*

4.  **Access the Application:**
    Launch a web browser and navigate to `http://localhost:8501`.

### Option 2: Google Colab Deployment

1.  Upload the `CodeGenie_Colab_Complete.ipynb` notebook to your Google Colab environment.
2.  Configure the Runtime type to **GPU (T4)**.
3.  Execute all cells in sequence. The application will initialize and display a public ngrok URL for access.

---

## Project Structure

```
codegenie/
├── backend/                 # FastAPI backend and core logic modules
│   ├── model_loader.py      # Model initialization and quantization
│   ├── code_generator.py    # Code generation logic
│   ├── user_management.py   # User auth and RBAC implementation
│   └── ...
├── streamlit_app/           # Streamlit frontend application
│   ├── app.py               # Main application entry point
│   ├── style.css            # Custom CSS for UI styling
│   └── ...
├── Dockerfile               # Docker container definition
├── start.sh                 # Container entry point script
└── requirements.txt         # Python dependency manifest
```

---

## Contributing

Contributions to CodeGenie are welcome. Please fork the repository and submit a Pull Request with your proposed changes.

---

## License

This project is licensed under the MIT License.

---

<div align="center">
  <sub>Built with dedication by the CodeGenie Team</sub>
</div>
