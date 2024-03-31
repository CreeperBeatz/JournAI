import os
from modules.config import CHATS_FOLDER
import json
import uuid
from datetime import datetime
from typing import Dict, List, Tuple


class Conversation:
    def __init__(self):
        self.conversation_id = self._generate_uuid()
        self.title = "New Conversation"
        self.turns: List[Dict[str, str]] = []
        self.metadata: Dict[str, any] = {}
        self.last_modified: datetime = datetime.now()

    @staticmethod
    def _generate_uuid() -> str:
        """Generates a unique identifier based on the current timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, timestamp)
        return str(unique_id)

    def add_turn(self, role: str, text: str):
        self.turns.append({"role": role, "text": text})
        self.last_modified: datetime = datetime.now()

    def set_metadata(self, **kwargs):
        self.metadata = kwargs

    def to_json(self) -> str:
        return json.dumps({
            "conversation_id": self.conversation_id,
            "title": self.title,
            "turns": self.turns,
            "metadata": self.metadata,
            "last_modified": self.last_modified.strftime('%Y%m%d%H%M%S'),
        }, indent=4)

    @classmethod
    def from_json(cls, data: dict):
        conversation = cls()
        conversation.conversation_id = data['conversation_id']
        conversation.title = data['title']
        conversation.turns = data['turns']
        conversation.metadata = data['metadata']
        conversation.last_modified = datetime.strptime(data['last_modified'], '%Y%m%d%H%M%S')
        return conversation


def save_conversation(username: str, conversation: Conversation):
    user_dir = os.path.join(CHATS_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(
        user_dir,
        f"{conversation.conversation_id}_"
        f"{conversation.title.replace('_', ' ')}"
        f".json"
    )
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


def list_conversations(username: str) -> dict[str, dict[str, str | datetime]]:
    """
    Lists conversation titles, last modified dates, and IDs for a given user based on the file names,
    organizing them into a dictionary.

    The function sorts the conversations in Descending order based on their timestamp.

    Args:
        username (str): Username of the person whose conversations are being listed.
        sort (bool):

    Returns:
        dict: Dictionary where each key is a conversation UUID and the value is another dictionary
              with 'title' and 'last_modified' datetime.
    """
    user_dir = os.path.join(CHATS_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)
    conversations = {}
    for filename in os.listdir(user_dir):
        if filename.endswith(".json"):
            conversation_id = filename.split('_', 1)[0]
            title = filename.split('_', 1)[1].rsplit('.', 1)[0]
            last_modified_time = datetime.fromtimestamp(
                os.path.getmtime(os.path.join(user_dir, filename))
            )

            conversations[conversation_id] = {
                "title": title,
                "last_modified": last_modified_time
            }

    # Sort conversations by 'last_modified' in descending order
    sorted_conversations = dict(sorted(
        conversations.items(),
        key=lambda item: item[1]['last_modified'],
        reverse=True
    ))

    return sorted_conversations

