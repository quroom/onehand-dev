from rest_framework import fields, serializers
from questions.models import Question, Answer, ITEM_CATEGORY, TRADE_CATEGORY

class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    average_response_time = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()
    end_date = serializers.DateField()
    moving_date = serializers.DateField()
    user_has_answered = serializers.SerializerMethodField()
    trade_category = fields.MultipleChoiceField(choices=TRADE_CATEGORY)
    item_category = fields.MultipleChoiceField(choices=ITEM_CATEGORY)

    class Meta:
        model = Question
        exclude = ["updated_at"]
    
    def get_average_response_time(self, instance):
        return instance.author.profile.average_response_time

    def get_end_date(self, instance):
        return instance.created_at.strftime("yyyy-MM-ddThh:mm")

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d %Y")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()
    

class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    question_id = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ["question"]

    def get_question_id(self, instance):
        return instance.question.id