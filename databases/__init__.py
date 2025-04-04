from typing import Optional

from .mongodb import MongoDB
from .qdrant import Qdrant


_db: Optional[MongoDB] = None


class Instance:
    """
    Base class for singleton instances.
    """
    init: bool = False
    def __init__(self):
        if not self.init:
            Qdrant().initialize()   # Initialize Qdrant
            MongoDB().initialize()  # Initialize MongoDB
            self.init = True
        else:
            raise Exception("Instance already initialized.")

Instance() # Initialize the singleton instance

def get_db() -> MongoDB:
    """
    Returns the singleton instance of MongoDB.
    """
    global _db
    if _db is None:
        _db = MongoDB()
    return _db


def set_db(db_instance: MongoDB):
    """
    Sets the singleton instance of MongoDB.
    :param db_instance:
    :return:
    """
    global _db
    _db = db_instance


__all__ = [
    "MongoDB",
    "Qdrant",
    "get_db",
    "set_db",
]
