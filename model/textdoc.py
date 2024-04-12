from datetime import datetime
from docarray import BaseDoc
from docarray.typing import NdArray


class TextDoc(BaseDoc):
    date: datetime = datetime.now()
    text: str
    username: str
    embedding: NdArray
