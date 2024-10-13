import random
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    SendPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer
)
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.utils import timezone
from account.models import Student
from account.utils import Util

# Google Meet Imports
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.http import JsonResponse
from django.conf import settings
from google.oauth2 import service_account

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CALENDAR_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

class SendOTPView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['otp_email'] = email
        request.session['otp_expires_at'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        body = f'Your OTP Code is {otp}\n\nOTP is valid for 10 min only'
        data = {
            'subject': 'Verify your account',
            'body': body,
            'to_email': email
        }
        Util.send_email(data)
        return Response({"msg": "OTP sent successfully."}, status=status.HTTP_200_OK)

class VerifyOtpView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        # Retrieve session data
        session_otp = request.session.get('otp')
        session_email = request.session.get('otp_email')
        session_otp_expires_at = request.session.get('otp_expires_at')
        
        if not all([session_otp, session_email, session_otp_expires_at]):
            return Response({'msg': 'OTP not found or session expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse session_otp_expires_at back to datetime
        session_otp_expires_at = make_aware(datetime.strptime(session_otp_expires_at, '%Y-%m-%d %H:%M:%S'))

        if email != session_email:
            return Response({'msg': 'Email mismatch'}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() - timedelta(minutes=10) > session_otp_expires_at:
            return Response({'msg': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        if str(session_otp) == str(otp):
            request.session.flush()  # Clear the session after verification
            return Response({'msg': 'OTP verified successfully'}, status=status.HTTP_200_OK)
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

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
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
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link sent. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)

# Google Meet Integration
class CreateGoogleMeetLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Set up Google OAuth 2.0 flow
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CALENDAR_CREDENTIALS,
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri='http://127.0.0.1:8000/api/google-meet/callback'
        )

        # Redirect user to the Google authorization page
        authorization_url, state = flow.authorization_url(access_type='offline')
        request.session['state'] = state  # Store the state in the session
        return Response({'authorization_url': authorization_url}, status=200)

class GoogleMeetCallbackView(APIView):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CALENDAR_CREDENTIALS,
            scopes=['https://www.googleapis.com/auth/calendar'],
            state=request.session['state']
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())

        # Get credentials and create a service
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)

        # Now you can create an event with a Google Meet link
        event = {
            'summary': 'Google Meet Test',
            'start': {
                'dateTime': '2024-10-14T10:00:00-07:00',  # Adjust to your desired time
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2024-10-14T11:00:00-07:00',  # Adjust to your desired time
                'timeZone': 'America/Los_Angeles',
            },
            'conferenceData': {
                'createRequest': {
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet',
                    },
                    'requestId': 'some-random-string',
                },
            },
        }

        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        return JsonResponse({'meet_link': event.get('hangoutLink')}, status=200)
