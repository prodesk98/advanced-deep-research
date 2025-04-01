from .mongodb import MongoDB
from .qdrant import Qdrant

db = MongoDB()      # Singleton instance of MongoDB

__all__ = [
    "MongoDB",
    "Qdrant",
    "db",           # MongoDB instance
]
