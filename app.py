import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="LPU Timetable Assistant",
    page_icon="📅",
    layout="centered"
)

MANUAL = """
1. Introduction
The LPU Timetable Assistant is an AI-powered chatbot designed to help students
of Lovely Professional University access and understand their academic
timetables. It provides information about class schedules, lecture timings,
classrooms, subjects, faculty details and academic days.

2. Objectives
- Help students understand their daily timetable.
- Provide information about class timings.
- Help students identify free periods.
- Provide subject-wise schedule information.
- Reduce confusion regarding timetable arrangements.
- Make timetable information easier to access.

3. Target Audience
- LPU undergraduate students.
- LPU postgraduate students.
- Faculty members.
- Newly admitted students.

4. Main Features
Q1. How can I check my LPU timetable?
Answer: Students can check their timetable through the official LPU UMS portal.

Q2. Can I check my weekly timetable?
Answer: Yes. The chatbot can display your weekly timetable if the latest
timetable data has been uploaded.

Q3. How can I find my classroom?
Answer: Check the classroom or venue mentioned against your subject in
the timetable.

Q4. Can I find my free periods?
Answer: Yes. The chatbot can identify free periods between scheduled lectures.

Q5. Does the timetable change?
Answer: Yes. Timetables may be updated due to academic requirements. Always
verify the latest schedule through official university channels.

Weekly LPU Timetable
Time                         Monday-Friday
11:10 AM - 12:00 PM          MGN253
12:00 PM - 12:50 PM          ACC103
12:50 PM - 1:40 PM           Free Period
1:40 PM - 2:30 PM            Free Period
2:30 PM - 3:20 PM            MGN206
3:20 PM - 4:10 PM            MGN388
4:10 PM - 5:00 PM            MGN386
"""

SYSTEM_INSTRUCTION = """
You are the LPU Timetable Assistant.
Answer only using the knowledge manual supplied with the question.
If the answer is not available in the manual, say exactly:
"Information is not available."
Give simple and clear answers. Do not invent classrooms, faculty names,
dates, or timetable updates.
"""

st.title("📅 LPU Timetable Assistant")
st.caption("Ask questions about your Monday–Friday class schedule.")

with st.sidebar:
    st.header("About")
    st.write(
        "This chatbot answers questions using the timetable and knowledge "
        "manual provided by its creator."
    )
    st.info(
        "For the latest official timetable and classroom changes, verify "
        "details through the LPU UMS portal."
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

def get_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask your question (type 'exit' to close the chat)...")

if question:
    if question.strip().lower() == "exit":
        st.session_state.messages.append(
            {"role": "assistant", "content": "Chatbot closed. Refresh the page or send a new message to start again."}
        )
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    api_key = get_api_key()
    if not api_key:
        answer = (
            "Gemini API key not found. Add GEMINI_API_KEY to your "
            "Streamlit secrets or environment variables, then restart the app."
        )
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.chat_message("assistant"):
                with st.spinner("Finding the answer..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"{MANUAL}\n\nQuestion: {question}",
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION
                        )
                    )
                    answer = response.text or "Information is not available."
                    st.markdown(answer)
        except Exception as exc:
            answer = f"Sorry, I couldn't get a response from Gemini. Error: {exc}"

    if not api_key or "Sorry, I couldn't" in answer:
        with st.chat_message("assistant"):
            st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
