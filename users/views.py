from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from users.models import Student, Admin
from users.serializers import StudentSerializer, StudentDetailSerializer, AdminSerializer, CustomUserCreateSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student management."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'register':
            return CustomUserCreateSerializer
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new student."""
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                'success': 'Student registered successfully',
                'student': StudentSerializer(student).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile."""
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentDetailSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            # If not a student, try to get as admin
            try:
                admin = Admin.objects.get(user=request.user)
                serializer = AdminSerializer(admin)
                return Response(serializer.data)
            except Admin.DoesNotExist:
                # Fallback: just return user info
                return Response({
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'is_staff': request.user.is_staff,
                })

    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile."""
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentDetailSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)


class AdminViewSet(viewsets.ModelViewSet):
    """ViewSet for Admin management."""
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Admin.objects.none()
        return super().get_queryset()
