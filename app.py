import streamlit as st
import os
import io
import PyPDF2

from dotenv import load_dotenv
from groq import Groq

# ===== ENV & CLIENT SETUP =====
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.3-70b-versatile"  # Groq Llama 3.x general model [web:344]

# ===== STREAMLIT PAGE CONFIG =====
st.set_page_config(page_title="AI Interviewer Bot", layout="wide")
st.title("🤖 AI Interviewer Bot - Mock Interviews (Text)")

# Sidebar
st.sidebar.header("Instructions")
st.sidebar.info(
    """
1. Upload resume (PDF) and paste job description  
2. Click "Generate 8 Interview Questions"  
3. Answer each question in the text box and click "Next"  
4. After 8 questions, a detailed performance report is generated
"""
)

# ===== RESUME & JD INPUT =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume (PDF)")
    resume_file = st.file_uploader("Choose PDF", type="pdf", key="resume")
    resume_text = ""

    if resume_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_file.read()))
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""
        st.success(f"✅ Resume parsed: {len(resume_text)} characters")

with col2:
    st.subheader("📋 Job Description")
    job_desc = st.text_area("Paste job description here", height=200, key="jd")


def reset_session():
    """Reset for new interview."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# ===== GENERATE QUESTIONS =====
if st.button("🎯 Generate 8 Interview Questions", type="primary") and resume_text and job_desc:
    with st.spinner("Generating role-specific questions..."):
        prompt = f"""
        RESUME:
        {resume_text[:3000]}

        JOB DESCRIPTION:
        {job_desc[:3000]}

        Generate EXACTLY 8 interview questions (mix of technical + behavioral)
        that test this candidate's fit for the role.
        Questions should get progressively harder.
        Number them 1-8. Return ONLY the numbered list.
        """

        try:
            chat_completion = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical interviewer.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            response_text = chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"Groq model error while generating questions: {e}")
            st.stop()

        questions = [q.strip() for q in response_text.strip().split("\n") if q.strip()]
        questions = questions[:8]

        st.session_state.questions = questions
        st.session_state.question_idx = 0
        st.session_state.answers = []
        st.session_state.resume_text = resume_text
        st.session_state.job_desc = job_desc


# ===== INTERVIEW LOOP (TEXT ANSWERS) =====
if "questions" in st.session_state and st.session_state.question_idx < 8:
    idx = st.session_state.question_idx
    st.header(f"❓ Question {idx + 1}/8")
    st.markdown(f"**{st.session_state.questions[idx]}**")

    answer = st.text_area("✏️ Type your answer here", height=180, key=f"answer_{idx}")

    if st.button("✅ Submit & Next", type="secondary"):
        if not answer.strip():
            st.warning("Please enter an answer before continuing.")
        else:
            st.session_state.answers.append(answer.strip())
            st.session_state.question_idx += 1
            st.rerun()


# ===== FINAL REPORT =====
elif "questions" in st.session_state and st.session_state.question_idx >= 8:
    st.header("📊 Interview Performance Report")

    with st.spinner("Analyzing performance..."):
        full_transcript = "\n".join(
            [
                f"Q{idx+1}: {st.session_state.questions[idx]}\nA{idx+1}: {ans}\n"
                for idx, ans in enumerate(st.session_state.answers)
            ]
        )

        report_prompt = f"""
        RESUME: {st.session_state.resume_text[:2000]}
        JD: {st.session_state.job_desc[:2000]}
        INTERVIEW TRANSCRIPT:
        {full_transcript}

        Create detailed interview feedback:
        1. OVERALL SCORE (0-100%)
        2. STRENGTHS (3 bullets)
        3. AREAS FOR IMPROVEMENT (3 bullets)
        4. HIRING RECOMMENDATION (Yes/No/Maybe + reason)
        5. ACTIONABLE TIPS (4 specific suggestions)

        Use markdown format with clear headers.
        """

        try:
            chat_completion = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strict but fair interview evaluator.",
                    },
                    {"role": "user", "content": report_prompt},
                ],
                temperature=0.4,
            )
            report_text = chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"Groq model error while generating report: {e}")
            st.stop()

        st.markdown(report_text)

    st.button("🔄 New Interview", type="primary", on_click=reset_session)


# ===== FOOTER =====
if __name__ == "__main__":
    st.markdown("---")
    st.caption("Built with Streamlit + Groq Llama 3 | Text-based mock interviews")
