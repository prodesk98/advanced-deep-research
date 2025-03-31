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

# Initialize session states
if "summary" not in st.session_state:
    st.session_state.summary = None

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "current_flashcard" not in st.session_state:
    st.session_state.current_flashcard = 0

# Step 1: Generate the summary
if prompt := st.chat_input("Enter your text for summarization or information extraction"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.generate(prompt)
        summary = st.write_stream(stream)
        st.session_state.summary = summary
        st.success("Summary generated successfully!")

# Step 2: Display the summary and button to create flashcards
if st.session_state.summary:
    st.subheader("Summary:")
    st.write(st.session_state.summary)

    if st.button("Create Flashcards"):
        with st.spinner("Generating flashcards..."):
            try:
                # Calls client.flashcard with the summary
                flashcards = client.flashcard(st.session_state.summary)  # returns a list

                if isinstance(flashcards, list) and len(flashcards) > 0:
                    st.session_state.flashcards = flashcards
                    st.session_state.current_flashcard = 0
                    st.success(f"{len(flashcards)} Flashcards created successfully!")
                else:
                    st.warning("No flashcards were generated.")
            except Exception as e:
                st.error(f"Error while generating flashcards: {e}")

# Step 3: Flashcard Viewer
if st.session_state.flashcards:
    current_index = st.session_state.current_flashcard
    current_card = st.session_state.flashcards[current_index]

    st.subheader(f"Flashcard {current_index + 1} of {len(st.session_state.flashcards)}")

    if st.button("Show Question"):
        st.write(f"**Question:** {current_card.question}")

    if st.button("Show Answer"):
        st.success(current_card.answer)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous", disabled=current_index == 0):
            st.session_state.current_flashcard -= 1
    with col2:
        if st.button("Next", disabled=current_index == len(st.session_state.flashcards) - 1):
            st.session_state.current_flashcard += 1