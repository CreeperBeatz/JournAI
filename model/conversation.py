import json
import uuid
from datetime import datetime
from typing import List, Dict


class Conversation:
    def __init__(self):
        self.conversation_id = self._generate_uuid()
        self.title = "New Conversation"
        self.history: List[Dict[str, str]] = []
        self.metadata: Dict[str, any] = {}
        self.last_modified: datetime = datetime.now()

    @staticmethod
    def _generate_uuid() -> str:
        """Generates a unique identifier based on the current timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, timestamp)
        return str(unique_id)

    def add_turn(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self.last_modified: datetime = datetime.now()

    def set_metadata(self, **kwargs):
        self.metadata = kwargs

    def to_json(self) -> str:
        return json.dumps({
            "conversation_id": self.conversation_id,
            "title": self.title,
            "history": self.history,
            "metadata": self.metadata,
            "last_modified": self.last_modified.strftime('%Y%m%d%H%M%S'),
        }, indent=4)

    @classmethod
    def from_json(cls, data: dict):
        conversation = cls()
        conversation.conversation_id = data['conversation_id']
        conversation.title = data['title']
        conversation.history = data['history']
        conversation.metadata = data['metadata']
        conversation.last_modified = datetime.strptime(data['last_modified'], '%Y%m%d%H%M%S')
        return conversation
