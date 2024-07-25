from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from Quiz.serializers import QuizWithCorrectAnswersSerializer
from Quiz.models import Quiz

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def score_quiz(request, pk):
    try:
        quiz = Quiz.objects.get(id=pk)
    except Quiz.DoesNotExist:
        return JsonResponse({'message': f'quiz {pk} doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)

    user_answers = QuizWithCorrectAnswersSerializer(data=JSONParser().parse(request))
    if not user_answers.is_valid():
        return JsonResponse(user_answers.errors, status=status.HTTP_400_BAD_REQUEST)
    correct_answers = QuizWithCorrectAnswersSerializer(quiz).data['questions']

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

