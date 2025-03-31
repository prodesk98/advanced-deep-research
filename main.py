import streamlit as st
from llm import OpenAILLM

client = OpenAILLM()

"""
Otimize a análise de textos resumindo e extraindo as informações mais relevantes com o auxílio de um chat LLM.
"""

st.title("Resumo de Textos com LLM")

st.write(
    "Esta aplicação utiliza um modelo de linguagem para resumir textos e extrair informações relevantes. "
    "Você pode colar um texto longo e o modelo irá gerar um resumo ou extrair informações específicas."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.generate(prompt)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


