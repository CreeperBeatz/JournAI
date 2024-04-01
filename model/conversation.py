import json
import uuid
from datetime import datetime
from typing import Dict, List
from langchain.memory import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class Conversation:

    system = "system"
    assistant = "assistant"
    user = "user"

    def __init__(self):
        self.conversation_id = self._generate_uuid()
        self.title = "New Conversation"
        self.history: ChatMessageHistory = ChatMessageHistory()
        self.metadata: Dict[str, any] = {}
        self.last_modified: datetime = datetime.now()
        self.creation_date: datetime = datetime.now()

    @staticmethod
    def _generate_uuid() -> str:
        """Generates a unique identifier based on the current timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, timestamp)
        return str(unique_id)

    def add_user_turn(self, content: str):
        self.history.add_user_message(content)
        self.last_modified: datetime = datetime.now()

    def add_ai_turn(self, content: str):
        self.history.add_ai_message(content)
        self.last_modified: datetime = datetime.now()

    def set_metadata(self, **kwargs):
        self.metadata = kwargs

    def to_json(self) -> str:
        return json.dumps({
            "conversation_id": self.conversation_id,
            "title": self.title,
            "history": self.history_to_jsonable(),
            "metadata": self.metadata,
            "last_modified": self.last_modified.strftime('%Y%m%d%H%M%S'),
            "creation_date": self.creation_date.strftime('%Y%m%d%H%M%S'),
        }, indent=4)

    def history_as_str(self, user="user", assistant="assistant", system="system") -> str:
        """
        Args:
            user: The label for user messages.
            assistant: The label for assistant messages.
            system: The label for system messages.

        Returns:
            A single string containing the formatted history.
        """
        # Mapping message types to their corresponding labels.
        prefix_map = {
            SystemMessage: system,
            HumanMessage: user,
            AIMessage: assistant
        }

        # Building the history string using list comprehension and join.
        history_text = "".join(
            f"{prefix_map[type(message)]}: {message.content}" for message in self.history.messages)

        return history_text

    def history_to_jsonable(self) -> List[Dict[str, str]]:
        """
        Converts the history of messages into a format that can be easily serialized into JSON.

        Returns:
            A list of dictionaries, each representing a message with the sender and the message content.
        """
        # Define the mapping of message types to sender roles.
        type_to_role = {
            SystemMessage: "system",
            HumanMessage: "user",
            AIMessage: "assistant"
        }

        # Convert each message in the history to a dictionary.
        history_list = [
            {"role": type_to_role[type(message)], "content": message.content}
            for message in self.history.messages
        ]

        return history_list

    @classmethod
    def history_from_jsonable(cls, data: list[Dict]):
        history = ChatMessageHistory()

        for message in data:
            if message["role"] == "system":
                history.add_system_message(message["content"])
            if message["role"] == "assistant":
                history.add_ai_message(message["content"])
            if message["role"] == "user":
                history.add_user_message(message["content"])

        return history



    @classmethod
    def from_json(cls, data: dict):
        conversation = cls()
        conversation.conversation_id = data['conversation_id']
        conversation.title = data['title']
        conversation.history = cls.history_from_jsonable(data['history'])
        conversation.metadata = data['metadata']
        conversation.last_modified = datetime.strptime(data['last_modified'], '%Y%m%d%H%M%S')
        conversation.creation_date = datetime.strptime(data['creation_date'], '%Y%m%d%H%M%S')
        return conversation


