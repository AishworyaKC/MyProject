from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'membership_type', 'membership_start_date', 'membership_expiry_date']

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'username']

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            username=validated_data.get('username', None)
        )
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class MembershipSerializer(serializers.Serializer):
    membership_type = serializers.ChoiceField(choices=['Silver', 'Gold', 'Diamond'])
