import openai
import streamlit as st
from datetime import date


import os
st.title("GrumPT Bot - the uncle you never had and never wanted")

openai.api_key = st.secrets["OPENAI_API_KEY"]
grumpa = st.secrets["GRUMPA"]

username = st.text_input("Enter your username")

if username:
    st.session_state['log_file'] = f"./logs/{str(username)}_{date.today().strftime('%Y_%m_%d')}.txt"
    if not os.path.exists(st.session_state['log_file']):
        with open(st.session_state['log_file'], 'w') as file:
            file.write("")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-16k-0613"

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append(
            {"role": "system", "content": grumpa + f"\nYou are entering a conversation with:{username}\n\n"})

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            with open(st.session_state['log_file'], 'a') as file:
                file.write(f"{username}: {prompt}")
                file.write("\n\n")
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
            with open(st.session_state['log_file'], 'a') as file:
                file.write(f"Wisdomosaurus: {full_response}")
                file.write("\n\n")
            print(full_response)

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    st.warning("Please enter a username to continue.")
