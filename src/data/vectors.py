import os, openai, langchain, chromadb, sqlite3
from datetime import datetime
from django.conf import settings
from langchain_community.vectorstores import Chroma, FAISS

from accounts.models import Account
from .models import VectorDBArchive, ActiveVectorDB
from lib.utils import get_tmp_directory, is_directory_empty, empty_directory, directory_exists, copy_directory, get_file_list_string
from .llm_settings import get_embeddings, get_vector_db
from .loaders import get_docs, get_web_base_docs, get_online_pdf_docs


# -------------------------------------------------------------------------------------------------
# Database - Vector Stores and Retrievers

# get user directory
def get_user_directory(user):
    path = f'{settings.VECTOR_DB_LOCATION}/{str(user.id)}'
    return path


# get vector db directory
def get_vector_directory(user):
    directory = f'{settings.VECTOR_DB_LOCATION}/{str(user.id)}'
    if os.path.exists(directory):
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
        return path
    else:
        return False


# create vector db directory
def create_vector_directory(user, directory):
    path = f'{settings.VECTOR_DB_LOCATION}/{str(user.id)}/{directory}'
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory '{path}' created successfully.")
        except OSError as error:
            print(f"Error creating directory '{path}': {error}")
    else:
        print(f"Directory '{path}' already exists.")
    return path


def create_vector(user, raw_docs):
    if raw_docs == False:
        db = False
        return db
    user_path = get_user_directory(user)
    if not is_directory_empty(user_path):
        # close all connections to vector db
        remove_vector(user)
    vector_db = get_vector_db(user)
    if vector_db == 'chroma':
        db = create_vector_chroma(user, vector_db, raw_docs)
    elif vector_db == 'faiss':
        db = create_vector_faiss(user, vector_db, raw_docs)
    else:
        # default to chroma
        vector_db == 'chroma'
        db = create_vector_chroma(user, vector_db, raw_docs)
    return db


def create_vector_web_base(user, url):
    vector_db = get_vector_db(user)
    if vector_db == 'chroma':
        db = create_vector_chroma_web_base(user, vector_db, url)
    elif vector_db == 'faiss':
        db = create_vector_faiss_web_base(user, vector_db, url)
    else:
        # default to chroma
        db = create_vector_chroma_web_base(user, vector_db, url)
    return db


def create_vector_online_pdf(user, url):
    vector_db = get_vector_db(user)
    if vector_db == 'chroma':
        db = create_vector_chroma_online_pdf(user, vector_db, url)
    elif vector_db == 'faiss':
        db = create_vector_faiss_online_pdf(user, vector_db, url)
    else:
        # default to chroma
        db = create_vector_chroma_online_pdf(user, vector_db, url)
    return db


def retrieve_vector(user):
    vector_db = get_vector_db(user)
    if vector_db == 'chroma':
        db = retrieve_vector_chroma(user)
    elif vector_db == 'faiss':
        db = retrieve_vector_faiss(user)
    else:
        # default to chroma
        db = retrieve_vector_chroma(user)
    return db


def remove_vector(user):
    vector_db = get_vector_db(user)
    if vector_db == 'chroma':
        db = remove_vector_chroma(user)
    elif vector_db == 'faiss':
        db = remove_vector_faiss(user)
    else:
        # default to chroma
        db = remove_vector_chroma(user)
    return db


# Chroma ----------------------------------------
# db using chroma

# create chroma vector from user files
def create_vector_chroma(user, vector_db, raw_docs):
    db_path = create_vector_directory(user, 'chroma_db')
    docs = get_docs(raw_docs)
    db = store_vector_chroma(user, docs, db_path)
    # archive db after creating vector
    archive_vector_db(user, vector_db)
    # clean up tmp directory after creating vector
    tmp_directory = get_tmp_directory(user)
    empty_directory(tmp_directory)
    return db


# special case for web base - for Vector Stores and Retrievers
def create_vector_chroma_web_base(user, vector_db, url):
    raw_docs = get_web_base_docs(url)
    db = create_vector_chroma(user, vector_db, raw_docs)
    return db


# special case for online pdf - for Vector Stores and Retrievers
def create_vector_chroma_online_pdf(user, vector_db, url):
    raw_docs = get_online_pdf_docs(url)
    db = create_vector_chroma(user, vector_db, raw_docs)
    return db


