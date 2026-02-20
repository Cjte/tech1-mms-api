from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False, default="Viewer")
    is_staff = serializers.BooleanField(required=False, default=False)  # admin site access

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name",
                  "password", "password2", "role", "is_staff")

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.pop('role', 'developer')
        is_staff = validated_data.pop('is_staff', False)
        
        user = User.objects.create_user(**validated_data)
        user.role = role
        user.is_staff = is_staff
        user.save()
        return user
