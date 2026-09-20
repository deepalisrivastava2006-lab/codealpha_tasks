from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("create-project/", views.create_project, name="create_project"),
    path("project/<int:project_id>/",views.project_detail,name="project_detail"),
    path("project/<int:project_id>/create-task/",views.create_task,name="create_task"),
    path(
    "project/<int:project_id>/add-member/",
    views.add_member,
    name="add_member"
),

path(
    "task/<int:task_id>/update-status/",
    views.update_task_status,
    name="update_task_status"
),

path(
    "task/<int:task_id>/",
    views.task_detail,
    name="task_detail"
),

path(
    "task/<int:task_id>/comment/",
    views.add_comment,
    name="add_comment"
),


]