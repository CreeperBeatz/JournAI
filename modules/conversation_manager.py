import glob
import json
import os
from datetime import datetime

from model.conversation import Conversation
from modules.config import CHATS_FOLDER
from modules.utilities import sanitize_filename


def save_conversation(username: str, conversation: Conversation):
    # Crude way to check if there are any messages in the conversation
    if len(conversation.history) < 2:
        # 1 message means only system message, or no AI response
        return

    user_dir = os.path.join(CHATS_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)

    # Delete any previous conversation files
    file_pattern = os.path.join(user_dir, f"{conversation.id}_*.json")
    for file in glob.glob(file_pattern):
        os.remove(file)

    # Sanitize conversation title
    title = sanitize_filename(conversation.title)

    file_path = os.path.join(
        user_dir,
        f"{conversation.id}_"
        f"{title}"
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

    The function sorts the conversations in Descending order based on their creation timestamp.

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
            creation_time = datetime.fromtimestamp(
                os.path.getctime(os.path.join(user_dir, filename))
            )

            conversations[conversation_id] = {
                "title": title,
                "creation_time": creation_time
            }

    # Sort conversations by 'last_modified' in descending order
    sorted_conversations = dict(sorted(
        conversations.items(),
        key=lambda item: item[1]['creation_time'],
        reverse=True
    ))

    return sorted_conversations
