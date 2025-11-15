from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Student, Admin


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model."""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'username', 'email', 'first_name', 'last_name', 'student_id', 'phone', 'profile_picture', 'is_verified', 'created_at']
        read_only_fields = ['id', 'user_id', 'created_at', 'is_verified']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Student model."""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'username', 'email', 'first_name', 'last_name', 'student_id', 'phone', 'profile_picture', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at', 'is_verified']


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for Admin model."""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Admin
        fields = ['id', 'user_id', 'username', 'email', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'user_id', 'created_at']


class CustomUserCreateSerializer(serializers.Serializer):
    """Custom serializer for user registration."""
    username = serializers.CharField(required=True, min_length=3)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    student_id = serializers.CharField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        student = Student.objects.create(
            user=user,
            student_id=validated_data['student_id'],
            phone=validated_data.get('phone', '')
        )
        return student
