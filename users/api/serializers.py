from rest_framework import serializers
from users.models import CustomUser, Profile

class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username"]

class ProfileDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 