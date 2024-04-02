import json
import os
from typing import List
from modules.config import QUESTIONS_FOLDER

save_questions_description = {
    "name": "save_questions",
    "description": "Set daily journal questions for the user. The questions can be for a Gratitude journal"
                   " (What are you grateful for?), self-improvement (what charged you with energy, what "
                   "drained you of energy, what would you like to do more, what would you like to do less)"
                   ", or anything else the user wants as a goal.",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "array of strings, representing the questions the user wants to set as their "
                               "daily questions."
            }
        },
        "required": [
            "questions"
        ]
    }
}


def save_questions(username: str, questions: List[str]):
    """
    Set daily journal questions for the user.

    Args:
        username (str): Identifier of current user.
        questions (List[str]): List of questions to be saved.

    Returns:
        None
    """
    # Ensure the directory for storing questions exists
    os.makedirs(QUESTIONS_FOLDER, exist_ok=True)
    file_path = os.path.join(QUESTIONS_FOLDER, f"{username}.json")

    # Open the file in write mode and save the questions as JSON
    with open(file_path, 'w') as file:
        json.dump(questions, file)


def load_questions(username: str) -> List[str]:
    """
    Load daily journal questions for the user.

    Args:
        username (str): Identifier of current user.

    Returns:
        List[str]: List of questions loaded from the file.
    """
    file_path = os.path.join(QUESTIONS_FOLDER, f"{username}.json")

    # Check if the file exists before trying to open it
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        # Return an empty list if the file doesn't exist
        return []
