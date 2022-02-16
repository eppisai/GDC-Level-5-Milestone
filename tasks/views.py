from turtle import title
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task
completed = []

def tasks_view(request):
    searchVal = request.GET.get("search")
    tasks = Task.objects.filter(deleted=False, completed=False)
    if searchVal:
        tasks = tasks.filter(title__icontains=searchVal)
    else:
        searchVal = ''
    return render(request,"tasks.html",{"tasks":tasks, "sQuery" : searchVal})

def add_task_view(request):
    task_value = request.GET.get("task")
    task_obj = Task(title=task_value)
    task_obj.save()
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks")

def complete_task_view(request, index):
    thisTask = Task.objects.filter(id=index)
    thisTask.update(completed=True)
    return HttpResponseRedirect("/tasks")

def completed_tasks_view(request):
    completed = Task.objects.all().filter(deleted=False, completed=True)
    return render(request,"display.html",{"completed":completed})

def all_tasks_view(request):
    tasks = Task.objects.filter(deleted=False, completed=False)
    completed = Task.objects.all().filter(deleted=False, completed=True)
    return render(request,"display.html",{"tasks":tasks,"completed":completed})
