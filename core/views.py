from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View

from .models import Todo


def index_view(request):
    todos = Todo.objects.all()

    return render(request, "index.html", context={"todos": todos})


class TodoUpdateView(View):
    def get(self, request, todo_id):
        todo = get_object_or_404(Todo.objects.all(), id=todo_id)
        return render(request, "update-todo.html", {"todo": todo})

    def post(self, request, todo_id):
        todo = get_object_or_404(Todo.objects.all(), id=todo_id)

        action = request.GET.get("action")

        if action == "state":
            todo.done = not todo.done
            todo.save()
            return render(request, "oob-todo_detail_hx.html", {"todo": todo, "swap_oob": False})

        todo.name = request.POST["name"]
        todo.done = request.POST.get("done", False) is not False
        todo.save()
        return render(request, "oob-todo_detail_hx.html", {"todo": Todo.objects.get(id=todo_id)})


class TodoView(View):
    def post(self, request):
        name = request.POST["name"]
        done = request.POST.get("done", False)
        todo = Todo.objects.create(name=name, done=done)
        return render(request, "oob-todo_detail_add_hx.html", {"todo": todo})

    def get(self, request, todo_id):
        todo = get_object_or_404(Todo.objects.all(), id=todo_id)
        return render(request, "oob-todo_detail_hx.html", {"todo": todo})

    def delete(self, request, todo_id):
        todo = get_object_or_404(Todo.objects.all(), id=todo_id)
        todo.delete()
        return HttpResponse(status=200)
