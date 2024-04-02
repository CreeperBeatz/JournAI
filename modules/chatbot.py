import openai
from model.conversation import Conversation
from modules.config import config

system_message = ("You are a friendly AI assistant. You are currently "
                  "having a conversation with a human.")


class ChatBot:

    def __init__(self):
        self.client = openai.OpenAI(api_key=config["openai"]["token"])

    def chat(self, conversation: Conversation) -> str:
        """
        Given a conversation object, predict the next text output.
        The function also calls functions and RAG where needed

        Args:
            conversation (Conversation):

        Returns:

        """
        # TODO define functions

        # TODO add RAG

        last_role = conversation.history[-1]["role"]
        if last_role != "assistant" and last_role != "system":

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation.history
            )
            msg = response.choices[0].message.content
            return msg
        else:
            return "Waiting on human input."
