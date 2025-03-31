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

if prompt := st.chat_input(""):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.generate(prompt)
        response = st.write_stream(stream)


