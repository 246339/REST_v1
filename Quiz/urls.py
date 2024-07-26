from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from .models import Quiz
from .views import score_quiz
from rest_framework.authtoken import views
from django.views.generic import RedirectView
from django.contrib import admin
from rest_framework import generics
from .serializers import QuizListSerializer, QuizSerializer, QuizWithRandomizedAnswersSerializer
from rest_framework import permissions
urlpatterns =  [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', RedirectView.as_view(url='api/quizzes/')),
    path('api/quizzes/', generics.ListAPIView.as_view(queryset=Quiz.objects.all(), serializer_class=QuizListSerializer, permission_classes=[permissions.IsAuthenticated])),
    path('api/quizzes/<int:pk>', generics.RetrieveAPIView.as_view(queryset=Quiz.objects.all(), serializer_class=QuizWithRandomizedAnswersSerializer, permission_classes=[permissions.IsAuthenticated])),
    path('api/quizzes/<int:pk>/score', score_quiz),
    path('api/quizzes/manage/new/', generics.CreateAPIView.as_view(serializer_class=QuizSerializer, permission_classes=[permissions.IsAdminUser])),
    path('api/quizzes/manage/<int:pk>', generics.RetrieveDestroyAPIView.as_view(queryset=Quiz.objects.all(), serializer_class=QuizSerializer, permission_classes=[permissions.IsAdminUser])),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token)
]
