from .mongodb import MongoDB
from .qdrant import Qdrant

db = MongoDB()      # Singleton instance of MongoDB
vecdb = Qdrant()    # Singleton instance of Qdrant

__all__ = [
    "MongoDB",
    "Qdrant",
    "db",           # MongoDB instance
    "vecdb",        # Qdrant instance
]
