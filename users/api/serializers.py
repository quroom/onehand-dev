from rest_framework import serializers
from users.models import CustomUser, Profile

class UserDisplaySerializer(serializers.ModelSerializer):
    is_authenticated = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "is_authenticated"]

    def get_is_authenticated(self, instance):
        return instance.is_authenticated

class ProfileDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 