from django.urls import path
from .views import quizzes, quiz_list, view_quiz
from django.views.generic import RedirectView
urlpatterns = [
    path('api/quizzes/', quiz_list, name='quizz_list'),
    path('', RedirectView.as_view(url='api/quizzes/')),

    path('api/quizzes/<quiz_id>', view_quiz, name='quizz_list'),
]