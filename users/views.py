from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, MembershipSerializer

User = get_user_model()

@api_view(['POST'])
def register(request):
    """User registration API"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """User login API"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]
        user = authenticate(phone_number=phone_number, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def activate_membership(request):
    """Activate user membership"""
    serializer = MembershipSerializer(data=request.data)
    if serializer.is_valid():
        membership_type = serializer.validated_data['membership_type']
        user = request.user
        user.activate_membership(membership_type)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Return user profile"""
    return Response(UserSerializer(request.user).data)
