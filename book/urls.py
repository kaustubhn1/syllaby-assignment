from django.urls import path
from .views import BookView


urlpatterns = [
    path('', BookView.as_view()),
    path('<int:id>', BookView.as_view()),
]