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


def test_sub_queries():
    from llm.openai_llm import OpenAILLM

    openai_llm = OpenAILLM()

    query = "Explain the concept of reinforcement learning."
    result = openai_llm.generate_sub_queries(query)
    assert isinstance(result, list), "Sub-queries result should be a list"
    assert len(result) > 0, "Sub-queries result should not be empty"
    assert all(isinstance(q, str) for q in result), "All sub-queries should be strings"


def test_reflection():
    from llm.openai_llm import OpenAILLM

    openai_llm = OpenAILLM()

    query = "Explain the concept of reinforcement learning."
    sub_queries = [
        "What is reinforcement learning?",
        "How does reinforcement learning work?",
        "What are the applications of reinforcement learning?"
    ]
    chunks = [
        "Reinforcement learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize cumulative reward.",
        "In reinforcement learning, an agent interacts with an environment and learns from the consequences of its actions.",
        "Reinforcement learning has applications in robotics, game playing, and autonomous vehicles."
    ]
    result = openai_llm.reflection(query, sub_queries, chunks)
    assert isinstance(result, list), "Reflection result should be a list"
    assert len(result) > 0, "Reflection result should not be empty"
    assert all(isinstance(r, str) for r in result), "All reflection results should be strings"


def test_summarize():
    from llm.openai_llm import OpenAILLM

    openai_llm = OpenAILLM()

    query = "Summarize the key features of reinforcement learning."
    chunks = [
        "Reinforcement learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize cumulative reward.",
        "In reinforcement learning, an agent interacts with an environment and learns from the consequences of its actions.",
        "Reinforcement learning has applications in robotics, game playing, and autonomous vehicles."
    ]
    result = openai_llm.summarize(query, chunks)
    assert isinstance(result, str), "Summary result should be a string"
    assert len(result) > 0, "Summary result should not be empty"