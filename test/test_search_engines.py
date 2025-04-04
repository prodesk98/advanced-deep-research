
def test_google_search():
    from services import GoogleSearch
    google_search = GoogleSearch()
    query = "Python programming"
    limit = 5
    results = google_search.search(query, limit)
    assert isinstance(results, str)
    assert len(results) > 0
    assert "Python" in results
    assert "programming" in results


def test_arxiv_search():
    from services import ArxivSearch
    arxiv_search = ArxivSearch()
    query = "Quantum Computing"
    limit = 5
    results = arxiv_search.search(query, limit)
    assert isinstance(results, str)
    assert len(results) > 0
    assert "Quantum" in results
    assert "Computing" in results


def test_semantic_search():
    from services import SemanticSearch
    semantic_search = SemanticSearch("default")
    query = "Machine Learning"
    document = """Machine Learning is a subset of artificial intelligence that focuses on the development of 
    algorithms that can learn from and make predictions based on data.
    """
    limit = 5
    semantic_search.upsert(document)
    results = semantic_search.search(query, limit)
    assert isinstance(results, str)
    assert len(results) > 0
    assert "Machine" in results
    assert "Learning" in results

