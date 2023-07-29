import openai
import streamlit as st
from datetime import date

import os

st.title("GrumPT Bot - the uncle you never had and never wanted")

openai.api_key = st.secrets["OPENAI_API_KEY"]

bot_options = {
    "Friedrich": st.secrets["Friedrich"],
    "Neo": st.secrets["NEO"],
    "Jason": st.secrets["JASON"],
    "Wisdomosaurus": st.secrets["GRUMPA"]
}

username = st.text_input("Enter your username")
bot_name = st.selectbox("Select Bot", list(bot_options.keys()))

if "selected_bot" not in st.session_state or st.session_state.selected_bot != bot_name:
    st.session_state.clear()
    st.session_state.selected_bot = bot_name

if username:
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-16k-0613"

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append(
            {"role": "system", "content": bot_options[bot_name] + f"\nYou are entering a conversation with:{username}\n\n"})

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    st.warning("Please enter a username to continue.")
