from django.urls import path
from .views import quizzes
from django.views.generic import RedirectView
urlpatterns = [
    path('api/quizzes/', quizzes, name='quizzes'),
    path('', RedirectView.as_view(url='api/quizzes/'))

]