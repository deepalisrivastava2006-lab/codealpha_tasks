from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project, Task, Comment


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("dashboard")

    return render(request, "core/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "core/login.html")


@login_required
def dashboard(request):
    projects = Project.objects.filter(members=request.user) | Project.objects.filter(owner=request.user)

    return render(
        request,
        "core/dashboard.html",
        {"projects": projects.distinct()}
    )

@login_required
def create_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        project = Project.objects.create(
            name=name,
            description=description,
            owner=request.user
        )

        project.members.add(request.user)

        return redirect("dashboard")

    return render(request, "core/create_project.html")

@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.user != project.owner and request.user not in project.members.all():
        return redirect("dashboard")

    tasks = project.tasks.all()

    return render(
        request,
        "core/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
        }
    )


@login_required
def create_task(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.user != project.owner and request.user not in project.members.all():
        return redirect("dashboard")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        assigned_to_id = request.POST.get("assigned_to")
        status = request.POST.get("status")
        due_date = request.POST.get("due_date")

        assigned_to = None

        if assigned_to_id:
            assigned_to = User.objects.get(id=assigned_to_id)

        Task.objects.create(
            project=project,
            title=title,
            description=description,
            assigned_to=assigned_to,
            status=status,
            due_date=due_date if due_date else None
        )

        return redirect("project_detail", project_id=project.id)

    members = project.members.all()

    return render(
        request,
        "core/create_task.html",
        {
            "project": project,
            "members": members,
        }
    )

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def add_member(request, project_id):

    project = Project.objects.get(id=project_id)

    if request.user != project.owner:
        return redirect("project_detail", project_id=project.id)

    if request.method == "POST":

        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)

            if user not in project.members.all():
                project.members.add(user)

            return redirect("project_detail", project_id=project.id)

        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return redirect("project_detail", project_id=project.id)


@login_required
def update_task_status(request, task_id):

    task = Task.objects.get(id=task_id)

    project = task.project

    if request.user != project.owner and request.user not in project.members.all():
        return redirect("dashboard")

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status in ["todo", "progress", "done"]:
            task.status = new_status
            task.save()

    return redirect("project_detail", project_id=project.id)


@login_required
def task_detail(request, task_id):

    task = Task.objects.get(id=task_id)

    project = task.project

    if request.user != project.owner and request.user not in project.members.all():
        return redirect("dashboard")

    comments = task.comments.all()

    return render(
        request,
        "core/task_detail.html",
        {
            "task": task,
            "comments": comments,
        }
    )


@login_required
def add_comment(request, task_id):

    task = Task.objects.get(id=task_id)

    project = task.project

    if request.user != project.owner and request.user not in project.members.all():
        return redirect("dashboard")

    if request.method == "POST":

        text = request.POST.get("text")

        if text:
            Comment.objects.create(
                task=task,
                user=request.user,
                text=text
            )

    return redirect("task_detail", task_id=task.id)



