class InstanceManager:
    from .embeddings import Embeddings
    from .reranker import Reranker
    from .summarization import Summarization

    _instances = None

    @classmethod
    def get_instances(cls):
        if cls._instances is None:
            cls._instances = {
                "embeddings": cls.Embeddings(),
                "reranker": cls.Reranker(),
                "summarization": cls.Summarization(),
            }
        return cls._instances

def get_reranker():
    """
    Get the reranker instance.
    :return: "Reranker"
    :raises RerankError: If reranker initialization fails.
    """
    return InstanceManager.get_instances()["reranker"]

def get_embeddings():
    """
    Get the embeddings instance.
    :return: "Embeddings"
    :raises EmbedError: If embeddings initialization fails.
    """
    return InstanceManager.get_instances()["embeddings"]


def get_summarization():
    """
    Get the summarization instance.
    :return: "Summarization"
    :raises SummarizationError: If summarization initialization fails.
    """
    return InstanceManager.get_instances()["summarization"]


__all__ = ["get_reranker", "get_embeddings", "get_summarization"]
