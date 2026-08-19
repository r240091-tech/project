import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

import streamlit as st
from agent import client, tools

SYSTEM_INSTRUCTION = (
    "You are Compa, a helpful AI agent assistant built for the Pleximus AI "
    "Hackathon. Introduce yourself as Compa when asked your name. You can "
    "do calculations, check the weather, manage a to-do list, and work "
    "with text (word count, reverse text). Be concise and friendly."
)

st.set_page_config(page_title="Compa", page_icon="🤖", layout="centered")

st.title("🤖 Compa — Your AI Agent")
st.caption("Ask me to calculate, check weather, manage tasks, or work with text.")

with st.sidebar:
    st.header("What Compa can do")
    st.markdown(
        """
        - 🧮 **Calculator** — add, subtract, multiply, divide
        - 🌦️ **Weather** — ask about any city
        - 📝 **Text Utility** — count words, reverse text
        - ✅ **To-Do List** — add, list, complete tasks

        ---
        Try asking:
        - "What is 25 multiplied by 4?"
        - "What's the weather in Ratnagiri?"
        - "Reverse the text hello world"
        - "Add buy milk to my todo list"
        """
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask Compa anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Compa is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                    config={
                        "tools": tools,
                        "system_instruction": SYSTEM_INSTRUCTION,
                    },
                )
                reply = response.text
            except Exception as e:
                reply = f"Error: {e}"

        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})