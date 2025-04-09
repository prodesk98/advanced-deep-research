

def test_tavily_search():
    from researchers import TavilySearch
    tavily_search = TavilySearch()
    query = "Artificial Intelligence"
    limit = 5
    result = tavily_search.search(query, limit)
    assert isinstance(result, list), "Expected result to be a list"
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_brave_search():
    from researchers import BraveSearch # noqa
    brave_search = BraveSearch()
    query = "Artificial Intelligence"
    limit = 5
    result = brave_search.search(query, limit)
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_search_engine():
    from researchers import SearchEngine
    search_engine = SearchEngine()
    query = "Reinforcement Learning"
    limit = 5
    result = search_engine.search(query, limit)
    assert isinstance(result, str), "Expected result to be a string"
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_youtube_search():
    from researchers import YoutubeSearch
    youtube_search = YoutubeSearch()
    query = "Reinforcement Learning"
    limit = 5
    result = youtube_search.search(query, limit)
    assert isinstance(result, list), "Expected result to be a list"
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_arxiv_search():
    from researchers import ArxivSearch
    arxiv_search = ArxivSearch()
    query = "Quantum Computing"
    limit = 5
    result = arxiv_search.search(query, limit)
    assert isinstance(result, str), "Expected result to be a string"
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_semantic_search_upsert():
    from researchers import SemanticSearch
    semantic_search = SemanticSearch("deep-searcher")
    document1 = """Reinforcement learning (RL) is an interdisciplinary area of machine learning and optimal control concerned with how an intelligent agent should take actions in a dynamic environment in order to maximize a reward signal. 
Reinforcement learning is one of the three basic machine learning paradigms, alongside supervised learning and unsupervised learning.

Reinforcement learning differs from supervised learning in not needing labelled input-output pairs to be presented, and in not needing sub-optimal actions to be explicitly corrected. 
Instead, the focus is on finding a balance between exploration (of uncharted territory) and exploitation (of current knowledge) with the goal of maximizing the cumulative reward (the feedback of which might be incomplete or delayed).
The search for this balance is known as the exploration–exploitation dilemma.

The environment is typically stated in the form of a Markov decision process (MDP), as many reinforcement learning algorithms use dynamic programming techniques.
The main difference between classical dynamic programming methods and reinforcement learning algorithms is that the latter do not assume knowledge of an exact mathematical model of the Markov decision process, and they target large MDPs where exact methods become infeasible."""
    document2 = """Due to its generality, reinforcement learning is studied in many disciplines, such as game theory, control theory, operations research, information theory, simulation-based optimization, multi-agent systems, swarm intelligence, and statistics.
In the operations research and control literature, RL is called approximate dynamic programming, or neuro-dynamic programming.
The problems of interest in RL have also been studied in the theory of optimal control, which is concerned mostly with the existence and characterization of optimal solutions, and algorithms for their exact computation, and less with learning or approximation (particularly in the absence of a mathematical model of the environment)."""
    document_id = "test_document"
    semantic_search.upsert(document1, document_id)
    semantic_search.upsert(document2, document_id)


def test_semantic_search_query():
    from researchers import SemanticSearch
    semantic_search = SemanticSearch("deep-searcher")
    query = "Artificial Intelligence"
    limit = 5
    result = semantic_search.query(query, limit)
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_semantic_search_search():
    from researchers import SemanticSearch
    semantic_search = SemanticSearch("deep-searcher")
    query = "Machine Learning"
    limit = 5
    result = semantic_search.search(query, limit)
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_semantic_delete():
    from researchers import SemanticSearch
    semantic_search = SemanticSearch("deep-searcher")
    document_id = "test_document"
    semantic_search.delete_by_document_id(document_id)
