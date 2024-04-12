from datetime import datetime
from typing import List, Dict
from vectordb import InMemoryExactNNVectorDB
from docarray import DocList
from model.textdoc import TextDoc
from modules.config import VECTOR_FOLDER


class VectorDBStorage:
    def __init__(self):
        """
        TODO
        """
        self.db = InMemoryExactNNVectorDB[TextDoc](workspace=VECTOR_FOLDER)

    def insert_document(self, username: str, text: str, embedding: List[float],
                        date: datetime = None):
        """
        Insert a document into the collection. The current datetime is used if no date is provided.

        Args:
        username (str): The username associated with the document.
        text (str): The text content of the document.
        vector (List[float]): The feature vector associated with the document.
        date (datetime, optional): The date associated with the document.

        Returns:
        """
        if date is None:
            date = datetime.now()
        text_doc = TextDoc(
            username=username,
            text=text,
            date=date,
            embedding=embedding
        )
        text_doc.username = username
        text_doc.text = text
        text_doc.date = date
        text_doc.embedding = embedding
        self.db.index(inputs=DocList[TextDoc]([text_doc]))
        return True

    def search_similar(self, username: str, query_text: str, query_embedding: List[float],
                       limit: int = 5) -> List[Dict]:
        """
        Search for documents with vectors similar to the given query vector,
        filtered by the specified username.

        Args:
            username (str): Username to filter documents by.
            query_text (str):
            query_embedding (List[float]): The query vector for similarity search.
            limit (int): Maximum number of similar documents to return.

        Returns:
        List[Dict]: A list of documents with similar vectors, limited to `limit` results.
        """
        query = TextDoc(
            username=username,
            text=query_text,
            embedding=query_embedding
        )
        results = self.db.search(inputs=DocList[TextDoc]([query]), limit=limit)[0].matches

        # Double check for correct username
        return [result for result in results if result.username == username]
