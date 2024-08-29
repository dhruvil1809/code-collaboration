from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Project, File, FileVersion

# Project views

def get_file_content(request, file_id):
    file = get_object_or_404(File, id=file_id)
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
    projects = Project.objects.all()
    return render(request, 'accounts/home.html', {'projects': projects})


def current_user_project_list(request):
    user = request.user
    projects = Project.objects.filter(user=user)
    return render(request, 'projects/user_project_list.html', {'projects': projects})


def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    projects = Project.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if Project.objects.filter(name=name).exclude(pk=pk).exists():
            return render(request, 'accounts/home.html', {
                'update_duplicate_project': True,
                'modal_data': {'name': name, 'description': description},
                'project': project,
                'projects': projects,
            })

        # Update project
        project.name = name
        project.description = description
        project.save()

        return redirect('project_list')

    return render(request, 'accounts/home.html', {'project': project})


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})



# File views
def create_file(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')

        if File.objects.filter(name=name).exists():
            return render(request, 'projects/project_detail.html', {
                'duplicate_file': True,
                'modal_data': {'name': name},
                'project': project
            })

        
        if name: 
            file = File(name=name, project=project)
            file.save()
            return redirect('project_detail', pk=project.pk)
        else:
            return render(request, 'projects/project_detail.html', {'project': project})

    return render(request, 'projects/project_detail.html', {'project': project})


def file_edit(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'projects/editor.html', {'file': file})


def update_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    
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
    
    if request.method == 'POST':
        project_pk = file.project.pk
        file.delete()
        return redirect('project_detail', pk=project_pk)
    
    return redirect('project_detail', pk=file.project.pk)


def file_detail(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'projects/file_detail.html', {'file': file})


def save_file_version(file):
    FileVersion.objects.create(file=file, content=file.content)


def revert_file_to_version(request, pk, version_id):
    file = get_object_or_404(File, pk=pk)
    version = get_object_or_404(FileVersion, pk=version_id, file=file)
    
    file.content = version.content
    file.save()
    
    return redirect('file_detail', pk=pk)


def view_file_version(request, file_id, version_id):
    file_version = get_object_or_404(FileVersion, pk=version_id, file_id=file_id)
    return render(request, 'projects/view_file_version.html', {'file_version': file_version})