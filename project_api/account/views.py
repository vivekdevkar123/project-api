from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
#   renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    # token = get_tokens_for_user(user)
    # return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
