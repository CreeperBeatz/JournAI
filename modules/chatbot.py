from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from model.conversation import Conversation
from modules.config import config

prompt_template = """You are a friendly AI assistant. You are
currently having a conversation with a human.

chat_history: {chat_history},
assistant:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=prompt_template
)

llm = ChatOpenAI(openai_api_key=config["openai"]["token"])


class ChatBot:

    def __init__(self):
        self.memory = ConversationBufferWindowMemory()

        # Configure LLMChain with temporary memory
        self.llm_chain = LLMChain(
            llm=llm,
            memory=self.memory,
            prompt=prompt
        )

    def predict(self, conversation: Conversation):
        # Check if the last message is from the user
        if conversation.history.messages and type(conversation.history.messages[-1]) is HumanMessage:
            # Generate AI response using LLMChain
            response = self.llm_chain.run(conversation.history_as_str())
            # Optionally, add AI response to the conversation
            return response
        else:
            return "Waiting for user input."
