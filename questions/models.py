from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField
from datetime import datetime
from items.models import Item

#ONR / TWR / THR / FOR / SHH / OFT
#APT / VIL / HOS / CMH /
#STO /
#LND
ITEM_CATEGORY = (
    ('ONR', '원룸'),
    ('TWR', '투룸'),
    ('THR', '쓰리룸'),
    ('FOR', '포룸'),
    ('SHH', '쉐어하우스'),
    ('OFT', '오피스텔'),
    ('APT', '아파트'),
    ('VIL', '빌라'),
    ('HOS', '단독주택'),
    ('CMH', '상가주택'),
    ('STO', '상가'),
    ('LND', '토지')
)
#TR(TRADE) DL(Deposit Loan) RT(Rent) EX(Exchange) CS(Consulting)
TRANSACTION_CATEGORY = (
    ('TR', '매매'),
    ('DL', '전세'),
    ('RT', '월세'),
    ('EX', '교환'),
    ('CS', '상담')
)

#REB(Real Estate Brokerage) / TAX(Tax) / RGS(Registered) / LAW(Law)
#LON(Loan) / INR(Interior) / CLN(Clean) / MOV(Move) / PRC(Pre-Check)
#HAP(Home Appliance Purchase) / FRP(Furniture Purchase)
PROS_CATEGORY = (
    ('REB', '중개'),
    ('TAX', '세무'),
    ('RES', '등기'),
    ('LAW', '법률'),
    ('LON', '대출'),
    ('INR', '인테리어'),
    ('CLN', '청소'),
    ('MOV', '이사'),
    ('PRC', '입주사전점검'),
    ('HAP', '가전구매'),
    ('FRP', '가구구매'),
)

# Create your models here.
class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name="questions")
    trade_price = models.BigIntegerField(default=0)
    deposit = models.BigIntegerField(default=0)
    end_date = models.DateField(blank=True, null=True)
    is_question_done = models.BooleanField(default=False)
    item_category = models.CharField(max_length=3, choices=ITEM_CATEGORY, default='NA')
    land_area = models.IntegerField(default=0)
    building_area = models.IntegerField(default=0)
    from_location = models.CharField(max_length=100, blank=True)
    monthly_fee = models.IntegerField(default=0)
    move_date = models.DateField(blank=True, null=True)
    pros_category = MultiSelectField(choices=PROS_CATEGORY, default='NA')
    to_location = models.CharField(max_length=100, blank=True)
    transaction_category = models.CharField(max_length=2, choices=TRANSACTION_CATEGORY, default='NA')
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