from datetime import datetime
from docarray.index import HnswDocumentIndex
from model.textdoc import TextDoc
from modules.config import VECTOR_FOLDER
import os
import sqlite3
from typing import (
    List,
    Tuple,
)


class VectorDBStorage:
    def __init__(self):
        """
        Initialize a local Hnsw Document storage, that writes TextDocs in an SQLite database and their
        embeddings in a bin file
        """
        # Monkey patch the constructor, to ensure compatibility with streamlit
        HnswDocumentIndex.__init__ = new_init
        self.db = HnswDocumentIndex[TextDoc](work_dir=VECTOR_FOLDER)

    def insert_document(self, username: str, text: str, embedding: List[float],
                        date: datetime | str | None = None, uuid: str = None):
        """
        Insert a document into the collection. The current datetime is used if no date is provided.

        Args:
        username (str): The username associated with the document.
        text (str): The text content of the document.
        vector (List[float]): The feature vector associated with the document.
        date (datetime | str, optional): The timestamp associated with the document.
        uuid (str, optional): If an id(UUID) is provided, a check is made if a document with that UUID
            doesn't already exist. If it does, the newly passed document overrides the current one.


        Returns:

        Notes:
            This UUID is different from the `doc_id` and `id` present on all BaseDoc items, as there is
            no reliable way to set them, as of docarray version 0.40.0
        """
        # Delete any previous records with the same ID
        doc = self.search_by_uuid(uuid)
        if doc:
            self.db.__delitem__(doc.id)

        # Validate date parameter
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        if type(date) is datetime:
            date = date.strftime('%Y-%m-%d')
        if type(date) is not str:
            raise ValueError("date parameter is not datetime, str or None!")

        # Insert new record
        text_doc = TextDoc(
            username=username,
            text=text,
            date=date,
            embedding=embedding,
            uuid=uuid
        )
        return self.db.index(text_doc)

    def search_similar(self, username: str, query_embedding: List[float], omit_uuid: str = None,
                       limit: int = 5) -> Tuple[List[TextDoc], List[float]]:
        """
        Search for documents with vectors similar to the given query vector,
        filtered by the specified username.

        Args:
            username (str): Username to filter documents by.
            query_embedding (List[float]): The query vector for similarity search.
            omit_uuid (str, optional): Document uuid to exclude from the search. Usually used for current
                conversation. CURRENTLY NOT FUNCTIONAL!
            limit (int): Maximum number of similar documents to return.

        Returns:
            Tuple[List[TextDoc], List[float]]: Tuple containing a list of documents with similar
                vectors as a first value, limited to `limit` results, and a list of similarity scores
                for all the documents, where closer to 0 means better similarity
        """
        query = (
            self.db.build_query()
            .filter(filter_query={'username': {'$eq': username}})
            .find(query=query_embedding, search_field='embedding', limit=limit)
            .build()
        )

        return self.db.execute_query(query)

    def search_by_uuid(self, uuid: str) -> TextDoc | None:
        """
        Search a document based on its UUID. Returns None if no doc with that ID.
        """
        try:
            results = self.db.filter({'uuid': {'$eq': uuid}})
            return results[0] if results else None
        except RuntimeError:
            return None


# Save the original __init__ method
original_init = HnswDocumentIndex.__init__


def new_init(self, db_config=None, **kwargs):
    # Call the original __init__ method
    original_init(self, db_config, **kwargs)

    # Close the original SQLite connection created in the original __init__
    if hasattr(self, '_sqlite_conn'):
        self._sqlite_conn.close()

    # Create a new SQLite connection with check_same_thread set to False
    self._sqlite_db_path = os.path.join(self._work_dir, 'docs_sqlite.db')
    self._sqlite_conn = sqlite3.connect(self._sqlite_db_path, check_same_thread=False)
    self._sqlite_cursor = self._sqlite_conn.cursor()
    # Log the new connection setup
    self._logger.debug('Modified connection to DB with check_same_thread=False')
