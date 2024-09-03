from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Project, File, FileVersion
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

# Helper function to check if the user has access to the project
def user_has_project_permission(user, project):
    return user == project.user or user in project.collaborators.all()

# Project views

def get_file_content(request, file_id):
    file = get_object_or_404(File, id=file_id)
    project = file.project

    if not user_has_project_permission(request.user, project):
        raise PermissionDenied

    content = file.content  
    return JsonResponse({'content': content})


def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if Project.objects.filter(name=name).exists():
            return render(request, 'accounts/home.html', {
                'duplicate_project': True,
                'modal_data': {'name': name, 'description': description}
            })

        if name and description:
            project = Project(name=name, description=description, user=request.user)
            project.save()
            return redirect('project_detail', pk=project.pk)

    return render(request, 'accounts/home.html')


def project_list(request):
    user = request.user
    
    owned_projects = Project.objects.filter(user=user)
    collaborated_projects = Project.objects.filter(collaborators=user)
    
    projects = owned_projects | collaborated_projects
    projects = projects.distinct()

    return render(request, 'accounts/home.html', {'projects': projects})


def current_user_project_list(request):
    user = request.user
    projects = Project.objects.filter(user=user)
    return render(request, 'projects/user_project_list.html', {'projects': projects})


def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not user_has_project_permission(request.user, project):
        raise PermissionDenied

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if Project.objects.filter(name=name).exclude(pk=pk).exists():
            return render(request, 'accounts/home.html', {
                'update_duplicate_project': True,
                'modal_data': {'name': name, 'description': description},
                'project': project
            })

        project.name = name
        project.description = description
        project.save()

        return redirect('project_list')

    return render(request, 'accounts/home.html', {'project': project})


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not user_has_project_permission(request.user, project):
        raise PermissionDenied

    project.delete()
    return redirect('project_list')


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not user_has_project_permission(request.user, project):
        raise PermissionDenied

    collaborators = project.collaborators.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'collaborators': collaborators})


# File views
def create_file(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)

    if not user_has_project_permission(request.user, project):
        raise PermissionDenied
    
    if request.method == 'POST':
        name = request.POST.get('name')

        if File.objects.filter(name=name, project=project).exists():
            return render(request, 'projects/project_detail.html', {
                'duplicate_file': True,
                'modal_data': {'name': name},
                'project': project
            })

        if name: 
            file = File(name=name, project=project)
            file.save()
            return redirect('project_detail', pk=project.pk)

    return render(request, 'projects/project_detail.html', {'project': project})


def file_edit(request, pk):
    file = get_object_or_404(File, pk=pk)

    if not user_has_project_permission(request.user, file.project):
        raise PermissionDenied

    return render(request, 'projects/editor.html', {'file': file})


def update_file(request, pk):
    file = get_object_or_404(File, pk=pk)

    if not user_has_project_permission(request.user, file.project):
        raise PermissionDenied

    if request.method == 'POST':
        new_name = request.POST.get('name')

        if File.objects.filter(name=new_name, project=file.project).exclude(pk=pk).exists():
            return render(request, 'projects/project_detail.html', {
                'update_duplicate_file': True,
                'modal_data': {'name': new_name},
                'file': file,
                'project': file.project
            })

        if new_name:
            file.name = new_name
            file.save()
            return redirect('project_detail', pk=file.project.pk)
    
    return render(request, 'projects/project_detail.html', {'file': file, 'project': file.project})


def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)

    if not user_has_project_permission(request.user, file.project):
        raise PermissionDenied

    if request.method == 'POST':
        project_pk = file.project.pk
        file.delete()
        return redirect('project_detail', pk=project_pk)

    return redirect('project_detail', pk=file.project.pk)


def file_detail(request, pk):
    file = get_object_or_404(File, pk=pk)

    if not user_has_project_permission(request.user, file.project):
        raise PermissionDenied

    return render(request, 'projects/file_detail.html', {'file': file})


def revert_file_to_version(request, pk, version_id):
    file = get_object_or_404(File, pk=pk)

    if not user_has_project_permission(request.user, file.project):
        raise PermissionDenied

    version = get_object_or_404(FileVersion, pk=version_id, file=file)
    
    file.content = version.content
    file.save()
    
    return redirect('file_detail', pk=pk)


def view_file_version(request, file_id, version_id):
    file_version = get_object_or_404(FileVersion, pk=version_id, file_id=file_id)

    if not user_has_project_permission(request.user, file_version.file.project):
        raise PermissionDenied

    return render(request, 'projects/view_file_version.html', {'file_version': file_version})


def add_collaborator(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)

    if not user_has_project_permission(request.user, project):
        raise PermissionDenied

    collaborators = project.collaborators.all()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            
            if user != project.user and user not in project.collaborators.all():
                project.collaborators.add(user)
                project.save()
                return redirect('project_detail', pk=project.pk)
            else:
                return render(request, 'projects/project_detail.html', {
                    'project': project,
                    'collaborators': collaborators,
                    'error_message': "User is already a collaborator or is the project owner."
                })
        except User.DoesNotExist:
            return render(request, 'projects/project_detail.html', {
                'project': project,
                'collaborators': collaborators,
                'error_message': "User does not exist."
            })

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'collaborators': collaborators
    })


def remove_collaborator(request, project_pk, user_pk):
    project = get_object_or_404(Project, pk=project_pk)

    if not user_has_project_permission(request.user, project):
        raise PermissionDenied

    user = get_object_or_404(User, pk=user_pk)

    if user in project.collaborators.all():
        project.collaborators.remove(user)
        project.save()
    
    return redirect('project_detail', pk=project.pk)
