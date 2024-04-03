import openai
from openai.types.chat import ChatCompletionMessage

from model.conversation import Conversation
from modules.config import config


class ChatBot:

    def __init__(self, function_descriptions):
        self.client = openai.OpenAI(api_key=config["openai"]["token"])

        self.system_message = ("You are a friendly AI assistant. You are currently "
                               "having a conversation with a human.")

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
            model="gpt-3.5-turbo",
            messages=conversation.history,
            functions=self.function_descriptions
        )
        msg = response.choices[0].message
        return msg

    def get_summary(self, conversation: Conversation) -> str:
        # TODO
        pass

    def get_title(self, conversation: Conversation) -> str:
        # TODO
        pass
