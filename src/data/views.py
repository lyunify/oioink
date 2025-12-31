from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Account
from .models import FileUpload, LLMSettings, upload_path
from .forms import FileUploadForm, WebBaseUploadForm, OnlinePDFUploadForm, DirectoryUploadForm
from .forms import VectorDBForm, LLMSettingsForm, LLMSettingsUpdateForm
from lib.utils import create_tmp_directory, delete_file, get_file_list, download_url_content
from .vectors import create_vector, create_vector_web_base, create_vector_online_pdf, get_vector_db_list, activate_vector_db, delete_vector_db
from .loaders import get_file_docs,get_csv_docs, get_directory_docs
from .llm_settings import set_default_llm_settings

FILE_LIST_PER_PAGE = 10
VECTOR_DB_LIST_PER_PAGE = 10


@login_required
def data_upload_view(request, *args, **kwargs):
    context = {}
    return render(request, 'data/data_upload.html', context)


@login_required
def file_upload_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            directory = create_tmp_directory(user)
            fs = FileSystemStorage(location=directory)
            file = request.FILES['doc_file']
            file_name = fs.save(file.name, file)
            raw_docs = get_file_docs(user)
            db = create_vector(user, raw_docs)
            if db:
                context['status_message'] = 'File uploaded / vector DB created'
                return render(request, 'data/file_upload.html', context)
            else:
                context['status_message'] = 'File not uploaded / vector DB not created'
                return render(request, 'data/file_upload.html', context)
        else:
            form = FileUploadForm()
            context['form'] = form
            context['status_message'] = 'File not uploaded'
            return render(request, 'data/file_upload.html', context)
    else:
        set_default_llm_settings(user)
        form = FileUploadForm()
    context['form'] = form
    return render(request, 'data/file_upload.html', context)


@login_required
def csv_upload_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            directory = create_tmp_directory(user)
            fs = FileSystemStorage(location=directory)
            file = request.FILES['doc_file']
            file_name = fs.save(file.name, file)
            elements = form.data['doc_elements']
            print(elements)
            raw_docs = get_csv_docs(user, elements)
            db = create_vector(user, raw_docs)
            if db:
                context['status_message'] = 'CSV uploaded / vector DB created'
                return render(request, 'data/csv_upload.html', context)
            else:
                context['status_message'] = 'CSV not uploaded / vector DB not created'
                return render(request, 'data/csv_upload.html', context)
        else:
            form = FileUploadForm()
            context['form'] = form
            context['status_message'] = 'CSV not uploaded'
            return render(request, 'data/csv_upload.html', context)
    else:
        set_default_llm_settings(user)
        form = FileUploadForm()
    context['form'] = form
    return render(request, 'data/csv_upload.html', context)


@login_required
def web_base_upload_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = WebBaseUploadForm(request.POST)
        if form.is_valid():
            url = form.data['doc_file']
            # create a tmp file using url to show elements of vector_db
            directory = create_tmp_directory(user)
            path = download_url_content(directory, url)
            db = create_vector_web_base(user, url)
            if db:
                context['status_message'] = 'Web content uploaded / vector DB created'
                return render(request, 'data/web_base_upload.html', context)
            else:
                context['status_message'] = 'Web content not uploaded / vector DB not created'
                return render(request, 'data/web_base_upload.html', context)
        else:
            form = WebBaseUploadForm()
            context['form'] = form
            context['status_message'] = 'Web content not uploaded'
            return render(request, 'data/web_base_upload.html', context)
    else:
        set_default_llm_settings(user)
        form = WebBaseUploadForm()
    context['form'] = form
    return render(request, 'data/web_base_upload.html', context)


@login_required
def online_pdf_upload_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = OnlinePDFUploadForm(request.POST)
        if form.is_valid():
            url = form.data['doc_file']
            # create a tmp file using url to show elements of vector_db
            directory = create_tmp_directory(user)
            path = download_url_content(directory, url)
            db = create_vector_online_pdf(user, url)
            if db:
                context['status_message'] = 'Online PDF uploaded / vector DB created'
                return render(request, 'data/online_pdf_upload.html', context)
            else:
                context['status_message'] = 'Online PDF not uploaded / vector DB not created'
                return render(request, 'data/online_pdf_upload.html', context)
        else:
            form = OnlinePDFUploadForm()
            context['form'] = form
            context['status_message'] = 'Online PDF not uploaded'
            return render(request, 'data/online_pdf_upload.html', context)
    else:
        set_default_llm_settings(user)
        form = OnlinePDFUploadForm()
    context['form'] = form
    return render(request, 'data/online_pdf_upload.html', context)


