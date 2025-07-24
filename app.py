import streamlit as st
import datetime
from ai_interface import generate_survey_questions, get_feedback_and_recommendations
from survey_manager import save_survey_version, load_survey_versions
from collaboration import init_collaboration_space
from excel_export import export_to_excel

CATEGORIES = [
    "Customer Product Review",
    "Education Feedback",
    "Employee Feedback",
    "Event Evaluation",
    "Exit Interview",
    "Custom"
]

def login_flow():
    if 'user' not in st.session_state:
        name = st.text_input("Enter your name to login:", key="login_name")
        if st.button("Login") and name.strip():
            st.session_state.user = name.strip()
            st.rerun()
        st.stop()

def setup_survey():
    with st.form("survey_setup_form"):
        category = st.selectbox("Survey Category", CATEGORIES)
        title = st.text_input("Survey Title", value="")
        submitted = st.form_submit_button("Generate Survey")
        if submitted and title.strip():
            with st.spinner("AI is generating your survey questions and use case..."):
                result = generate_survey_questions(category, title)
            st.session_state.survey_setup = {
                "category": category,
                "title": title,
                "use_case_example": result.get("use_case_example", ""),
                "questions": result.get("questions", [])
            }
            st.rerun()

def personal_info_form():
    st.subheader("Personal Information")
    with st.form("personal_info_form"):
        name    = st.text_input("Name")
        address = st.text_input("Address")
        email   = st.text_input("Email")
        phone   = st.text_input("Phone")
        date    = st.date_input("Date", value=datetime.date.today())
        submitted = st.form_submit_button("Proceed to Survey")
        if submitted:
            st.session_state.personal = {
                "Name": name,
                "Address": address,
                "Email": email,
                "Phone": phone,
                "Date": str(date)
            }
            st.rerun()

def main():
    st.set_page_config(page_title="AI Modular Survey Platform", layout="centered")
    st.title("AI Modular Survey Form")

    login_flow()
    st.sidebar.header(f"Hello, {st.session_state.user}!")
    page = st.sidebar.radio("Navigate", [
        "Take Survey", "Review Answers", "AI Feedback", "Collaboration", "History"
    ])

    if page == "Take Survey":
        if 'survey_setup' not in st.session_state:
            setup_survey()
            st.stop()
        if 'personal' not in st.session_state:
            personal_info_form()
            st.stop()

        # Always visible, light background use-case box
        use_case = st.session_state.survey_setup.get("use_case_example") or \
                   (f"This survey is for '{st.session_state.survey_setup.get('title','')}' (category: {st.session_state.survey_setup.get('category','')}).")
        st.markdown(
            f"<div style='background-color:#f8f9fa;padding:1em;border-radius:8px;margin-bottom:1em'>"
            f"<b>Survey Title:</b> {st.session_state.survey_setup['title']} &nbsp;&nbsp; | &nbsp;&nbsp; "
            f"<b>Category:</b> {st.session_state.survey_setup['category']}<br>"
            f"<b>Use Case:</b> {use_case}"
            f"</div>",
            unsafe_allow_html=True
        )
        questions = st.session_state.survey_setup["questions"]
        if len(questions) < 5:
            questions += [f"Additional question {i+1}" for i in range(5-len(questions))]
        with st.form("survey_main"):
            responses = []
            for idx, q in enumerate(questions, 1):
                responses.append(st.text_area(f"Question {idx}: {q}", key=f"q{idx}"))
            done = st.form_submit_button("Submit Survey")
            if done:
                st.session_state.responses = responses
                save_survey_version(
                    st.session_state.user,
                    {
                        "personal": st.session_state.personal,
                        "survey_setup": st.session_state.survey_setup,
                        "responses": responses,
                        "questions": questions,
                    }
                )
                st.success("Survey answers saved! Check 'Review Answers' or 'AI Feedback'.")
                st.rerun()

    elif page == "Review Answers":
        if all(x in st.session_state for x in ("personal", "responses", "survey_setup")):
            st.header("Summary of your responses")
            for k, v in st.session_state.personal.items():
                st.markdown(f"**{k}:** {v}")
            st.markdown("---")
            qs = st.session_state.survey_setup["questions"]
            ans = st.session_state.responses
            ai_results = st.session_state.get("ai_review_results", [])
            for idx, (q, resp) in enumerate(zip(qs, ans), 1):
                st.markdown(f"**Q{idx}: {q}**\n- **Your answer:** {resp if resp else '_No answer provided._'}")
                if ai_results and idx <= len(ai_results):
                    st.info(
                        f"**AI Review:** {ai_results[idx-1]['review_answer']}\n\n"
                        f"**AI Recommended Answer:** {ai_results[idx-1]['recommend_answer']}"
                    )
            if st.button("Get/Refresh AI Review and Export to Excel"):
                with st.spinner("Getting AI review and exporting..."):
                    ai_results = get_feedback_and_recommendations(qs, ans)
                    st.session_state.ai_review_results = ai_results
                    export_to_excel(
                        "user_data.xlsx",
                        {
                            "user_info": st.session_state.personal,
                            "survey_title": st.session_state.survey_setup["title"],
                            "survey_category": st.session_state.survey_setup["category"],
                            "survey_use_case": use_case,
                            "survey_questions": qs,
                            "user_answers": ans,
                            "ai_review_list": ai_results,
                        }
                    )
                st.success("Saved to user_data.xlsx and reloaded AI review.")

    elif page == "AI Feedback":
        if all(x in st.session_state for x in ("responses", "survey_setup")):
            questions = st.session_state.survey_setup["questions"]
            answers = st.session_state.responses
            with st.spinner("AI is evaluating your responses..."):
                ai_results = get_feedback_and_recommendations(questions, answers)
            for idx, (q, ans) in enumerate(zip(questions, answers), 1):
                st.markdown(f"**Q{idx}: {q}**\n- **Your answer:** {ans if ans else '_No answer provided._'}")
                st.info(
                    f"**AI Review:** {ai_results[idx-1]['review_answer']}\n\n"
                    f"**AI Recommended Answer:** {ai_results[idx-1]['recommend_answer']}"
                )

    elif page == "Collaboration":
        init_collaboration_space(st.session_state.user)

    elif page == "History":
        surveys = load_survey_versions(st.session_state.user)
        st.header("Your Survey History")
        for idx, survey in enumerate(surveys, 1):
            with st.expander(f"Survey Version {idx}"):
                st.json(survey)

if __name__ == "__main__":
    main()
