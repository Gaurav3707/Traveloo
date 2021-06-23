from api.services import UserServices
from rest_framework.views import APIView
from rest_framework.response import Response

userServices = UserServices()

class UserSignUpView(APIView):

    def post(self, request, format=None):
        result = userServices.user_sign_up(request, format=None)
        return Response(result, status=200)