# -----------------------------------------------------------------------------
# Mutiple Files

@login_required
def directory_upload_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = DirectoryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            directory = create_tmp_directory(user)
            fs = FileSystemStorage(location=directory)
            files = request.FILES.getlist('doc_file')
            for file in files:
                file_name = fs.save(file.name, file)
            raw_docs = get_directory_docs(user)
            db = create_vector(user, raw_docs)
            if db:
                context['status_message'] = 'Multiple files uploaded / vector DB created'
                return render(request, 'data/directory_upload.html', context)
            else:
                context['status_message'] = 'Multiple files not uploaded / vector DB not created'
                return render(request, 'data/directory_upload.html', context)
        else:
            form = DirectoryUploadForm()
            context['form'] = form
            context['status_message'] = 'Files not uploaded'
            return render(request, 'data/directory_upload.html', context)
    else:
        set_default_llm_settings(user)
        form = DirectoryUploadForm()
    context['form'] = form
    return render(request, 'data/directory_upload.html', context)


@login_required
def file_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    uploaded_files = get_file_list(user)
    if uploaded_files:
        # number of posts to display per page - set to 10
        per_page = FILE_LIST_PER_PAGE
        paginator = Paginator(uploaded_files, per_page)
        page = request.GET.get('page')
        paginated_uploaded_files = paginator.get_page(page)
        context['uploaded_files'] = paginated_uploaded_files
        # return render(request, 'data/file_list.html', {'uploaded_files': paginated_uploaded_files})
        return render(request, 'data/file_list.html', context)
    else:
        context['uploaded_files'] = {}
        return render(request, 'data/file_list.html', context)


@login_required
def delete_file_view(request, uploaded_file):
    context = {}
    user = request.user
    # uploaded_file = os.path.basename(request.path)
    delete_file(user, uploaded_file)
    # reload uploaded_file_view
    uploaded_files = get_file_list(user)
    if uploaded_files:
        # number of posts to display per page - set to 10
        per_page = FILE_LIST_PER_PAGE
        paginator = Paginator(uploaded_files, per_page)
        page = request.GET.get('page')
        paginated_uploaded_files = paginator.get_page(page)
        context['uploaded_files'] = paginated_uploaded_files
        # return render(request, 'data/file_list.html', {'uploaded_files': paginated_uploaded_files})
        return render(request, 'data/file_list.html', context)
    else:
        context['uploaded_files'] = {}
        return render(request, 'data/file_list.html', context)


# -----------------------------------------------------------------------------
# Vector DB

@login_required
def vector_db_view(request, *args, **kwargs):
    context = {}
    user = request.user
    author = Account.objects.get(email=user.email)
    try:
        settings_instance = LLMSettings.objects.get(author=author)
        if request.method == 'POST':
            form = VectorDBForm(request.POST, instance=settings_instance)
            if form.is_valid():
                raw_docs = get_directory_docs(user)
                db = create_vector(user, raw_docs)
                if db:
                    context['status_message'] = 'Vector DB created'
                    return render(request, 'data/vector_db.html', context)
                else:
                    context['status_message'] = 'Vector DB not created'
                    return render(request, 'data/vector_db.html', context)
        else:
            form = VectorDBForm(instance=settings_instance)
            context['form'] = form
            return render(request, 'data/vector_db.html', context)
    except LLMSettings.DoesNotExist:
        if request.method == 'POST':
            form = LLMSettingsUpdateForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = author
                instance.save()
                context['status_message'] = 'LLM settings set'
            settings_instance = LLMSettings.objects.get(author=author)
            form = VectorDBForm(instance=settings_instance)
            context['form'] = form
            return render(request, 'data/llm_settings.html', context)
        else:
            form = LLMSettingsUpdateForm()
            return render(request, 'data/llm_settings_update.html', context)


