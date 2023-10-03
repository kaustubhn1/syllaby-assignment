from django.urls import path
from .views import BookCollaboratorView


urlpatterns = [
    path('', BookCollaboratorView.as_view()),
    path('<int:id>', BookCollaboratorView.as_view()),
]