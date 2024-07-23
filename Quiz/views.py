from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from Quiz.serializers import QuizSerializer, QuizListSerializer, QuizWithRandomizedAnswersSerializer, QuizWithCorrectAnswersSerializer
from Quiz.models import Quiz

import logging


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


@api_view(['GET', 'POST'])
def view_quiz(request, quiz_id):
    logger = logging.getLogger('django')
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({'message': f'quiz {quiz_id} doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuizWithRandomizedAnswersSerializer(quiz)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        user_answers = QuizWithCorrectAnswersSerializer(data=JSONParser().parse(request))
        if not user_answers.is_valid():
            return JsonResponse(user_answers.errors, status=status.HTTP_400_BAD_REQUEST)
        logger.info(user_answers.validated_data['questions'])
        correct_answers = QuizWithCorrectAnswersSerializer(quiz).data['questions']

        logger.info(f'user_answers: {user_answers.validated_data}')
        logger.info(f'correct_answers: {correct_answers}')

        user_answers = user_answers.validated_data['questions']

        CorrectAnswers = 0;
        QuestionCount = len(correct_answers)

        if len(user_answers) != len(correct_answers):
            return JsonResponse({'message': 'user answers must have the same number of questions as the quiz'}, status=status.HTTP_400_BAD_REQUEST)

        for i in range(QuestionCount):
            if len(user_answers[i]['answers']) != 1:
                return JsonResponse({'message': 'each question must have exactly 1 answer'}, status=status.HTTP_400_BAD_REQUEST)

            if user_answers[i]['answers'][0] in correct_answers[i]['answers']:
                CorrectAnswers += 1


        return JsonResponse({"QuestionCount":QuestionCount, "CorrectAnswers":CorrectAnswers}, status=status.HTTP_200_OK)
