from rest_framework import serializers
from users.models import Student, Admin


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model."""
    
    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'student_id', 'phone', 'profile_picture', 'is_active', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Student model."""
    
    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'student_id', 'phone', 'profile_picture', 'is_active', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified']


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for Admin model."""
    
    class Meta:
        model = Admin
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'created_at']
        read_only_fields = ['id', 'created_at']


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Custom serializer for user creation."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Student
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'student_id', 'phone']

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password
        validated_data['password_hash'] = make_password(validated_data.pop('password'))
        return super().create(validated_data)


class CustomUserSerializer(StudentSerializer):
    """Custom serializer for user display."""
    pass
