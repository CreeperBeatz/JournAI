import os
from modules.config import CHATS_FOLDER
import json
import uuid
from datetime import datetime
from typing import Dict, List, Tuple


class Conversation:
    def __init__(self):
        self.conversation_id = self._generate_uuid()
        self.title = self.conversation_id[:10]
        self.turns: List[Dict[str, str]] = []
        self.metadata: Dict[str, any] = {}

    @staticmethod
    def _generate_uuid() -> str:
        """Generates a unique identifier based on the current timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, timestamp)
        return str(unique_id)

    def add_turn(self, role: str, text: str):
        self.turns.append({"role": role, "text": text})

    def set_metadata(self, **kwargs):
        self.metadata = kwargs

    def to_json(self) -> str:
        return json.dumps({
            "conversation_id": self.conversation_id,
            "name": self.title,
            "turns": self.turns,
            "metadata": self.metadata,
        }, indent=4)

    @classmethod
    def from_json(cls, data: dict):
        conversation = cls()
        conversation.conversation_id = data['conversation_id']
        conversation.title = data['name']
        conversation.turns = data['turns']
        conversation.metadata = data['metadata']
        return conversation


def save_conversation(username: str, conversation: Conversation):
    user_dir = os.path.join(CHATS_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, f"{conversation.conversation_id}_{conversation.title}.json")
    with open(file_path, 'w') as file:
        file.write(conversation.to_json())


def load_conversation(username: str, conversation_id: str) -> Conversation:
    user_dir = os.path.join(CHATS_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)
    target_file = None
    for filename in os.listdir(user_dir):
        if filename.startswith(f"{conversation_id}_"):
            target_file = filename
            break

    if not target_file:
        raise ValueError("Conversation doesn't exist!")

    file_path = os.path.join(user_dir, target_file)
    with open(file_path, 'r') as file:
        data = json.load(file)

    return Conversation.from_json(data)


def list_conversations(username: str) -> dict:
    """
    Lists conversation titles and IDs for a given user based only on the file names, organizing them into a dictionary.

    Returns:
        dict: Dictionary where the key is the Conversation ID and the value is the Title.
    """
    user_dir = os.path.join(CHATS_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)
    conversations = {}
    for filename in os.listdir(user_dir):
        if filename.endswith(".json"):
            conversation_id, title = (
                filename.rsplit('_', 1)[0],
                filename.rsplit('_', 1)[1].rsplit('.', 1)[0]
            )
            conversations[conversation_id] = title
    return conversations

