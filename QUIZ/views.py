from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from QUIZ.serializers import QuizSerializer
from QUIZ.models import Quiz

@api_view(['GET', 'POST', 'DELETE'])
def quizzes(request):
  if request.method == 'GET':
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return JsonResponse(serializer.data, safe=False)
  elif request.method == 'POST':
    request_data = JSONParser().parse(request)
    serializer = QuizSerializer(data=request_data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
