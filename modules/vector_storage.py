from datetime import datetime
from typing import List, Dict, Any
from vectordb import InMemoryExactNNVectorDB
from docarray import BaseDoc, DocList
from docarray.typing import NdArray

from modules.config import VECTOR_FOLDER


class TextDoc(BaseDoc):
    date: datetime = datetime.now()
    text: str
    username: str
    embedding: NdArray


class VectorDBStorage:
    def __init__(self):
        """
        TODO
        """
        self.db = InMemoryExactNNVectorDB[TextDoc](workspace=VECTOR_FOLDER)

    def insert_document(self, username: str, text: str, embedding: List[float],
                        date: datetime = None) -> str:
        """
        Insert a document into the collection. The current datetime is used if no date is provided.

        Args:
        username (str): The username associated with the document.
        text (str): The text content of the document.
        vector (List[float]): The feature vector associated with the document.
        date (datetime, optional): The date associated with the document.

        Returns:
        str: The ID of the inserted document.
        """
        if date is None:
            date = datetime.now()
        text_doc = TextDoc()
        text_doc.text = text
        text_doc.date = date
        text_doc.embedding = embedding
        self.db.index(inputs=DocList[TextDoc](text_doc))
        return

    def search_similar_vectors(self, username: str, query_vector: List[float], limit: int = 5) -> List[
        Dict]:
        """
        Search for documents with vectors similar to the given query vector,
        filtered by the specified username.

        Args:
        username (str): Username to filter documents by.
        query_vector (List[float]): The query vector for similarity search.
        limit (int): Maximum number of similar documents to return.

        Returns:
        List[Dict]: A list of documents with similar vectors, limited to `limit` results.
        """
        query = {
            "vector": query_vector,
            "filter": {"username": username},
            "limit": limit
        }
        return self.collection.search(query)
