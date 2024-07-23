from rest_framework import serializers
from .models import Quiz, Question
import logging
import random

logger = logging.getLogger('django')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'is_open_ended', 'answers']

    def validate(self, attrs):
        if 'is_open_ended' not in attrs.keys() or attrs['is_open_ended'] is False:
            is_open_ended = False
        else:
            is_open_ended = True

        logger.info(is_open_ended)

        answer_count = len(attrs['answers'])
        if answer_count == 0:
            raise serializers.ValidationError("A question must have at least 1 answer if it is open ended or 2 answers if it is closed")
        if answer_count == 1 and not is_open_ended:
            raise serializers.ValidationError("A closed question must have at least 2 answers")

        return attrs


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, allow_null=True)

    def validate(self, attrs):
        if len(attrs['questions']) < 1:
            raise serializers.ValidationError("A quiz must have at least 1 question")

        return attrs

    class Meta:
        model = Quiz
        fields = ['name', 'questions']
        
    def create(self, validated_data):
        questions = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question in questions:
            Question.objects.create(quiz=quiz, **question)
        return quiz


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name']


class QuestionWithRandomizedAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'is_open_ended', 'answers']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['is_open_ended']:
            random.shuffle(data['answers'])
        else :
            data.pop('answers', None)

        return data

class QuizWithRandomizedAnswersSerializer(serializers.ModelSerializer):
    questions = QuestionWithRandomizedAnswersSerializer(many=True, allow_null=True)

    class Meta:
        model = Quiz
        fields = ['name', 'questions']

