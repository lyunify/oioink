from django.urls import path
from django.contrib.auth import views
from . import views


app_name = 'data'

urlpatterns = [
    # data upload
    path('data_upload/', views.data_upload_view, name='data_upload'),
    # file upload
    path('file_upload/', views.file_upload_view, name='file_upload'),
    # csv upload
    path('csv_upload/', views.csv_upload_view, name='csv_upload'),
    # web base upload
    path('web_base_upload/', views.web_base_upload_view, name='web_base_upload'),
    # online upload
    path('online_pdf_upload/', views.online_pdf_upload_view, name='online_pdf_upload'),
    # directory upload
    path('directory_upload/', views.directory_upload_view, name='directory_upload'),
    # file list
    path('file_list/', views.file_list_view, name='file_list'),
    # create vector db
    path('vector_db/', views.vector_db_view, name='vector_db'),
    # create vector db
    path('vector_db_list/', views.vector_db_list_view, name='vector_db_list'),
    # llm settings
    path('llm_settings/', views.llm_settings_view, name='llm_settings'),
    # llm settings change/update
    path('llm_settings_update/', views.llm_settings_update_view, name='llm_settings_update'),
    # delete file using slug
    # path('<slug>/', views.delete_file_view, name='delete_file'),
    # delete file
    path('delete_file/<str:uploaded_file>', views.delete_file_view, name='delete_file'),
    # activate vector db
    path('activate_vector_db/<str:vector_db>', views.activate_vector_db_view, name='activate_vector_db'),
    # delete vector db
    path('delete_vector_db/<str:vector_db>', views.delete_vector_db_view, name='delete_vector_db'),
]
