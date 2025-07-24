import streamlit as st

def init_collaboration_space(user):
    st.header("Team Collaboration")
    msg = st.text_input("Send a message:")
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []
    if st.button("Send") and msg.strip():
        st.session_state.chat_log.append({"user": user, "message": msg})
    for chat in st.session_state.chat_log:
        st.markdown(f"**{chat['user']}**: {chat['message']}")
