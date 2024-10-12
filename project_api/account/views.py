import random
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
#Google Meet
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.shortcuts import redirect
from django.http import JsonResponse
import os
from django.conf import settings

# Define the scopes required for Google Meet (Calendar API)
SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_meet_auth(request):
    # Initialize the OAuth 2.0 flow
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'project_api/credentials/client_id.json'), SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/google-meet/callback'


    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    request.session['state'] = state
    return redirect(authorization_url)

def google_meet_callback(request):
    # Get the state parameter saved in session
    state = request.session.get('state')

    # Complete the OAuth 2.0 flow
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'project_api/credentials/client_id.json'), SCOPES, state=state)
    flow.redirect_uri = 'http://127.0.0.1:8000/google-meet/callback'

    # Fetch the token after the user approves the OAuth consent screen
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    # Get the user's credentials
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)  # Save the credentials in session

    return JsonResponse({"message": "Google Meet authenticated successfully."})

def create_google_meet(request):
    # Check if the user is authenticated and has credentials
    if 'credentials' not in request.session:
        return JsonResponse({"error": "User not authenticated. Please authenticate first."}, status=403)

    credentials = Credentials.from_authorized_user_info(request.session['credentials'], SCOPES)

    # Build the Google Calendar service
    service = build('calendar', 'v3', credentials=credentials)

    # Create a new Google Meet event (insert event in Google Calendar)
    event = {
        'summary': 'Mentor-Mentee Virtual Meeting',
        'start': {
            'dateTime': '2024-10-15T09:00:00-07:00',  # Set your start time
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2024-10-15T10:00:00-07:00',  # Set your end time
            'timeZone': 'America/Los_Angeles',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-id',  # Random string for unique request ID
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'  # Specifies Google Meet
                }
            }
        }
    }

    try:
        # Insert the event into the user's primary calendar
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        return JsonResponse({
            'meet_link': event['hangoutLink'],
            'event_id': event['id']
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def credentials_to_dict(credentials):
    """Converts the credentials to a dictionary for JSON serialization."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
#Google meet code end

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