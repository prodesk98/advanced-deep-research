from langchain_core.messages import HumanMessage


def test_rerank():
    from llm.reranker import Reranker

    reranker = Reranker()

    query = "Machine Learning"
    documents = [
        "Machine Learning is a subset of artificial intelligence that focuses on the development of algorithms that can learn from and make predictions based on data.",
        "Artificial Intelligence is the simulation of human intelligence processes by machines, especially computer systems.",
        "Deep Learning is a class of machine learning based on artificial neural networks.",
        "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan."
    ]
    reranked_results = reranker.rerank(query, documents)
    assert isinstance(reranked_results, list), "Reranked results should be a list"
    assert len(reranked_results) > 0, "Reranked results should not be empty"
    assert reranked_results[0].score >= reranked_results[1].score, "First result should have a higher score than the second result"


def test_embeddings():
    from llm.embeddings import Embeddings

    embeddings = Embeddings()

    query = "What is the capital of France?"
    result = embeddings.embed([query])
    assert isinstance(result, list), "Embeddings result should be a list"
    assert len(result) > 0, "Embeddings result should not be empty"
    assert isinstance(result[0], list), "First element of embeddings result should be a list"
    assert len(result[0]) > 0, "First element of embeddings result should not be empty"


def test_generative():
    from llm.openai_llm import OpenAILLM

    openai_llm = OpenAILLM()

    history = [
        HumanMessage("What is the capital of France?")
    ]
    result = openai_llm.generate(history)
    assert isinstance(result, str), "Generated result should be a string"
    assert len(result) > 0, "Generated result should not be empty"
    assert "Paris" in result, "Generated result should contain the answer to the question"


def test_flashcard():
    from llm.openai_llm import OpenAILLM

    openai_llm = OpenAILLM()

    prompt = """
        Picture this. Your artificial intelligence model
        is ready to go live, but without a proper deployment strategy, it's at
        risk of crashing during peak demand, or worse, leaking sensitive data. 
        How do you prevent these pitfalls? Let's break down the key features
        of a robust deployment plan. By the end of this video, you'll be
        able to describe the critical components of an effective deployment strategy,
        ensuring your models perform consistently and reliably in any environment.
    """
    quantities = 3
    result = openai_llm.flashcard(prompt, quantities)
    assert isinstance(result, list), "Flashcard result should be a list"
    assert len(result) == quantities, f"Flashcard result should contain {quantities} items"
