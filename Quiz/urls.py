from django.urls import path
from .views import *
from django.views.generic import RedirectView
from django.contrib import admin
from rest_framework import generics
from .serializers import QuizListSerializer, QuizSerializer, QuizWithRandomizedAnswersSerializer
urlpatterns =  [
    path('', RedirectView.as_view(url='api/quizzes/')),
    path('api/quizzes/', generics.ListAPIView.as_view(queryset=Quiz.objects.all(), serializer_class=QuizListSerializer)),
    path('api/quizzes/<int:pk>', generics.RetrieveAPIView.as_view(queryset=Quiz.objects.all(), serializer_class=QuizWithRandomizedAnswersSerializer)),
    path('api/quizzes/<int:pk>/score', view_quiz),
    path('api/quizzes/manage/new/', generics.CreateAPIView.as_view(serializer_class=QuizSerializer)),
    path('api/quizzes/manage/<int:pk>', generics.RetrieveDestroyAPIView.as_view(queryset=Quiz.objects.all(), serializer_class=QuizSerializer)),
    path('admin/', admin.site.urls)
]