import streamlit as st
import asyncio
from core.llama_response import analyze_chunk

st.set_page_config(page_title="Fraud Detection LLM", page_icon="🛡️")
st.title("🛡️ Real-Time Fraud Detection")

user_input = st.text_input("Enter message chunk:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "follow_up" not in st.session_state:
    st.session_state.follow_up = False
if "show_conversation" not in st.session_state:
    st.session_state.show_conversation = False
if "cumulative_risk_score" not in st.session_state:
    st.session_state.cumulative_risk_score = 0.0

def update_cumulative_risk(risk_score):
    st.session_state.cumulative_risk_score += risk_score
    if st.session_state.cumulative_risk_score > 1.0:
        st.session_state.cumulative_risk_score = 1.0

if st.button("Analyze") and user_input:
    async def fetch_analysis():
        result = await analyze_chunk(user_input, st.session_state.chat_history)
        update_cumulative_risk(result['risk_score'])
        st.session_state.chat_history.append(f"👤 User: {user_input}")
        st.session_state.chat_history.append(f"🤖 LLM Response: {result['notification_en']}")
        st.session_state.last_result = result
        st.session_state.follow_up = False
        if st.session_state.cumulative_risk_score >= 0.7:
            st.error(f"🚨 Warning! High risk of fraud detected! (Score: {st.session_state.cumulative_risk_score:.2f})")
        else:
            st.success(f"✅ Current Cumulative Risk Score: {st.session_state.cumulative_risk_score:.2f}")
        st.info(f"Latest Classification: {result['classification']}")
        st.warning(f"Notification (EN): {result['notification_en']}")
        st.warning(f"Notification (AR): {result['notification_ar']}")
    asyncio.run(fetch_analysis())

if st.session_state.last_result:
    if st.button("Start Follow-up Chat"):
        st.session_state.follow_up = True

if st.session_state.follow_up:
    st.subheader("💬 Follow-up Chat")
    follow_up_input = st.text_input("Write your follow-up question:")
    if st.button("Send Follow-up"):
        async def fetch_followup_response():
            result = await analyze_chunk(follow_up_input, st.session_state.chat_history)
            update_cumulative_risk(result['risk_score'])
            st.session_state.chat_history.append(f"👤 User: {follow_up_input}")
            st.session_state.chat_history.append(f"🤖 LLM Response: {result['notification_en']}")
            if st.session_state.cumulative_risk_score >= 0.7:
                st.error(f"🚨 Warning! High risk of fraud detected! (Score: {st.session_state.cumulative_risk_score:.2f})")
            else:
                st.success(f"✅ Current Cumulative Risk Score: {st.session_state.cumulative_risk_score:.2f}")
            st.info(f"Response Classification: {result['classification']}")
            st.warning(f"Notification (EN): {result['notification_en']}")
            st.warning(f"Notification (AR): {result['notification_ar']}")
        asyncio.run(fetch_followup_response())

if st.button("Show Full Conversation"):
    st.session_state.show_conversation = not st.session_state.show_conversation

if st.session_state.show_conversation:
    st.subheader("📜 Conversation History")
    for msg in st.session_state.chat_history:
        st.write(msg)