# store vector using chroma
def store_vector_chroma(user, docs, db_path):
    client = chromadb.PersistentClient(path=db_path)
    embeddings = get_embeddings(user)
    db = Chroma.from_documents(documents=docs, embedding=embeddings, client=client, collection_name="my_collection")
    # functions for future advanced use
    # collection = client.get_or_create_collection("my_collection")
    # collection = client.create_collection(name="my_collection", embedding_function=embeddings)
    # collection = client.get_collection(name="my_collection", embedding_function=embeddings)
    # collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])
    # db = Chroma(client=client, collection_name="my_collection", embedding_function=embeddings)
    return db


# retrieve vector from chroma index
def retrieve_vector_chroma(user):
    db_path = get_vector_directory(user)
    if directory_exists(db_path) and not is_directory_empty(db_path):
        client = chromadb.PersistentClient(path=db_path)
        embeddings = get_embeddings(user)
        db = Chroma(client=client, collection_name="my_collection", embedding_function=embeddings)
    else:
        # to use without user data
        db = False
    return db


# close all connections to vector chroma and remove db
def remove_vector_chroma(user):
    db_path = get_vector_directory(user)
    if directory_exists(db_path) and not is_directory_empty(db_path):
        # establish a connection to the SQLite database
        db_file = 'chroma.sqlite3'
        db_file_path = os.path.join(db_path, db_file)
        connection = sqlite3.connect(db_file_path)
        # close the database connection
        connection.close()
        # clean the directory
        empty_directory(db_file_path)
        return True
    else:
        # to use without user data
        return False


# FAISS -----------------------------------------
# db using faiss

# create faiss vector from user files
def create_vector_faiss(user, vector_db, raw_docs):
    db_path = create_vector_directory(user, 'faiss_index')
    docs = get_docs(raw_docs)
    db = store_vector_faiss(user, docs)
    db.save_local(db_path)
    # archive db after creating vector
    archive_vector_db(user, vector_db)
    # clean up tmp directory after creating vector
    tmp_directory = get_tmp_directory(user)
    empty_directory(tmp_directory)
    return db


# special case for web base - for Vector Stores and Retrievers
def create_vector_faiss_web_base(user, vector_db, url):
    raw_docs = get_web_base_docs(url)
    db = create_vector_faiss(user, vector_db, raw_docs)
    return db


# special case for online pdf - for Vector Stores and Retrievers
def create_vector_faiss_online_pdf(user, vector_db, url):
    raw_docs = get_online_pdf_docs(url)
    db = create_vector_faiss(user, vector_db, raw_docs)
    return db


# store vector using faiss
def store_vector_faiss(user, docs):
    embeddings = get_embeddings(user)
    db = FAISS.from_documents(docs, embeddings)
    return db


# retrieve vector from faiss index
def retrieve_vector_faiss(user):
    db_path = get_vector_directory(user)
    if directory_exists(db_path) and not is_directory_empty(db_path):
        embeddings = get_embeddings(user)
        db = FAISS.load_local(db_path, embeddings)
    else:
        # to use without user data
        db = False
    return db


# close all connections to vector faiss and remove db
def remove_vector_faiss(user):
    db_path = get_vector_directory(user)
    if directory_exists(db_path) and not is_directory_empty(db_path):
        # establish a connection to the faiss database
        db_file = 'faiss-index'
        db_file_path = os.path.join(db_path, db_file)
        # connection = faiss.connect(db_file_path)
        # close the database connection
        # connection.close()
        # clean the directory
        empty_directory(db_file_path)
        return True
    else:
        # to use without user data
        return False


# -------------------------------------------------------------------------------------------------
# check vector or get vector status

def check_vector(user):
    path = get_user_directory(user)
    if directory_exists(path):
        return True
    else:
        return False


def get_vector_status(user):
    db_elements = get_active_db_elements(user)
    return db_elements


def get_db_status(db):
    if db:
        status = 'with User Data'
    else:
        status = 'without User Data'
    return status


# -------------------------------------------------------------------------------------------------
# vector DB management - for vector stores

# get vector db archive directory
def get_archive_directory(user):
    path = f'{settings.VECTOR_DB_ARCHIVE}/{str(user.id)}'
    return path


# create vector db archive directory
def create_archive_directory(user):
    path = f'{settings.VECTOR_DB_ARCHIVE}/{str(user.id)}'
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory '{path}' created successfully.")
        except OSError as error:
            print(f"Error creating directory '{path}': {error}")
    else:
        print(f"Directory '{path}' already exists.")
    return path


