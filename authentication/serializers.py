from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from Developments_Test.models import Users


'''class UserFullNameSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        max_length=65, min_length=2, write_only=True)
    class Meta:
        model = Users
        fields = ('full_name',)'''

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8,write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)
    full_names = serializers.CharField(max_length=30, allow_blank=True, source="users.full_name")

    class Meta:
        model = User
        fields = ['username','email', 'password','full_names']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data, instance=None):
        full_name_data = validated_data.pop('users')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Users.objects.update_or_create(user=user, **full_name_data)
        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=2)
    password = serializers.CharField(max_length=65, min_length=8,write_only=True)

    class Meta:
        model = User
        fields = ['username','password']
