from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.response import Response
from rest_framework import status
from accounts.forms import CustomUserLoginForm
from accounts.api.serializers import CustomRegisterSerializer, CustomLoginSerializer


class CustomLoginView(LoginView):
    
    redirect_authenticated_user = True
    serializer_class = CustomLoginSerializer

    def get_success_url(self):
        return reverse_lazy('')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Authentication')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get(self, request, format=None):
        context = {
            'form': AuthenticationForm(request=request)
        }
        return render(request,"account/login.html",context=context)
    
    # def post(self, request, format=None):
    #     print(request.data)
    #     serializer = CustomLoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
