# CodeGenie AI Assistant

![CodeGenie Banner](https://img.shields.io/badge/AI-CodeGenie-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=flat-square&logo=streamlit)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=flat-square&logo=fastapi)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-yellow?style=flat-square&logo=huggingface)

**CodeGenie** is a comprehensive, enterprise-grade AI-powered coding assistant designed to enhance software development workflows. By integrating state-of-the-art Large Language Models (LLMs) such as **Gemma**, **DeepSeek Coder**, and **Phi-2**, CodeGenie offers robust capabilities including automated code generation, detailed technical explanations, and a sophisticated administrative dashboard for analytics and user management.

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
