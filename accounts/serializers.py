from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'fullname', 'email')
