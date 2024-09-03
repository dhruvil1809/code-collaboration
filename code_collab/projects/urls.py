from django.urls import path
from . import views

urlpatterns = [
    # Project management URLs
    path('', views.project_list, name='project_list'),
    path('list', views.current_user_project_list, name='current_user_project_list'),
    path('create', views.create_project, name='create_project'),
    path('<int:pk>/update', views.update_project, name='update_project'),
    path('<int:pk>/delete', views.delete_project, name='delete_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:project_pk>/add-collaborator/', views.add_collaborator, name='add_collaborator'),
    path('<int:project_pk>/remove-collaborator/<int:user_pk>/', views.remove_collaborator, name='remove_collaborator'),



    # File management URLs
    path('file/create/<int:project_pk>', views.create_file, name='create_file'),
    path('file/<int:pk>/update', views.update_file, name='update_file'),
    path('file/<int:pk>/delete', views.delete_file, name='delete_file'),
    path('file/<int:pk>', views.file_detail, name='file_detail'),
    path('get-file-content/<int:file_id>', views.get_file_content, name='get_file_content'),

    # Real-time code editing URL
    path('file/<int:pk>/edit', views.file_edit, name='file_edit'),

    # Version control URLs
    path('file/<int:pk>/revert/<int:version_id>', views.revert_file_to_version, name='revert_file'),
    path('view-file/<int:file_id>/version/<int:version_id>', views.view_file_version, name='view_file_version'),
]
