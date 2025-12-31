from django.conf import settings
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from lib.prompt import get_default_prompt
from data.llm_settings import get_openai_llm


# get conversation chain
def get_conversation_chain(user):
    llm = get_openai_llm()
    conversation_chain = ConversationChain(
        llm=llm,
        prompt=get_default_prompt(),
        verbose=True,
        memory=ConversationBufferMemory()
    )
    return conversation_chain


# get conversation
def get_conversation(user, query):
    # start conversation chain
    conversation_chain = get_conversation_chain(user)
    ai_message = conversation_chain.predict(input=query)
    print(ai_message)
    return ai_message