# create archive index name from list of files
def create_archive_db_name(user, vector_db, db_directory):
    archive_directory = create_archive_directory(user)
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    directory = f'{db_directory}-{timestamp}'
    # directory_path = os.path.join(db_directory, directory)
    archive_path = f'{archive_directory}/{directory}'
    os.makedirs(archive_path)
    # prepare for DB
    author = Account.objects.get(email=user.email)
    # vector_db = vector_db
    db_name = directory
    db_elements = get_file_list_string(user)
    # save to VectorDBArchive
    archive_db = VectorDBArchive(author=author, vector_db=vector_db, db_name=db_name, db_elements=db_elements)
    archive_db.save()
    # update/save to ActiveVectorDB
    try:
        active_db = ActiveVectorDB.objects.get(author=author)
        active_db.vector_db = vector_db
        active_db.db_name = db_name
        active_db.db_elements = db_elements
        active_db.save()
    except ActiveVectorDB.DoesNotExist:
        active_db = ActiveVectorDB(author=author, vector_db=vector_db, db_name=db_name, db_elements=db_elements)
        active_db.save()
    return archive_path


# archive vector db
def archive_vector_db(user, vector_db):
    vector_path = get_vector_directory(user)
    db_directory = os.path.basename(vector_path)
    archive_path = create_archive_db_name(user, vector_db, db_directory)
    copy_directory(vector_path, archive_path)
    return True


# get list of datasets that constitutes the active vector db
def get_active_db_elements(user):
    author = Account.objects.get(email=user.email)
    try:
        obj = ActiveVectorDB.objects.get(author=author)
        db_elements = obj.db_elements
    except ActiveVectorDB.DoesNotExist:
        return ['no dataset']
    return db_elements


# get list of datasets that constitutes the archive vector db
def get_archive_db_elements(directory):
    try:
        obj = VectorDBArchive.objects.get(db_name=directory)
        db_elements = obj.db_elements
    except VectorDBArchive.DoesNotExist:
        return ['no dataset']
    return db_elements


# get active vector db
def get_active_db(user):
    author = Account.objects.get(email=user.email)
    try:
        active_db = ActiveVectorDB.objects.get(author=author)
    except ActiveVectorDB.DoesNotExist:
        return False
    return active_db


# get list of vector directories
def get_vector_db_list(user):
    active_db = get_active_db(user)
    # empty list if no active db
    if not active_db:
        return False
    db_directory = create_archive_directory(user)
    directory_list = []
    # Get a list of files in the directory
    directories = os.listdir(db_directory)
    # Sort the list by modification date in descending order
    directories.sort(key=lambda x: os.path.getmtime(os.path.join(db_directory, x)), reverse=True)
    # Iterate over directory in the db_directory
    for directory in directories:
        directory_path = os.path.join(db_directory, directory)
        timestamp = os.path.getmtime(directory_path)
        date = datetime.fromtimestamp(timestamp).strftime('%b %d, %Y %I:%M %p')
        db_elements = get_archive_db_elements(directory)
        if directory == active_db.db_name:
            status = True
        else:
            status = False
        directory_list.append({'directory': directory, 'db_elements': db_elements, 'date': date, 'status': status})
    return directory_list


# activate db to be active vector db
def activate_vector_db(user, target_db):
    # prepare to copy new active db
    user_path = get_user_directory(user)
    if not is_directory_empty(user_path):
        # close all connections to vector db
        remove_vector(user)
    db_name = target_db.split('-')
    vector_path = create_vector_directory(user, db_name[0])
    archive_directory = get_archive_directory(user)
    archive_path = f'{archive_directory}/{target_db}'
    copy_directory(archive_path, vector_path)
    # update/save to ActiveVectorDB
    db_elements = get_archive_db_elements(target_db)
    author = Account.objects.get(email=user.email)
    try:
        active_db = ActiveVectorDB.objects.get(author=author)
        active_db.db_name = target_db
        active_db.db_elements = db_elements
        active_db.save()
    except ActiveVectorDB.DoesNotExist:
        active_db = ActiveVectorDB(author=author, db_name=target_db, db_elements=db_elements)
        active_db.save()
    return True


# delete directory in vector db
def delete_db_entry(directory):
    try:
        obj = VectorDBArchive.objects.get(db_name=directory)
        obj.delete()
    except VectorDBArchive.DoesNotExist:
        return False
    return True


# delete selected vector directory
def delete_vector_db(user, target_db):
    db_directory = get_archive_directory(user)
    # Remove target db from archive directory
    # Iterate over directory in the db_directory
    for directory in os.listdir(db_directory):
        if directory == target_db:
            directory_path = f'{db_directory}/{target_db}'
            empty_directory(directory_path)
            os.rmdir(directory_path)
    # Remove target db from database entry
    delete_db_entry(target_db)
    return True
