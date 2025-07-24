AI Modular Survey Platform
Create, manage, answer, review, and export dynamic AI-powered surveys with Groq or other LLMs.

Key features:

Passwordless login (name-based)

User-driven survey creation (category & title)

AI-generated use-case context and at least 5 target questions per survey

User answers collection with review and AI feedback/recommendations for each answer

Export all data (including AI review and suggestions) to user_data.xlsx

Built-in collaboration chat and run history

🚀 Features
Login: One-step, privacy-friendly login via user name—no password.

Survey Creation:

Select survey category and title.

AI generates at least 5 open-ended, relevant questions and a human-readable use-case description, shown visibly above the questions.

Personal Info:

Collects name, address, email, mobile number, and date.

Flexible Answering:

Responsive UI for detailed user inputs.

AI Feedback & Review:

Per-question feedback and recommended answers integrated, powered by Groq (or any compatible LLM).

Export:

All user data, survey info, answers, and AI analysis saved to user_data.xlsx for local/archive/reporting/audit use.

History:

View previous submissions and full record for audit or export.

Collaboration:

Team chat space for multi-user workflows.

📦 Folder Structure
text
/
├ app.py
├ ai_interface.py
├ survey_manager.py
├ excel_export.py
├ collaboration.py
├ requirements.txt
├ .env
├ user_data/           # Per-user versioned JSON survey history
├ user_data.xlsx       # Excel export (auto-generated)
⚙️ Requirements
Python 3.8+

Groq API access (or your LLM provider)

Install dependencies once:

bash
pip install -r requirements.txt
🔑 Setup: Environment
Place a .env file in the project root with:

text
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3-70b-tool-use
GROQ_API_URL=https://your-real-groq-endpoint/v1/chat/completions
(Adjust values for your LLM deployment)

▶️ How to Run
Launch the app:

bash
streamlit run app.py
Log in with your name, create a survey (pick category & title), answer the questions, and review results.

View AI feedback, recommendations, and collaborate or query previous history.

All data and feedback is saved to user_data.xlsx (Excel) for easy analysis or reporting.

📝 Excel Export Details
Each row in user_data.xlsx includes:

User name, address, email, mobile, date

Survey title, category, use case context

5+ survey questions and user answers

AI review per answer

AI recommended answer per question

Compatible with all spreadsheet tools for analytics or compliance use.

💡 Customizing
Add/edit survey categories in app.py.

Change answer/feedback logic in ai_interface.py.

Adjust Excel columns as needed in excel_export.py.

Bring your own model by adjusting .env and API logic.

🛠️ Troubleshooting
Blank use-case or questions: The app injects default text if AI output is incomplete.

Excel not saving: Close user_data.xlsx in Excel when exporting.

Module not found: Run pip install -r requirements.txt again.

App rerun fail: Code uses st.rerun() for Streamlit 1.27+.

🏛️ Credits
Streamlit

Groq Llama-3

openpyxl

python-dotenv

