import streamlit as st
import openai

# Get the current query parameters as a dict
params = st.experimental_get_query_params()
if 'params' not in st.session_state:
    st.session_state.params = params

# Get the value of the "example" parameter, or use a default value if not set
chatbot_id = st.session_state.params.get("chatbot", ["0"])[0]

#Get the chatbot ids and msgs from the secrets file
prompt_engineer_id = st.secrets["prompt_engineer_id"]
prompt_engineer_msg = st.secrets["prompt_engineer_msg"]

psychic_id = st.secrets["psychic_id"]
psychic_msg = st.secrets["psychic_msg"]


if chatbot_id == prompt_engineer_id:
    name = "Prompt Engineer"
    sys_msg = prompt_engineer_msg
elif chatbot_id == psychic_id:
    name = "Psychic"
    sys_msg = psychic_msg
else:
    name = "None"

if name == "None": 
    break
else: 
    st.title(f"{name}")
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "system", "content": sys_msg})
    for message in st.session_state.messages:
            if message["role"] != "system": # check if the role is not system
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    if prompt := st.chat_input("Start Talking"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
        
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
