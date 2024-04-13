from datetime import datetime
from docarray import BaseDoc
from docarray.typing import NdArrayEmbedding


class TextDoc(BaseDoc):
    uuid: str
    date: str = datetime.now().strftime('%Y-%m-%d')
    text: str
    username: str
    embedding: NdArrayEmbedding[1536]
