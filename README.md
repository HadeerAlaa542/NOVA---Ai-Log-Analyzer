# NOVA - AI Log Analyzer 🚀

Nova is a powerful, AI-driven log analysis tool designed to help DevOps engineers and developers quickly diagnose system issues. Powered by Google's Gemini AI, it parses complex log files, identifies root causes, and suggests remediation steps in seconds.

![Nova UI](https://img.shields.io/badge/Interface-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![AI](https://img.shields.io/badge/AI-Gemini-4285F4?style=for-the-badge&logo=google)

## ✨ Features

*   **🔍 Deep Log Analysis:** Upload raw log files (text, json, log) and get an instant summary of errors, anomalies, and root causes.
*   **🤖 Nova Chat Assistant:** A built-in AI chatbot to answer your DevOps questions and help you debug interactively.
*   **🎨 Cyberpunk UI:** A sleek, dark-themed interface designed for focus and clarity.
*   **💡 Actionable Insights:** Get specific CLI commands and fixes for identified issues.

## 🛠️ Prerequisites

*   **Python 3.8+** installed on your system.
*   A **Google Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/)).

## 📦 Installation

1.  **Clone the repository** (or navigate to the project folder):
    ```bash
    cd c:\Brainsq\ai-log-analyzer
    ```

2.  **Set up the Environment Variables:**
    *   Navigate to the `backend` folder.
    *   Create a `.env` file (if it doesn't exist) and add your API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    GEMINI_MODEL=gemini-2.0-flash-exp  # or gemini-1.5-flash
    ```

3.  **Install Dependencies:**
    You need to install dependencies for both the backend and the frontend.

    ```bash
    # Install Backend Requirements
    pip install -r backend/requirements.txt

    # Install Frontend Requirements
    pip install -r ui/requirements.txt
    ```

## 🚀 How to Run

You need to run the Backend and the Frontend in separate terminals.

### 1. Start the Backend (API)
This handles the AI processing.
```bash
python backend/app.py
```
*The server will start at `http://localhost:8000`*

### 2. Start the Frontend (UI)
This launches the web interface.
```bash
streamlit run ui/streamlit_app.py
```
*The app will open in your browser at `http://localhost:8503`*

<img width="1919" height="929" alt="Screenshot 2025-11-28 202153" src="https://github.com/user-attachments/assets/f7be6b47-1a19-47d2-b23a-58b29e5f335c" />

## 📂 Project Structure

```
ai-log-analyzer/
├── backend/
│   ├── app.py              # FastAPI server & endpoints
│   ├── analyzer.py         # Gemini AI integration logic
│   ├── requirements.txt    # Backend dependencies
│   └── .env                # API Keys (not committed)
├── ui/
│   ├── streamlit_app.py    # Main Streamlit UI application
│   └── requirements.txt    # Frontend dependencies
├── .streamlit/
│   └── config.toml         # UI Theme configuration
├── sample_logs.log         # Sample file for testing
└── README.md               # Project documentation
```

## 🧪 Testing

We have provided sample log file to test the capabilities of Nova:
*   `devops_test_logs.log`: Contains Kubernetes, Nginx, and Jenkins errors.

Upload the file in the UI to see Nova in action!

---
*Powered by Brainsq & Google Gemini*
