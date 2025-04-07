

def test_brave_search():
    from researchers import BraveSearch
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
    semantic_search = SemanticSearch("default")
    document1 = """Machine Learning is a subset of artificial intelligence that focuses on the development of 
    algorithms that can learn from and make predictions based on data.
    """
    document2 = """Deep Learning is a subset of machine learning that uses neural networks with many layers
    (deep architectures) to learn from large amounts of data.
    """
    document_id = "test_document"
    semantic_search.upsert(document1, document_id)
    semantic_search.upsert(document2, document_id)


def test_semantic_search_query():
    from researchers import SemanticSearch
    semantic_search = SemanticSearch("default")
    query = "Artificial Intelligence"
    limit = 5
    result = semantic_search.query(query, limit)
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_semantic_search_search():
    from researchers import SemanticSearch
    semantic_search = SemanticSearch("default")
    query = "Machine Learning"
    limit = 5
    result = semantic_search.search(query, limit)
    assert len(result) > 0, "Expected result to have length greater than 0"


def test_semantic_delete():
    from researchers import SemanticSearch
    semantic_search = SemanticSearch("default")
    document_id = "test_document"
    semantic_search.delete_by_document_id(document_id)
