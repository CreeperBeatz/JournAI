import logging
from datetime import datetime
from typing import List
import openai
from openai.types.chat import ChatCompletionMessage
from modules.question_manager import save_questions_description, get_questions_description
from modules.answer_manager import get_answers_description, save_answer_description
from model.conversation import Conversation
from modules.config import config, CHAT_MODEL, EMBEDDING_MODEL

function_descriptions = [
    save_questions_description,
    get_questions_description,
    get_answers_description,
    save_answer_description
]


class ChatBot:

    def __init__(self, name_of_user: str = None):
        self.client = openai.OpenAI(api_key=config["openai"]["token"])

        self.system_message = (f"You are a friendly AI assistant specializing in psychological help and "
                               f"improvement. You are currently "
                               f"having a conversation with a human called {name_of_user}. "
                               f"The current date is {datetime.now().strftime('%Y-%m-%d')} (YYYY-MM-DD)")
        self.function_descriptions = function_descriptions

    def chat(self, conversation: Conversation) -> ChatCompletionMessage:
        """
        Given a conversation object, predict the next text output.
        The function also calls functions and RAG where needed

        Args:
            conversation (Conversation):

        Returns:
            ChatCompletionMessage
        """

        # TODO add RAG

        last_role = conversation.history[-1]["role"]
        if last_role == "assistant" and last_role == "system":
            raise ValueError("Last message from assistant or system, can't complete query!")

        response = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=conversation.history,
            functions=self.function_descriptions,

        )
        msg = response.choices[0].message
        return msg

    def get_summary(self, conversation, max_tokens: int = 150) -> str:
        # Prepare the conversation history as a single string
        conversation_text = "\n".join(
            [f"{message['role']}: {message['content']}" for message in conversation.history])

        # Call the OpenAI API to generate a summary
        response = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user",
                       "content": f"Provide a summary for this conversation:\n\n{conversation_text}"}],
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    def get_title(self, conversation, max_tokens: int = 10):
        # Prepare the conversation history as a single string
        conversation_text = str(conversation.history)

        # Call the OpenAI API to generate a summary
        response = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user",
                       "content": f"Provide a title for this conversation."
                                  f"Please omit any brackets or escape characters, that aren't suitable"
                                  f"for a filename:\n\n{conversation_text}"}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def get_embedding(self, text):
        if not text or type(text) is not str:
            return None

        try:
            embedding = self.client.embeddings.create(
                input=text,
                model=EMBEDDING_MODEL
            ).data[0].embedding
            return embedding
        except Exception as e:
            logging.error(f"Error while embedding: {e}")
            return None