@login_required
def vector_db_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    vector_dbs = get_vector_db_list(user)
    if vector_dbs:
        # number of posts to display per page - set to 10
        per_page = VECTOR_DB_LIST_PER_PAGE
        paginator = Paginator(vector_dbs, per_page)
        page = request.GET.get('page')
        paginated_vector_dbs = paginator.get_page(page)
        context['vector_dbs'] = paginated_vector_dbs
        # return render(request, 'data/vector_db_list.html', {'vector_dbs': paginated_vector_dbs})
        return render(request, 'data/vector_db_list.html', context)
    else:
        context['vector_dbs'] = {}
        return render(request, 'data/vector_db_list.html', context)


@login_required
def activate_vector_db_view(request, vector_db):
    context = {}
    user = request.user
    # make selected db as active vector db
    activate_vector_db(user, vector_db)
    # after deleting, redisplay the vector db list
    vector_dbs = get_vector_db_list(user)
    if vector_dbs:
        # number of posts to display per page - set to 10
        per_page = VECTOR_DB_LIST_PER_PAGE
        paginator = Paginator(vector_dbs, per_page)
        page = request.GET.get('page')
        paginated_vector_dbs = paginator.get_page(page)
        context['vector_dbs'] = paginated_vector_dbs
        # return render(request, 'data/vector_db_list.html', {'vector_dbs': paginated_vector_dbs})
        return render(request, 'data/vector_db_list.html', context)
    else:
        context['vector_dbs'] = {}
        return render(request, 'data/vector_db_list.html', context)


@login_required
def delete_vector_db_view(request, vector_db):
    context = {}
    user = request.user
    # vector_db = os.path.basename(request.path)
    # delete selected db
    delete_vector_db(user, vector_db)
    # after deleting, redisplay the vector db list
    vector_dbs = get_vector_db_list(user)
    if vector_dbs:
        # number of posts to display per page - set to 10
        per_page = VECTOR_DB_LIST_PER_PAGE
        paginator = Paginator(vector_dbs, per_page)
        page = request.GET.get('page')
        paginated_vector_dbs = paginator.get_page(page)
        context['vector_dbs'] = paginated_vector_dbs
        # return render(request, 'data/vector_db_list.html', {'vector_dbs': paginated_vector_dbs})
        return render(request, 'data/vector_db_list.html', context)
    else:
        context['vector_dbs'] = {}
        return render(request, 'data/vector_db_list.html', context)


@login_required
def llm_settings_view(request, *args, **kwargs):
    context = {}
    user = request.user
    author = Account.objects.get(email=user.email)
    try:
        settings_instance = LLMSettings.objects.get(author=author)
        form = LLMSettingsForm(request.POST, instance=settings_instance)
        context['form'] = form
        return render(request, 'data/llm_settings.html', context)
    except LLMSettings.DoesNotExist:
        if request.method == 'POST':
            form = LLMSettingsUpdateForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = author
                instance.save()
                context['status_message'] = 'LLM settings set'
            settings_instance = LLMSettings.objects.get(author=author)
            form = LLMSettingsForm(instance=settings_instance)
            context['form'] = form
            return render(request, 'data/llm_settings.html', context)
        else:
            form = LLMSettingsUpdateForm()
            return render(request, 'data/llm_settings_update.html', context)
    # context['form'] = form
    # return render(request, 'data/llm_settings.html', context)


@login_required
def llm_settings_update_view(request, *args, **kwargs):
    context = {}
    user = request.user
    author = Account.objects.get(email=user.email)
    try:
        settings_instance = LLMSettings.objects.get(author=author)
        if request.method == 'POST':
            form = LLMSettingsUpdateForm(request.POST, instance=settings_instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = author
                instance.save()
                context['status_message'] = 'LLM settings set'
            settings_instance = LLMSettings.objects.get(author=author)
            form = LLMSettingsForm(instance=settings_instance)
            context['form'] = form
            return render(request, 'data/llm_settings.html', context)
        else:
            form = LLMSettingsUpdateForm()
            return render(request, 'data/llm_settings_update.html', context)
    except LLMSettings.DoesNotExist:
        if request.method == 'POST':
            form = LLMSettingsUpdateForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = author
                instance.save()
                context['status_message'] = 'LLM settings set'
            settings_instance = LLMSettings.objects.get(author=author)
            form = LLMSettingsForm(instance=settings_instance)
            context['form'] = form
            return render(request, 'data/llm_settings.html', context)
        else:
            form = LLMSettingsUpdateForm()
            return render(request, 'data/llm_settings_update.html', context)
    # context['form'] = form
    # return render(request, 'data/llm_settings_update.html', context)
