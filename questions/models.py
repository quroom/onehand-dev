from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField
from datetime import datetime
from items.models import Item

ITEM_CATEGORY = (
    (1, '원룸'), (2, '투룸'), (3, '쓰리룸'), (4, '포룸'), (5, '쉐어하우스'), (6, '오피스텔'),
    (21, '아파트'), (22, '빌라'), (23, '단독주택'), (24, '상가주택'),
    (31, '상가'),
    (41, '토지')
)

TRADE_CATEGORY = (
    (1, '매매'), (2, '전세'), (3, '월세'), (4, '교환')
)

PROS_CATEGORY = (
    (1, '중개사'), (2, '세무사'), (3, '법무사'), (4, '변호사'),
    (11, '대출'), (12, '인테리어'), (13, '청소'), (14, '이사'),
    (21, '가전구매'), (22, '가구구매'),
)

# Create your models here.
class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    additional_request = models.CharField(max_length=45, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name="questions")
    trade_price = models.BigIntegerField(default=0)
    deposit = models.BigIntegerField(default=0)
    end_date = models.DateField()
    is_question_done = models.BooleanField(default=False)
    item_category = models.IntegerField(choices=ITEM_CATEGORY, default=0)
    from_area = models.IntegerField(default=0)
    from_location = models.CharField(max_length=100, blank=True)
    monthly_fee = models.IntegerField(default=0)
    moving_date = models.DateField()
    pros_category = MultiSelectField(choices=PROS_CATEGORY, default=0)
    to_area = models.IntegerField(default=0)
    to_location = models.CharField(max_length=100, blank=True)
    trade_category = models.IntegerField(choices=TRADE_CATEGORY, default=0)
    etc = models.TextField(blank=True)
    # selected_answer = models.ForeignKey(Answer, related_name='questions')

class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name="answers")
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)
    question = models.ForeignKey(Question,
                            on_delete=models.CASCADE,
                            related_name="answers")
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="votes")