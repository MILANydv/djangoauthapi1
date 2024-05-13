from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import CategorySerializer, SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserProfileUpdateSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Category, Profile
from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.shortcuts import render
from django.http import Http404

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


def send_email_after_registration(email, token):
  subject = "Verify Email"
  message = f"Hi Click on the link to verify your account 'http://127.0.0.1:8000/account-verify/{token}'" 
  from_email = settings.EMAIL_HOST_USER
  recipient_list = [email]
  try:
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
    print('email sent')
  except:
     print('email not sent')

def account_verify(request, token):
    try:
        pf = Profile.objects.get(token=token)
        
        if pf.verify:
            return render(request, 'verifypage.html', {'message': 'Your account is already verified.'})
        
        pf.verify = True
        pf.save()
        
        return render(request, 'verifypage.html', {'message': 'Your account has been verified successfully.'})
        
    except Profile.DoesNotExist:
        return render(request, 'verifypage.html', {'message': 'Invalid verification link.'})


class VerifyPage(APIView):
   def get(self, request):
      return render(request, 'verifypage.html')

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]  

    def post(self, request, format=None):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            uid = uuid.uuid4()
            print(uid)
            pro_obj = Profile(user=new_user, token=uid)
            pro_obj.save()
            send_email_after_registration(new_user.email, uid )
                       
            return Response({
                'status': 'success',
                'message': 'Your Account Created Successfully, to verify your Account Check Your Email'
            }, status=status.HTTP_201_CREATED)
        
        # If serializer is not valid, return error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                pro = Profile.objects.get(user=user)
                
                if pro.verify:
                    token = get_tokens_for_user(user)
                    return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'Your account is not verified, please check your email and verify your Account'}, status=status.HTTP_404_NOT_FOUND)
            
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if 'current_password' not in request.data:
            return Response({'error': 'Current password is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  
class UserProfileUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, format=None):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
