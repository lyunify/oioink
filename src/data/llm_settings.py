import os
from django.conf import settings
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

from accounts.models import Account
from .models import LLMSettings


# -------------------------------------------------------------------------------------------------

def get_openai_llm():
    llm_api_key = settings.OPENAI_API_KEY
    llm_model = settings.OPENAI_MODEL_NAME
    llm_temperature = settings.OPENAI_TEMPERATURE
    llm = ChatOpenAI(openai_api_key=llm_api_key, model_name=llm_model, temperature=llm_temperature, streaming=True)
    return llm


def get_llm(user):
    author = Account.objects.get(email=user.email)
    try:
        obj = LLMSettings.objects.get(author=author)
        if obj.llm == settings.OPENAI:
            llm_api_key = settings.OPENAI_API_KEY
            llm_model = obj.llm_model
            llm_temperature = obj.llm_temperature
            llm = ChatOpenAI(openai_api_key=llm_api_key, model_name=llm_model, temperature=llm_temperature, streaming=True)
        else:
            # default
            llm_api_key = settings.OPENAI_API_KEY
            llm_model = obj.llm_model
            llm_temperature = obj.llm_temperature
            llm = ChatOpenAI(openai_api_key=llm_api_key, model_name=llm_model, temperature=llm_temperature, streaming=True)
    except LLMSettings.DoesNotExist:
        # default setting
        llm = get_openai_llm()
    return llm


def get_embeddings(user):
    author = Account.objects.get(email=user.email)
    try:
        obj = LLMSettings.objects.get(author=author)
        if obj.llm == settings.OPENAI:
            llm_api_key = settings.OPENAI_API_KEY
            embeddings = OpenAIEmbeddings(openai_api_key=llm_api_key)
        else:
            # default
            llm_api_key = settings.OPENAI_API_KEY
            embeddings = OpenAIEmbeddings(openai_api_key=llm_api_key)
    except LLMSettings.DoesNotExist:
        # default setting
        llm_api_key = settings.OPENAI_API_KEY
        embeddings = OpenAIEmbeddings(openai_api_key=llm_api_key)
    return embeddings


def get_vector_db(user):
    author = Account.objects.get(email=user.email)
    try:
        obj = LLMSettings.objects.get(author=author)
        vector_db = obj.vector_db
    except LLMSettings.DoesNotExist:
        # default setting
        vector_db = settings.VECTOR_DB
    return vector_db


def set_default_llm_settings(user):
    author = Account.objects.get(email=user.email)
    try:
        instance = LLMSettings.objects.get(author=author)
        return False
    except LLMSettings.DoesNotExist:
        # default setting
        llm = settings.OPENAI
        llm_api_key = settings.OPENAI_API_KEY
        llm_model = settings.OPENAI_MODEL_NAME
        llm_temperature = 0.0
        vector_db = settings.VECTOR_DB
        search_engine = settings.SEARCH_ENGINE
        instance = LLMSettings(author=author, llm=llm, llm_model=llm_model, llm_api_key=llm_api_key, llm_temperature=llm_temperature, vector_db=vector_db, search_engine=search_engine)
        instance.save()
        return True


# Search ==========================================================================================

def get_search_engine_org(user):
    author = Account.objects.get(email=user.email)
    try:
        obj = LLMSettings.objects.get(author=author)
        if obj.search_engine == 'duckduckgo':
            # search using ddg
            search = DuckDuckGoSearchRun()
        elif obj.search_engine == 'tavily':
            # search using tavily
            os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
            search = TavilySearchResults(max_results=1)
        else:
            # default search using ddg
            search = DuckDuckGoSearchRun()
    except LLMSettings.DoesNotExist:
        # default setting
        search = DuckDuckGoSearchRun()
    return search


def get_search_tool_org(user):
    author = Account.objects.get(email=user.email)
    try:
        obj = LLMSettings.objects.get(author=author)
        if obj.search_engine == 'duckduckgo':
            # search using ddg
            search = DuckDuckGoSearchRun()
            search_tool = Tool(
                name="ddg_search",
                description="Search DDG for recent results.",
                func=search.run,
            )
        elif obj.search_engine == 'google':
            # search using google
            os.environ["GOOGLE_CSE_ID"] = '005df163c16d04ad1'
            os.environ["GOOGLE_API_KEY"] = 'AIzaSyAfdUr1Eb0hOgmKwYxXnhm02yAK4qCa5I0'
            search = GoogleSearchAPIWrapper()
            search_tool = Tool(
                name="google_search",
                description="Search Google for recent results.",
                func=search.run,
            )
        elif obj.search_engine == 'tavily':
            # search using tavily
            os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
            search = TavilySearchResults(max_results=1)
            search_tool = Tool(
                name="tavily_search",
                description="Search Tavily for recent results.",
                func=search.run,
            )
        else:
            # search using ddg
            search = DuckDuckGoSearchRun()
            search_tool = Tool(
                name="ddg_search",
                description="Search DDG for recent results.",
                func=search.run,
            )
    except LLMSettings.DoesNotExist:
        # search using ddg
        search = DuckDuckGoSearchRun()
        search_tool = Tool(
            name="ddg_search",
            description="Search DDG for recent results.",
            func=search.run,
        )
    return search_tool
