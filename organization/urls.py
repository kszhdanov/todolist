from django.urls import path

from .views import CustomAuthTokenView
from .views import OrganizationTodoListView
from .views import OrganizationViewDetail
from .views import OrganizationViewList
from .views import TodoViewDetail
from .views import TodoViewList

app_name = "organization"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('todos/', TodoViewList.as_view()),
    path('todos/<int:pk>', TodoViewDetail.as_view()),
    path('organizations/', OrganizationViewList.as_view()),
    path('organizations/<int:pk>', OrganizationViewDetail.as_view()),
    path('organizations/<int:pk>/todolist', OrganizationTodoListView.as_view()),
    path('organizations/<int:pk>/api-token-auth', CustomAuthTokenView.as_view()),
]