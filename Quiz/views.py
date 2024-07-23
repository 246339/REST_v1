from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from Quiz.serializers import QuizSerializer, QuizListSerializer, QuizWithRandomizedAnswersSerializer
from Quiz.models import Quiz


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


@api_view(['GET'])
def quiz_list(request):
    quizzes = Quiz.objects.all()
    serializer = QuizListSerializer(quizzes, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def view_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({'message': f'quiz {quiz_id} doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = QuizWithRandomizedAnswersSerializer(quiz)
    return JsonResponse(serializer.data, safe=False)
