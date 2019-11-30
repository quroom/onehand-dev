from rest_framework import fields, serializers
from questions.models import Question, Answer, ITEM_CATEGORY, TRADE_CATEGORY

class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()
    end_date = serializers.DateTimeField()
    moving_date = serializers.DateField()
    user_has_answered = serializers.SerializerMethodField()
    trade_category = fields.MultipleChoiceField(choices=TRADE_CATEGORY)
    item_category = fields.MultipleChoiceField(choices=ITEM_CATEGORY)

    class Meta:
        model = Question
        exclude = ["updated_at"]
  
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d %Y")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()

class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        exclude = ["question"]