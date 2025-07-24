import os
import requests
from dotenv import load_dotenv
import json
import re

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
GROQ_API_URL = os.getenv("GROQ_API_URL")

def generate_survey_questions(category, survey_title):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = (
        f"You are a professional survey writer. For survey category: '{category}' and title: '{survey_title}', "
        "generate at least 5 open-ended, use-case-specific questions in a JSON like: "
        "{\"use_case_example\":\"...\",\"questions\":[\"Q1...\",\"Q2...\",...]}"
    )
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 700
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    try:
        match = re.search(r"({.*})", content, re.DOTALL)
        out = json.loads(match.group(1)) if match else json.loads(content)
        # Ensure 5 questions minimum
        questions = out.get("questions", [])
        while len(questions) < 5:
            questions.append(f"Additional question {len(questions)+1}")
        out["questions"] = questions
        # Fill missing use case sensibly
        if not out.get("use_case_example") or not out["use_case_example"].strip():
            out["use_case_example"] = (
                f"This survey is for '{survey_title}' (category: {category}). Please answer all questions thoughtfully."
            )
        return out
    except Exception:
        return {
            "use_case_example": f"This survey is for '{survey_title}' (category: {category}). Please answer all questions thoughtfully.",
            "questions": [f"Q{i+1}" for i in range(5)]
        }

def get_feedback_and_recommendations(questions, answers):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    combined = "\n\n".join([f"Q: {q}\nA: {a if a else '(No answer)'}" for q, a in zip(questions, answers)])
    prompt = (
        "For each Q&A below, reply with BOTH of the following as JSON with two keys: "
        "review_answer: detailed review (Does answer match Q? Is it clear/detailed? Suggestions to improve). "
        "recommend_answer: If the answer is not ideal, what would be the best model answer? "
        "Return as: [{\"review_answer\":\"...\",\"recommend_answer\":\"...\"}, ...]\n"
        f"{combined}\n"
    )
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1200
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    try:
        match = re.search(r"(\[.*\])", content, re.DOTALL)
        return json.loads(match.group(1)) if match else json.loads(content)
    except Exception:
        # fallback data prevents UI break
        return [{"review_answer": "N/A", "recommend_answer": "N/A"} for _ in questions]
