import streamlit as st
from llm import OpenAILLM
from utils import PDFParser

client = OpenAILLM()

st.title("Resumo de Textos com LLM")

st.write(
    """Esta aplicação utiliza um modelo de linguagem para resumir textos e extrair informações relevantes.
    Você pode colar um texto longo e o modelo irá gerar um resumo ou extrair informações específicas."""
)

# Clear session state on button click
if st.button("Novo chat"):
    st.session_state.summary = None
    st.session_state.flashcards = []
    st.session_state.current_flashcard = 0
    st.session_state.messages = []
#

# Initialize session states
if "summary" not in st.session_state:
    st.session_state.summary = None

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "current_flashcard" not in st.session_state:
    st.session_state.current_flashcard = 0

if "messages" not in st.session_state:
    st.session_state.messages = []
#

# Step 0: Upload PDF
uploaded_file = st.file_uploader("Envie um PDF para extração de texto", type="pdf")

pdf_text = ""
if uploaded_file is not None:
    try:
        pdf_parser = PDFParser(uploaded_file.read())
        pdf_text = pdf_parser.to_text()
        st.success("PDF lido com sucesso!")
    except Exception as e:
        st.error(f"Erro ao ler o PDF: {e}")

# Step 1: User Input or PDF content
prompt = None

if pdf_text:
    st.subheader("Texto extraído do PDF:")
    st.write(pdf_text)
    if st.button("Usar texto do PDF para gerar resumo"):
        prompt = pdf_text

# Optional manual input
manual_prompt = st.chat_input("Ou digite seu texto manualmente para gerar o resumo")

if manual_prompt:
    prompt = manual_prompt

# Step 2: Generate Summary
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        stream = client.generate(st.session_state.messages)
        summary = st.write_stream(stream)
        st.session_state.summary = summary
        st.session_state.messages.append({"role": "assistant", "content": summary})
        st.success("Resumo e análise do texto gerado com sucesso!")

# Step 3: Display Summary and Generate Flashcards
if st.session_state.summary:
    st.subheader("Resumo:")
    st.write(st.session_state.summary)

    if st.button("Criar Flashcards"):
        with st.spinner("Gerando flashcards..."):
            try:
                flashcards = client.flashcard(st.session_state.summary)

                if isinstance(flashcards, list) and len(flashcards) > 0:
                    st.session_state.flashcards = flashcards
                    st.session_state.current_flashcard = 0
                    st.success(f"{len(flashcards)} Flashcards criados com sucesso!")
                else:
                    st.warning("Nenhum flashcard foi gerado.")
            except Exception as e:
                st.error(f"Erro ao gerar flashcards: {e}")

# Step 4: Flashcard Viewer
if st.session_state.flashcards:
    current_index = st.session_state.current_flashcard
    current_card = st.session_state.flashcards[current_index]

    st.subheader(f"Flashcard {current_index + 1} de {len(st.session_state.flashcards)}")

    if st.button("Mostrar Pergunta"):
        st.write(current_card.question)

    if st.button("Mostrar Resposta"):
        st.success(current_card.answer)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voltar", disabled=current_index == 0):
            st.session_state.current_flashcard -= 1
    with col2:
        if st.button("Próximo", disabled=current_index == len(st.session_state.flashcards) - 1):
            st.session_state.current_flashcard += 1