import json
import os
from datetime import datetime
from typing import Dict, List

save_answer_description = {
    "name": "save_answer",
    "description": "Save daily answer to a question",
    "parameters": {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "The raw answer that the user provided to the given daily question"
            },
            "question": {
                "type": "string",
                "description": "The daily question that was answered. If the given string isn't one from"
                               " get_daily_questions(), the function will fail"
            }
        },
        "required": [
            "answer",
            "question"
        ]
    }
}


def save_answer(username: str, question: str, answer: str):
    """
    Given a question and an answer, write the response to a file corresponding to the current date.
    If the question was already answered for the day, the function will write over it.

    Args:
        username (str): identifier of the current user
        question (str): Question the user is answering to
        answer (str): User provided answer to the question

    Returns:
        None
    """
    # Define the directory and file name for today's date
    dir_path = f"./answers/{username}"
    os.makedirs(dir_path, exist_ok=True)  # Ensure the directory exists
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(dir_path, f"{today_date}.json")

    # Attempt to read the existing answers from today's file
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            daily_answers = json.load(file)
    else:
        daily_answers = {}

    # Update the answer for the given question
    daily_answers[question] = answer

    # Write the updated answers back to the file
    with open(file_path, "w") as file:
        json.dump(daily_answers, file, indent=4)


get_answers_description = {
    "name": "get_answers",
    "description": "Load and return the answers saved for a specific user between two dates.",
    "parameters": {
        "type": "object",
        "properties": {
            "from_date": {
                "type": "string",
                "description": "The start date in 'YYYY-MM-DD' format to begin loading answers from, inclusive."
            },
            "to_date": {
                "type": "string",
                "description": "The end date in 'YYYY-MM-DD' format to stop loading answers at, inclusive."
            }
        },
        "required": [
            "username",
            "from_date",
            "to_date"
        ]
    },
    "returns": {
        "description": "A dictionary with dates as keys and dictionaries of question-answer pairs as values.",
        "type": "Dict[str, Dict[str, str]]"
    }
}


def get_answers(username: str, from_date: str, to_date: str) -> Dict[str, Dict[str, str]]:
    """
    Load and return the answers saved for a specific user between two dates.

    Args:
        username (str): Identifier of the current user.
        from_date (str): The start date in "YYYY-MM-DD" format to begin loading answers from.
        to_date (str): The end date in "YYYY-MM-DD" format to stop loading answers at.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary with dates as keys and dictionaries of question-answer pairs as values.

    Raises:
        ValueError: Dates are not in the correct format
    """
    answers = {}
    dir_path = f"./answers/{username}"

    # Convert strings to datetime objects for comparison
    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")

    # Check if the user's directory exists
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            # Extract date from filename
            file_date_str = filename.split(".")[0]
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")

            # Check if the file's date falls within the given range
            if start_date <= file_date <= end_date:
                file_path = os.path.join(dir_path, filename)
                with open(file_path, "r") as file:
                    answers[file_date_str] = json.load(file)

    return answers


def daily_questions_answered(username: str) -> List[str]:
    """
    Check if the user has answered the daily questions for today.

    Args:
        username (str): Identifier of the current user.

    Returns:
        List[str]: A list of all the questions the user has answered for the day
    """
    # Define the directory and file name for today's date
    dir_path = f"./answers/{username}"
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(dir_path, f"{today_date}.json")

    # Check if today's answer file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            daily_answers = json.load(file)
        return list(daily_answers.keys())
    else:
        return []
