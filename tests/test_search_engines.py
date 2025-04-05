from time import sleep


def test_google_search():
    from services import GoogleSearch
    google_search = GoogleSearch()
    query = "Python programming"
    limit = 5
    result = google_search.search(query, limit)
    assert isinstance(result, str), "Expected result to be a string"
    assert len(result) > 0, "Expected result to have length greater than 0"
    assert "Python" in result, "Expected result to contain 'Python'"
    assert "programming" in result, "Expected result to contain 'programming'"


def test_arxiv_search():
    from services import ArxivSearch
    arxiv_search = ArxivSearch()
    query = "Quantum Computing"
    limit = 5
    result = arxiv_search.search(query, limit)
    assert isinstance(result, str), "Expected result to be a string"
    assert len(result) > 0, "Expected result to have length greater than 0"
    assert "Quantum" in result, "Expected result to contain 'Quantum'"
    assert "Computing" in result, "Expected result to contain 'Computing'"


def test_semantic_search():
    from services import SemanticSearch
    semantic_search = SemanticSearch("default")
    query = "Machine Learning"
    document = """Machine Learning is a subset of artificial intelligence that focuses on the development of 
    algorithms that can learn from and make predictions based on data.
    """
    limit = 5
    document_id = "test_document"
    semantic_search.upsert(document, document_id)
    sleep(15)  # Wait for the document to be indexed
    results = semantic_search.search(query, limit)
    semantic_search.delete_by_document_id(document_id)
    assert isinstance(results, list), "Expected results to be a list"
    assert len(results) > 0, "Expected results to have length greater than 0"
    assert "Machine Learning" in results[0].text, "Expected results to contain 'Machine Learning'"

