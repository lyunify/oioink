import os, bs4
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, OnlinePDFLoader, UnstructuredPDFLoader
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, JSONLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import S3DirectoryLoader
from langchain_community.document_loaders import S3FileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from lib.utils import get_tmp_directory, directory_exists, is_directory_empty


# -------------------------------------------------------------------------------------------------
# data preparation - for vector stores and retrievers

# get raw_docs (check pdf or text file) from directory using Langchain loader
def get_file_docs(user):
    directory = get_tmp_directory(user)
    # Iterate over files in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        # Check if the current item is a file
        if os.path.isfile(file_path):
            # Open and read the file
            with open(file_path, 'r') as file:
                file_extension = os.path.splitext(file_path)[1]
                # Check the file type based on the extension
                if file_extension == '.pdf':
                    loader = PyPDFLoader(file_path)
                    raw_docs = loader.load()
                elif file_extension == '.txt':
                    loader = TextLoader(file_path)
                    raw_docs = loader.load()
                elif file_extension == '.csv':
                    loader = CSVLoader(file_path)
                    raw_docs = loader.load()
                elif file_extension == '.html':
                    loader = UnstructuredHTMLLoader(file_path)
                    raw_docs = loader.load()
                elif file_extension == '.md':
                    loader = UnstructuredMarkdownLoader(file_path)
                    raw_docs = loader.load()
                elif file_extension == '.json':
                    loader = JSONLoader(file_path)
                    raw_docs = loader.load()
                else:
                    # raw_docs = '[Document(page_content="aiplus")]'
                    raw_docs = False
                    print(f'Unknown file type: {file_path}')
        else:
            # use a string to trick FAISS to return a space vector
            # if there is no files
            # raw_docs = '[Document(page_content="aiplus")]'
            raw_docs = False
            print(f'Directory: {directory} is empty')
    return raw_docs


# get raw_docs (check csv file) from directory using Langchain loader
def get_csv_docs(user, args):
    directory = get_tmp_directory(user)
    # Iterate over files in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        # Check if the current item is a file
        if os.path.isfile(file_path):
            # Open and read the file
            with open(file_path, 'r') as file:
                file_extension = os.path.splitext(file_path)[1]
                # Check the file type based on the extension
                if file_extension == '.csv':
                    print(args)
                    columns = args.split(',')
                    csv_columns = {
                        'delimiter': ',',
                        # 'quotechar': '"',
                        'fieldnames': columns
                    }
                    print(csv_columns)
                    print(csv_columns['fieldnames'])
                    loader = CSVLoader(file_path=file_path, csv_args=csv_columns)
                    raw_docs = loader.load()
                else:
                    # raw_docs = '[Document(page_content="aiplus")]'
                    raw_docs = False
                    print(f'Unknown file type: {file_path}')
        else:
            # use a string to trick FAISS to return a space vector
            # if there is no files
            # raw_docs = '[Document(page_content="aiplus")]'
            raw_docs = False
            print(f'Directory: {directory} is empty')
    return raw_docs


# get raw_docs from web content using Langchain loader
def get_web_base_docs(url):
    if url:
        loader = WebBaseLoader(url)
        # bs_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
        # loader = WebBaseLoader(
        #     web_paths=([url]),
        #     bs_kwargs={"parse_only": bs_strainer},
        # )
        loader.requests_kwargs = {'verify':False}
        raw_docs = loader.load()
        return raw_docs
    else:
        return False


# get raw_docs from online PDF using Langchain loader
def get_online_pdf_docs(url):
    if url:
        # loader = UnstructuredPDFLoader(url)
        loader = OnlinePDFLoader(url)
        raw_docs = loader.load()
        return raw_docs
    else:
        return False


# get raw_docs (check pdf or text file) from directory using Langchain loader
def get_directory_docs(user):
    directory = get_tmp_directory(user)
    if directory_exists(directory) and not is_directory_empty(directory):
        loader = DirectoryLoader(directory)
        raw_docs = loader.load()
        return raw_docs
    else:
        return False


# get docs from raw_docs
def get_docs(raw_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    docs = text_splitter.split_documents(raw_docs)
    return docs
