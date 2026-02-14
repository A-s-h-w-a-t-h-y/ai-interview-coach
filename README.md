<div align="center">

# 🎯 AI Interview Coach

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

**AI-powered interview preparation tool.** Upload resume + job description to get 8 tailored questions, type your answers, and receive percentage match score with strengths & weaknesses analysis.

</div>

## 🚀 Features

- **Resume + JD Analysis**: AI extracts key skills from your PDF resume and job description to generate 8 role-specific questions.
- **Type Your Answers**: Answer all 8 questions in a clean interface (no voice required).
- **Smart Scoring**: Calculates percentage match between your resume, JD, and typed answers.
- **Detailed Feedback**: Identifies **strengths** (matching skills) and **weaknesses** (gaps to improve).
- **Engineering-Focused**: Perfect for robotics, AI/ML, automation, and software roles.

## 📋 Tech Stack

| **Frontend** | Streamlit |
| **Backend** | Python |
| **AI** | Groq + Llama model |
| **Processing** | PyPDF2 |


## 🎮 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/ai-interview-coach.git
cd ai-interview-coach
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
