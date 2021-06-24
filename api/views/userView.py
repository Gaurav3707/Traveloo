from api.services import UserServices
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render,redirect, HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer

userServices = UserServices()

class UserSignUpView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    def get(self, request, format=None):
        print('---------------------------get---------------------------')
        return Response(template_name='signup.html')

    def post(self, request, format=None):
        print('---------------------------post---------------------------')
        result = userServices.user_login(request, format=None)
        return Response(template_name='dashboard-02.html')


