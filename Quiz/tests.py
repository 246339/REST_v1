from rest_framework import status
from rest_framework.test import APITestCase
from Quiz.models import Quiz, Question
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class CreateQuiz(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='admin', password='12345')
        self.user.token = Token.objects.create(user=self.user)
        self.user.save()
        self.correct_quiz_data = {
            "name": "Test Quiz",
            "questions": [
                {
                    "text": "What is the capital of France?",
                    "is_open_ended": False,
                    "answers": ["Paris", "London", "Berlin", "Madrid"]
                },
                {
                    "text": "What is the capital of Spain?",
                    "is_open_ended": True,
                    "answers": ["madrid", "MADRID", "MaDriD", "Madrid"]
                }
            ]
        }


    def test_create_quiz_success(self):
        response = self.client.post('/api/quizzes/manage/new/', self.correct_quiz_data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Quiz.objects.get().name, 'Test Quiz')
        self.assertEqual(Question.objects.get(text='What is the capital of France?').answers, ["Paris", "London", "Berlin", "Madrid"])
        self.assertEqual(Question.objects.get(text='What is the capital of Spain?').answers, ["madrid", "MADRID", "MaDriD", "Madrid"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_quiz_no_questions(self):
        data = {
            "name": "Test Quiz",
            "questions": []
        }

        response = self.client.post('/api/quizzes/manage/new/', data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_quiz_no_name(self):
        data = {
            "questions": [
                {
                    "text": "What is the capital of France?",
                    "is_open_ended": False,
                    "answers": ["Paris", "London", "Berlin", "Madrid"]
                },
                {
                    "text": "What is the capital of Spain?",
                    "is_open_ended": True,
                    "answers": ["madrid", "MADRID", "MaDriD", "Madrid"]
                }
            ]
        }

        response = self.client.post('/api/quizzes/manage/new/', data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_quiz_no_answers(self):
        data = {
            "name": "Test Quiz",
            "questions": [
                {
                    "text": "What is the capital of France?",
                    "is_open_ended": False,
                    "answers": []
                },
                {
                    "text": "What is the capital of Spain?",
                    "is_open_ended": True,
                    "answers": []
                }
            ]
        }

        response = self.client.post('/api/quizzes/manage/new/', data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Quiz.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)


    def test_quiz_one_answer(self):
        data = {
            "name": "Test Quiz",
            "questions": [
                {
                    "text": "What is the capital of France?",
                    "is_open_ended": False,
                    "answers": ["Paris"]
                }
            ]
        }

        response = self.client.post('/api/quizzes/manage/new/', data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_not_authenticated(self):
        response = self.client.post('/api/quizzes/manage/new/', self.correct_quiz_data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_not_admin(self):
        user = User.objects.create_user(username='user', password='12345')
        user.token = Token.objects.create(user=user)
        user.save()
        response = self.client.post('/api/quizzes/manage/new/', self.correct_quiz_data, format='json', HTTP_AUTHORIZATION='Token ' + user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_quizzes(self):
        response = self.client.get('/api/quizzes/', format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_get_quiz(self):
        self.client.post('/api/quizzes/manage/new/', self.correct_quiz_data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        id = Quiz.objects.get().id
        response = self.client.get('/api/quizzes/' + str(id), format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Quiz')
        self.assertEqual(response.data['questions'][0]['text'], 'What is the capital of France?')
        self.assertEqual(response.data['questions'][1]['text'], 'What is the capital of Spain?')


    def test_get_quiz_not_authenticated(self):
        self.client.post('/api/quizzes/manage/new/', self.correct_quiz_data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        id = Quiz.objects.get().id
        response = self.client.get('/api/quizzes/' + str(id), format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_quiz_user_score(self):
        self.client.post('/api/quizzes/manage/new/', self.correct_quiz_data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        id = Quiz.objects.get().id
        data = {
            "questions": [
                {
                    "answers": ["Paris"]
                },
                {
                    "answers": ["Madrid"]
                }
            ]
        }
        response = self.client.post('/api/quizzes/' + str(id) + '/score', data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"QuestionCount": 2, "CorrectAnswers": 2}')

        data = {
            "questions": [
                {
                    "answers": ["Paris"]
                },
                {
                    "answers": ["London"]
                }
            ]
        }

        response = self.client.post('/api/quizzes/' + str(id) + '/score', data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"QuestionCount": 2, "CorrectAnswers": 1}')


        data = {
            "questions": [
                {
                    "answers": ["Paris"]
                },
                {
                    "answers": ["London", "New York"]
                }
            ]
        }

        response = self.client.post('/api/quizzes/' + str(id) + '/score', data, format='json', HTTP_AUTHORIZATION='Token ' + self.user.token.key, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
