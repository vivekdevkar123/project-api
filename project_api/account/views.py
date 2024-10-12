import random
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer,SendOTPSerializer,VerifyOTPSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.utils import timezone
from account.models import Student
from account.utils import Util
import requests

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
  
class SendOTPView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = random.randint(100000, 999999)

        print(f'Setting OTP {otp} for email {email} in session')
        request.session['Mak'] = 'Tighare'
        

        request.session['otp'] = otp
        request.session['otp_email'] = email
        request.session['otp_expires_at'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        body = f'Your OTP Code code is {otp}\n\nOtp is valid for 10 min only'
        data = {
          'subject':'Verify your account',
          'body':body,
          'to_email':email
        }
        Util.send_email(data)
        return Response({"msg": "OTP sent successfully."}, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        print("Incoming request data:", request.data)
        print("Session data:", request.session.items())
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        # Retrieve session data
        session_otp = request.session.get('otp')
        session_email = request.session.get('otp_email')
        session_otp_expires_at = request.session.get('otp_expires_at')
        print(f"Test Key: {request.session.get('Mak')}")

        print(f'Session OTP: {session_otp}, Session Email: {session_email}, Session OTP Expires At: {session_otp_expires_at}')
        
        if not all([session_otp, session_email, session_otp_expires_at]):
          return Response({'msg': 'OTP not found or session expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse session_otp_expires_at back to datetime
        session_otp_expires_at = make_aware(datetime.strptime(session_otp_expires_at, '%Y-%m-%d %H:%M:%S'))

        if email != session_email:
          return Response({'msg': 'Email mismatch'}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() - timedelta(minutes=10) > session_otp_expires_at:
            return Response({'msg': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
        if str(session_otp) == str(otp):
            try:
                request.session.flush()  # Clear the session after verification
                return Response({'msg': 'OTP verified successfully'}, status=status.HTTP_200_OK)

            except Student.DoesNotExist:
                return Response({'msg': 'Unexpected error occurs please try after some time'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    print(user)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


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
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
  

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
  
class LinkedInUserIdView(APIView):
    def get(self, request):
        try:
            # Extract the Authorization header
            authorization_header = request.headers.get('Authorization')

            if not authorization_header or not authorization_header.startswith('Bearer '):
                return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)
            
            # Extract access token from the header
            access_token = authorization_header.split(' ')[1]
            print(f'Access Token: {access_token}')

            # LinkedIn API URL for fetching user profile
            url = 'https://api.linkedin.com/v2/me'

            # Set up headers
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            # Send request to LinkedIn API
            response = requests.get(url, headers=headers, timeout=5)  # 5 seconds timeout

            # Handle LinkedIn API response
            if response.status_code == 200:
                data = response.json()
                # Return LinkedIn user ID or any other required information
                return JsonResponse({'linkedInUserId': data.get('id')}, status=200)
            else:
                error_data = response.json()
                print(f'Error fetching user data: {error_data}')  # Log the error details
                return JsonResponse({'error': error_data.get('message', 'Unknown error')}, status=response.status_code)

        except requests.exceptions.Timeout:
            return JsonResponse({'error': 'Request timed out'}, status=504)
        except Exception as e:
            print(f'Error fetching LinkedIn user data: {e}')  # Log the error for debugging
            return JsonResponse({'error': 'Failed to fetch user data from LinkedIn'}, status=500)

class LinkedInPostView(APIView):
    def post(self, request):
        try:
            # Extract access token and post content from request body
            data = request.data
            access_token = data.get('accessToken')
            content = data.get('content')

            # Get LinkedIn user ID
            user_id_response = self.get_user_id(access_token)
            if user_id_response.status_code != 200:
                return user_id_response  # Forward the error response
            
            linked_in_user_id = user_id_response.json().get('linkedInUserId')
            if not linked_in_user_id:
                return JsonResponse({'error': 'User ID not found'}, status=400)

            # LinkedIn API endpoint for UGC posts
            url = 'https://api.linkedin.com/v2/ugcPosts'

            # Post body data
            body = {
                "author": f"urn:li:person:{linked_in_user_id}",  # Using the retrieved user ID
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content,  # Text for your LinkedIn post
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            # Send POST request to LinkedIn API
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, json=body)

            # Check for successful response
            if response.status_code in [200, 201]:
                return JsonResponse({
                    'message': 'Post created successfully!',
                    'data': response.json()
                }, status=200)
            else:
                return JsonResponse({
                    'error': 'Failed to create post',
                    'details': response.json()
                }, status=response.status_code)

        except Exception as e:
            return JsonResponse({
                'error': 'An error occurred',
                'details': str(e)
            }, status=500)

    def get_user_id(self, access_token):
        """Helper method to get LinkedIn user ID."""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = 'https://api.linkedin.com/v2/me'
        return requests.get(url, headers=headers)