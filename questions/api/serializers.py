from rest_framework import fields, serializers
from questions.models import Question, Answer, ITEM_CATEGORY, PROS_CATEGORY, TRANSACTION_CATEGORY

class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    average_response_time = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()
    end_date = serializers.DateField()
    moving_date = serializers.DateField()
    user_has_answered = serializers.SerializerMethodField()
    transaction_category = serializers.ChoiceField(choices=TRANSACTION_CATEGORY)
    item_category = serializers.ChoiceField(choices=ITEM_CATEGORY)
    pros_category = fields.MultipleChoiceField(choices=PROS_CATEGORY)

    class Meta:
        model = Question
        exclude = ["updated_at"]
    
    def get_average_response_time(self, instance):
        return instance.author.profile.average_response_time

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        if(request.user.is_anonymous):
            return True
        return instance.answers.filter(author=request.user).exists()
    

class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField(read_only=True)
    question_id = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Answer
        exclude = ["question", "voters", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_question_id(self, instance):
        return instance.question.id

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()